import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


import collections
import csv
import settings
import re


from collections import defaultdict, Counter
from datetime import date
from emoji import emojize
import ephem
from glob import glob
from random import randint, choice
from textwrap import dedent


# Состояние для разговора
WORDCOUNT_SENTENCE, NICKNAME, CITIES_GAME_RUS,  CITIES_GAME_UK = range(4)

class TelegramBot(object):

    def __init__(self):#, token, generator, handlers=None):
        self.TOKEN = settings.API_KEY
        self.USER = None
        self.planets = {
            "Mercury": ephem.Mercury,
            "Venus": ephem.Venus,
            "Mars": ephem.Mars,
            "Jupiter": ephem.Jupiter,
            "Saturn": ephem.Saturn,
            "Uranus": ephem.Uranus,
            "Neptune": ephem.Neptune,
            "Pluto": ephem.Pluto
            }
        self.UK_city = []
        with open("gb.csv", "r", encoding="utf-8") as c:
            reader = csv.DictReader(c)
            for lane in reader:
                self.UK_city.append(lane["city"])
            

    
    logging.basicConfig(filename="bot.log", level = logging.INFO) # логирование при ошибке информационных сообщений

    #PROXY = {"proxy_url": settings.PROXY_URL, "urllib3_proxy_kwargs": {"self.USERname": settings.PROXY_self.USERNAME , "password": settings.PROXY_PASSWORD}} 
    # прокси для обхода блокировки телеграмм в РФ

    def help(self, update, context):
        update.message.reply_text((f"Hey hey! I am Bot and I can do a lot of "
        "interesting activities but I'm still developing.\n"
        "<b>Commands</b>:\n"
        " • /start - Start conversation\n"
        " • /help - Information about my abilities\n"
        " • /change_nickname - You can write a word and I save it like your nickname. " 
        "I will use it for naming you \n"
        " • /wordcount - I can count how many words you write to me\n" 
        " • /planet - I can find out in which constellation any planet is today. "
        "If you use this command - \n I show list of planet, you should chouse one and "
        "I show in which constellation this planet is today\n" 
        " • /next_full_moon - I can find out when will be next full moon\n" 
        " • /bot_looks - You can use this command and I'll show you how I looks like. "
        "Which emotion I'm feeling right now\n" 
        " • /cities_game_ru - It's a game in cities in Russia and use russian language. "
        "You can press this command and see the rule of this game\n"
        " • /cities_game_UK  - It's a game in cities in UK. You can press this command "
        "and see the rule of this game\n" 
        " • /guess - It's also a game. You choose number, then I chose a number +- 10. "
        "Win  person, whose number will be bigger\n"
        " • /calc - You can write any examle with +-*/() and I count the result \n"
        " • /stop - Stop any comman/game. I recomend to use this command at the end "
        "of every command\n" 
        " • /end - End conversation. I say to yo 'Good bye'\n" 
        f"{emojize(':winking_face_with_tongue:')} I am happy to speak with you. "), 
        parse_mode = "HTML")



    def start_talking(self, update, context): # update - что прешло от платформы телеграм, context - используется для отправки информации платформе, а не self.USER
        keyboard = [
            ["/start ✋"], 
            ["/help" , "/stop ⛔", "/end"],
            ["/change_nickname " , "/bot_looks 🖼"],
            ["/wordcount 🎲"], 
            ["/planet 🔭","/next_full_moon 🔮"],
            ["/cities_game_ru 🗺" , "/cities_game_UK 🇬🇧"]]
        
        #smile = choice(settings.USER_EMOJI) # заводить как отдельную переменную стоит если хотим сделать рандомный выбор смайликов
        #smile = emojize(smile)

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        # Отправляем сообщение с клавиатурой
        update.message.reply_text((f"Hey hey! {emojize(':waving_hand:')} "
        "I am <b>Bot</b>. Can you press a command /change_nickname \n and "
        "I will now how call you. You also can press a command /help and "
        "I describe all my commands"), reply_markup = reply_markup, parse_mode = "HTML")

    def get_smile(self):
        return emojize(choice(settings.USER_EMOJI))

    def talking(self, update, context):
        text = update.message.text.lower()
        if "yes" in text.lower():
            answer = "Oh, my God! I'm just a genius! Let's try something else. :)"
        elif "no" in text.lower():
            answer = (f"Oh, I'm so sorry! Let's try again" 
            f"{emojize(':face_with_crossed_out_eyes:')}")
        else:
            answer = (f"I don't know {self.get_smile()}, "
                      "let's try something else.")
        update.message.reply_text(answer)

    def end_talking(self, update, context):
        update.message.reply_text(f"Good bye <b>{context.user_data.get('nickname')}</b>! "
        f"{emojize(':saluting_face:')}", parse_mode = "HTML")

    # rename an appeal 
    def start_changing_nickname(self, update, context):
        # Начинаем разговор 
        update.message.reply_text((f"Hello. You would like to change your nickname - "
        f"<b>{context.user_data.get('nickname')}</b>? Write new nickname."), 
        parse_mode = "HTML")
        
        return NICKNAME

    def new_nickname(self, update, context):
        user_text = update.message.text
        
        context.user_data["nickname"] = user_text.capitalize()
        update.message.reply_text((f"Nice to meet you, <b>{context.user_data.get('nickname')}</b>."
        f" If this nickname is incorrect you can try to change it again."), parse_mode = "HTML")
        
        return ConversationHandler.END


    #####----- астрономия
    def keyboard_for_planet(self, update, context):
        keyboard_planets = list()
        for key in self.planets:
            keyboard_planets.append([InlineKeyboardButton(key, callback_data=key)])

        reply_markup = InlineKeyboardMarkup(keyboard_planets)
        update.message.reply_text(f"Choose a planet: {emojize(':telescope:')} ", 
                                  reply_markup = reply_markup)

    def find_constellation(self, update, context):
        planet = self.planets.get(update.callback_query.data)(date.today().strftime("%Y/%m/%d"))
        plant_name = update.callback_query.data.capitalize()
        constellation = ephem.constellation(planet)
        update.callback_query.answer()  # Оповещаем Telegram, что запрос обработан
        update.callback_query.edit_message_text((f"The planet {plant_name} is in "
                                                 f"the constellation {constellation[1]} today."))
    
    def next_full_moon(self, update, context):
        current_date = ephem.now()
        next_full_moon = ephem.next_full_moon(current_date)
        update.message.reply_text(f"Hello. Next full moon will be {next_full_moon} "
                                  f"{emojize(':telescope:')}.")
    ####------

    # count words
    def start_wordcount(self, update, context):
        # Начинаем разговор 
        update.message.reply_text(f"Hello. I can count how many words you "
                                  f"wrote {emojize(':teacher:')}.")
        return WORDCOUNT_SENTENCE

    def count_words(self, update, context):
        user_text = (del_symbol(update.message.text)).split()
        if len(user_text) == 0:
            answer = (f"You don't write words. {emojize(':face_screaming_in_fear:')} "
                      f"Write something and I can count how many words you wrote to me")
        else:
            answer = (f"You wrote {len(user_text)} words {emojize(':check_mark_button:')}."
                      f"If you would like to finish - choose comand /stop")
        update.message.reply_text(answer)
        return WORDCOUNT_SENTENCE
        # другой способ:
            #words = len(re.findall(r"\w+", update.message.text))
            #if words == 1:
            #    answer = "You don"t write words. Write something and I can count how many words you wrote to me"
            #else:
            #    answer = f"You wrote {words - 1} words. Is it correct?"
            #update.message.reply_text(answer)

    #игра в числа
    def play_random_numbers(self, user_number):
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
    
    def guess_number(self, update, context):
        if not context.args: 
            answer = f"You don't right anything {emojize(':face_screaming_in_fear:')}."
        else:
            try:
                user_number =  int(context.args[0])
                answer = self.play_random_numbers(user_number)
            except(TypeError, ValueError):
                answer = f"Write an integer {emojize(':input_number:')}."
        update.message.reply_text(answer)
    

    def cities(self, letter, history_list, cities_list):
        next_cities = [x for x in cities_list 
                       if x[0].lower() == letter and x.lower() not in history_list]
        city = choice(next_cities)
        return city

    def check_city(self, city, cities_list):
        # count or find should work
        l =  [x for x in cities_list if x.lower() == city]
        return len(l) == 1


    #игра в города
    def cities_ru_game_start(self, update, context):
        # Начинаем разговор 
        context.user_data['history_list'] = list()
        context.user_data['last_letter'] = ""
        update.message.reply_text((f"Класс, давай поиграем в города России"
        "Правила очень простые - сначала тебе нужно назвать любой город \n "
        "России, затем я нозову город, который начинается на последнюю букву твоего "
        "города(не учитываем ь, ы, ъ). Далее ты должен сделать тоже самое. "
        f"Ты не можешь повторяться. \n{emojize(':pool_8_ball:')}. \n Давай начнем! "
        "Назови любой город."), parse_mode = "HTML")
        return CITIES_GAME_RUS

    def cities_ru_game(self, update, context):
        user_city = update.message.text.lower()
        letter_for_user = context.user_data["last_letter"]
        letter_for_bot = user_city[-1]
        if letter_for_bot in ("ь", "ы", "ъ"):
                    letter_for_bot = user_city[-2]
        history_cites = context.user_data["history_list"]
        if len(user_city) == 0:
            answer = (f"<b>{context.user_data.get('nickname')}</b>, ты ничего не "
                      f"написал.{emojize(':face_screaming_in_fear:')} Напиши "
                      f"название любого города. Если хочешь закончить игру - "
                      f"нажми команду - /stop")
        elif letter_for_user.lower() != user_city[0].lower() and letter_for_user.lower() != "":
            answer = (f"Подожди подожди, твоя буква была <b>{letter_for_user.lower()}</b>, "
                      f"но ты написал город на букву <b>{user_city[0]}</b>. Попробуй еще раз")
        elif not self.check_city(user_city, settings.CITIES_RUSSIA):
            answer =(f"Подожди подожди, я не могу найти такого города " 
                     f"{user_city.capitalize()}. Попробуй другой город")
        elif self.check_city(user_city, history_cites):
            answer = (f"Подожди подожди, у нас уже был этот город {user_city.capitalize()}. " 
                     f"Так не честно. Попробуй другой город")
        else:
            context.user_data['history_list'].append(user_city)
            bot_city = self.cities(letter_for_bot.lower(), history_cites, settings.CITIES_RUSSIA)
            if bot_city:
                context.user_data["history_list"].append(bot_city.lower())
                next_letter = bot_city[-1]
                if bot_city[-1] in ("ь", "ы", "ъ"):
                    next_letter = bot_city[-2]
                context.user_data["last_letter"] = next_letter
                answer = (f"Класс <b>{context.user_data.get('nickname')}</b>! "
                          f"Мне на <b>{letter_for_bot.lower()}</b>. Мой город - "
                          f"{bot_city.capitalize()}, тебе на <b>{next_letter}</b>. "
                          f"Если хочешь закончить игру - нажми команду - /stop")
            else:
                answer = f"Ты выиграл. Я не знаю городов на букву <b>{letter_for_bot.lower()}</b>"
        update.message.reply_text(answer, parse_mode = "HTML")
        return CITIES_GAME_RUS
    #update.message.reply_text(f"Good bye  <b>{context.user_data.get('nickname')}</b>! {emojize(':saluting_face:')}" , parse_mode="HTML")

    #игра в города
    def cities_game_start_UK(self, update, context):
        # Начинаем разговор 
        context.user_data['history_list'] = list()
        context.user_data['last_letter'] = ""
        update.message.reply_text((f"Cool, let's play in the cities in UK."
        "The rules are very simple - you need to name \n any city in UK, then "
        "I'll name a city which start with the last letter of your city. "
        "Then it's your \n turn again to name a city which start with the last "
        f"letter of my city. You can't repeat yourself. {emojize(':pool_8_ball:')}. \n "
        "Let'go! Name the first city."), parse_mode = "HTML")
        return CITIES_GAME_UK


    def cities_game_UK(self, update, context):
        user_city = update.message.text.lower()
        letter_for_user = context.user_data["last_letter"]
        letter_for_bot = user_city[-1]
        history_cites = context.user_data["history_list"]
        if len(user_city) == 0:
            answer = ( f"<b>{context.user_data.get('nickname')}</b>, You haven't written "
            f"anything. {emojize(':face_screaming_in_fear:')}. Please write the name "
            "of any city. If you want to finish the game, press the command - /stop")
        elif letter_for_user.lower() != user_city[0].lower() and letter_for_user != "":
            answer = (f"Wait, wait, your letter was <b>{letter_for_user}</b>, "
            f"but you wrote a city starting with <b>{user_city[0]}</b>.")
        elif not self.check_city(user_city, self.UK_city):
            answer = (f"Please wait, I can't find a city with that "
            f"name {user_city.capitalize()}. Try to choose another city.")
        elif self.check_city(user_city.lower(), history_cites):
            answer = (f"Please wait, we already wrote this city {user_city.capitalize()}. " 
            f"It's not fair. Try it in another city.")
        else:
            context.user_data["history_list"].append(user_city.lower())
            bot_city = self.cities(letter_for_bot, history_cites, self.UK_city)
            if bot_city:
                context.user_data["history_list"].append(bot_city)
                context.user_data["last_letter"] = bot_city[-1]
                answer = (f"Cool {context.user_data.get('nickname')}! The last lettor "
                f"of your city was <b>{user_city[-1]}</b> and my city is {bot_city}. \n "
                f"You should name a city which start with letter - <b>{bot_city[-1]}</b> "
                "If you want to end the game, please use the command. - /stop")
            else:
                answer = (f"You've won. I do not know the cities which "
                          f"start with letter <b>{letter_for_bot}</b>")
        update.message.reply_text(answer, parse_mode = "HTML")
        return CITIES_GAME_UK

    def bot_looks(self, update, context):
        pictures_emotion = glob('images/emot*.jpg')
        picture_emotion = choice(pictures_emotion)
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id = chat_id, photo = open(picture_emotion, 'rb')) #rb - "read binary" (чтение в бинарном режиме)
    
    #математические операции 
    def operation(self, x, y, action):
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

    def prepared_example(self, x):
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

    def clean_el(self, where, i, n):
        while n != 0:
            where.pop(i)
            n -= 1
        return where 
    
    def calculation(self, example):
        i = 0
        while len(example) >= 1:
            actions = Counter(example)
            if len(example) == 1:
                return example[0]
            priority = [i for i in range(len(example)) if example[i] == "("]
            if len(priority)!=0:
                first = priority[0]
                last = len(example) + [i for i in range(-1, -len(example)+first, -1) if example[i] == ")"][0]
                res = self.calculation(example[first+1:last])
                example[first] = res
                example = self.clean_el(example, first+1, last-first)
                i = -1
            elif example[i] == "*" or example[i] == "/":
                res = self.operation( example[i-1], example[i+1], example[i])
                actions[example[i]] -= 1
                example[i-1] = res 
                example = self.clean_el(example, i, 2)
                i = -1
            elif (actions.get("*") is None and actions.get("/") is None) and (example[i] =="+" or example[i] == "-"):
                res = self.operation( example[i-1], example[i+1], example[i])
                actions[example[i]] -= 1
                example[i-1] = res  
                example = self.clean_el(example, i, 2)
                i = -1
            i+=1   

    def arithmetic_operations(self, update, context):
        user_example = update.message.text.replace("/calc", "").replace(" ", "")
        if not context.args: 
            answer = f"You don't right anything {emojize(':face_screaming_in_fear:')}."
        elif user_example.count("(") != user_example.count(")"):
            answer = (f"You create a mistake with <b>(</b> or <b>)</b>. "
            "Your example has different amount of this symbol")
        elif not re.search("[0-9-+*/()]", user_example):
            answer = (f"You can use only integers or symbol: +-/*(), but you used "
                      "something else. Try again")
        else:
            instance_ex  = self.prepared_example(user_example)
            answer = self.calculation(instance_ex)
        update.message.reply_text(answer, parse_mode = "HTML")




    def stop(self, update, context):
        context.user_data['history_list'] = list()
        context.user_data['last_letter'] = ""
        update.message.reply_text(f"Ok. We have finished this task. You " 
                                  f"can choose new comand {emojize(':paw_prints:')}.")
        return ConversationHandler.END


    def main(self):

        mybot = Updater(self.TOKEN, use_context=True)#, request_kwargs = PROXY)

        dp = mybot.dispatcher # просто для сохращения вводим переменную dp
        dp.add_handler(CommandHandler("start", self.start_talking)) # добавим обработчик CommandHandler который будет реагировать на коману start функцией hello_self.USER 
        dp.add_handler(CallbackQueryHandler(self.find_constellation))
        dp.add_handler(CommandHandler("planet", self.keyboard_for_planet))
        dp.add_handler(CommandHandler("end", self.end_talking))
        dp.add_handler(CommandHandler("guess", self.guess_number))
        dp.add_handler(CommandHandler("bot_looks", self.bot_looks))
        dp.add_handler(CommandHandler("next_full_moon", self.next_full_moon))
        dp.add_handler(CommandHandler("calc", self.arithmetic_operations))
        dp.add_handler(CommandHandler("help", self.help))
        
    # wordcount    
    # Определяем обработчик разговоров `ConversationHandler` 
        # с состоянием WORDCOUNT_SENTENCE
        conv_wordcount = ConversationHandler( # здесь строится логика разговора
            # точка входа в разговор
            entry_points = [CommandHandler("wordcount", self.start_wordcount)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states = {
                WORDCOUNT_SENTENCE: [MessageHandler(Filters.text & ~Filters.command, self.count_words)],
            },
            # точка выхода из разговора
            fallbacks = [CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_wordcount)

    # rename an appeal    
        conv_nickname = ConversationHandler( # здесь строится логика разговора
            # точка входа в разговор
            entry_points=[CommandHandler("change_nickname", self.start_changing_nickname)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states={
                NICKNAME: [MessageHandler(Filters.text & ~Filters.command, self.new_nickname)],
            },
            # точка выхода из разговора
            fallbacks=[CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_nickname)
           
    # cities game    
        conv_cities_game = ConversationHandler( # здесь строится логика разговора
            # точка входа в разговор
            entry_points = [CommandHandler("cities_game_ru", self.cities_ru_game_start)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states = {
                CITIES_GAME_RUS: [MessageHandler(Filters.text & ~Filters.command, self.cities_ru_game)],
            },
            # точка выхода из разговора
            fallbacks = [CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_cities_game)

    # cities game    
        conv_cities_game_UK = ConversationHandler( # здесь строится логика разговора
            # точка входа в разговор
            entry_points = [CommandHandler("cities_game_UK", self.cities_game_start_UK)],
            # этапы разговора, каждый со своим списком обработчиков сообщений
            states = {
                CITIES_GAME_UK: [MessageHandler(Filters.text & ~Filters.command, self.cities_game_UK)],
            },
            # точка выхода из разговора
            fallbacks = [CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_cities_game_UK)

        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.talking)) # общий и перехватывает все



#nickname
####

        logging.info("The bot started")
        mybot.start_polling()
        mybot.idle()

def del_symbol(str):
    garbage = "!@#$%^&*()_+-=№:,.;{}[]<>/?\\|~`'\""
    for symbol in garbage:
        str = str.replace(symbol, "")
    return str

if __name__ == "__main__":
    bot = TelegramBot()
    bot.main()

    


#ephem.next_full_moon(ДАТА)