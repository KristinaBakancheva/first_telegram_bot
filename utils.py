from collections import Counter, defaultdict
from emoji import emojize
from random import randint, choice

import csv
import re
import settings
import translation

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2


def get_language(info):
    if not info.get("language"):
        return "EN"
    return info.get("language")

    
def del_symbol(str):
    garbage = "!@#$%^&*()_+-=№:,.;{}[]<>/?\\|~`'\""
    for symbol in garbage:
        str = str.replace(symbol, "")
    return str

def get_smile():
    return emojize(choice(settings.USER_EMOJI))

def cities(letter, history_list, city_list):
    next_cities = [x for x in city_list 
                   if x and x[0].lower() == letter and x.lower() not in history_list]
    city = choice(next_cities)
    return city

def check_city(city, city_list):
    # count or find should work
    l =  [x for x in city_list if x.lower() == city]
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

def play_random_numbers(user_number, language):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        result = (translation.translator[language]["guess_number_lose"]
                .format(user_number, bot_number, emojize(":partying_face:")))
    elif user_number==bot_number:
        result = (translation.translator[language]["guess_number_draw"]
                .format(user_number, bot_number, emojize(":handshake:")))
    else:
        result = (translation.translator[language]["guess_number_draw"]
                .format(user_number, bot_number, emojize(":smiling_face_with_sunglasses:")))
    return result




def check_response(response, object):        
    if response.status.code == status_code_pb2.SUCCESS:
        for consept in response.outputs[0].data.concepts:
            if consept.name == object and consept.value >= 0.90:
                return True
    else:
        print(f"Error {response.outpots[0].status.description}")
    return False

def has_object_on_picture(file_name, object):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (("authorization", f"Key {settings.CLARIFAI_API_KEY}"),)
    with open(file_name, "rb") as f:
        file_data = f.read()
        image = resources_pb2.Image(base64 = file_data)
        request = service_pb2.PostModelOutputsRequest(
            model_id = "aaa03c23b3724a16a56b629203edc62c", # базовая модель из документации
            inputs = [
                resources_pb2.Input(
                    data = resources_pb2.Data(image = image)
                )
            ])
        response = app.PostModelOutputs(request, metadata = metadata)
        return check_response(response, object)
    
def check():
    city_russia = dict()
    with open("Russia.csv", encoding = "UTF-8") as r:
        #field = r[0]
        reader = csv.reader(r, delimiter = ";")
        city_ru = defaultdict(int)
        city_en = defaultdict(int)
        for line in reader:
            city_ru[line[0]] += 1
            city_en[line[1]] += 1
        city_russia["RU"] = city_ru
        city_russia["EN"] = city_en



if __name__ == "__main__":
    print(check())