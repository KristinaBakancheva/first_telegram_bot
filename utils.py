from collections import Counter
from emoji import emojize
from random import randint, choice

import re
import settings



def del_symbol(str):
    garbage = "!@#$%^&*()_+-=№:,.;{}[]<>/?\\|~`'\""
    for symbol in garbage:
        str = str.replace(symbol, "")
    return str

def get_smile():
    return emojize(choice(settings.USER_EMOJI))

def cities(letter, history_list, cities_list):
    next_cities = [x for x in cities_list 
                   if x[0].lower() == letter and x.lower() not in history_list]
    city = choice(next_cities)
    return city

def check_city(city, cities_list):
    # count or find should work
    l =  [x for x in cities_list if x.lower() == city]
    return len(l) == 1

def operation(x, y, action):
        if action == "+":
            return x + y
        elif action == "-":
            return x - y
        elif action == "*":
            return x * y
        elif action == "/":
            if y == 0:
                return "You can't divide by 0"
            return x / y
        else:
            return "I don't know how to do it."

def prepared_example(x):
        instance = list()
        pred, cur = 0, 0
        while cur < len(x):
            if re.search("[0-9]", x[cur]):
                cur += 1
            else:
                if pred != cur:
                    instance.append(int(x[pred: cur]))
                instance.append(x[cur])
                cur += 1
                pred = cur
        if pred != cur:
            instance.append(int(x[pred: cur])) 
        return instance

def clean_el(where, i, n):
        while n != 0:
            where.pop(i)
            n -= 1
        return where 

def calculation(example):
        i = 0
        while len(example) >= 1:
            actions = Counter(example)
            if len(example) == 1:
                return example[0]
            priority = [i for i in range(len(example)) if example[i] == "("]
            if len(priority)!=0:
                first = priority[0]
                last = len(example) + [i for i in range(-1, -len(example)+first, -1) if example[i] == ")"][0]
                res = calculation(example[first+1:last])
                example[first] = res
                example = clean_el(example, first+1, last-first)
                i = -1
            elif example[i] == "*" or example[i] == "/":
                res = operation( example[i-1], example[i+1], example[i])
                actions[example[i]] -= 1
                example[i-1] = res 
                example = clean_el(example, i, 2)
                i = -1
            elif (actions.get("*") is None and actions.get("/") is None) and (example[i] =="+" or example[i] == "-"):
                res = operation( example[i-1], example[i+1], example[i])
                actions[example[i]] -= 1
                example[i-1] = res  
                example = clean_el(example, i, 2)
                i = -1
            i+=1   

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        result = (f"Your number was {user_number}, my number is {bot_number}." 
                  f"You win {emojize(':partying_face:')}.")
    elif user_number==bot_number:
        result = (f"Your number was {user_number}, my number is {bot_number}. "
                  f"It's draw {emojize('handshake')}.")
    else:
        result = (f"Your number was {user_number}, my number is {bot_number}. "
                  f"I win {emojize(':smiling_face_with_sunglasses:')}.")
    return result