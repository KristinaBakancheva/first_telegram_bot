import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


import collections
import csv
import settings
import translation
import re
import os


from collections import defaultdict
from datetime import date
from emoji import emojize
import ephem
from glob import glob
from random import choice


from utils import (del_symbol, get_smile, cities, check_city, prepared_example, 
                    calculation, play_random_numbers, has_object_on_picture, get_language)

# Состояние для разговора
WORDCOUNT_SENTENCE, NICKNAME, CITIES_GAME, START_CITIES_GAME, CITIES_GAME_RUS,  CITIES_GAME_UK = range(6)

class City():
    def __init__(self, country):
        self.country = country
        self.city = {"RU": list(), "EN": list()}
        if self.country == "Russia":
            file = "Russia.csv"
        else:
            file = "UK.csv"

        with open(file, "r", encoding = "utf-8") as city:
            field = city.readline().strip().split(";")
            reader = csv.DictReader(city, field, delimiter = ";")
            for lane in reader:
                self.city["RU"].append(lane["city_ru"])
                self.city["EN"].append(lane["city_en"])

class TelegramBot(object):

    def __init__(self):#, token, generator, handlers=None):
        self.TOKEN = settings.API_KEY
        self.city_dict = list()
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
        

    logging.basicConfig(filename="bot.log", level = logging.INFO) # логирование при ошибке информационных сообщений

    #PROXY = {"proxy_url": settings.PROXY_URL, "urllib3_proxy_kwargs": {"self.USERname": settings.PROXY_self.USERNAME , "password": settings.PROXY_PASSWORD}} 
    # прокси для обхода блокировки телеграмм в РФ


    def callbacks(self, update, context):
        buttom = update.callback_query.data
        if self.planets.get(buttom):
            return self.find_constellation(update, context)
        elif buttom == "Russia" or buttom == "UK":
            return self.start_city_game(update, context)




    #main handlers

    def help(self, update, context):
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["help"]
            .format(emojize(":winking_face_with_tongue:")), 
            parse_mode = "HTML")

    def reply_markup_keyboard(self):
        keyboard = [
            ["/start ✋" , "/help" , "/stop ⛔", "/end"],
            [KeyboardButton("My location", request_location = True),"/change_nickname " , "/bot_looks 🖼"],
            ["/wordcount 🎲", "/cities_game 🗺" ], 
            ["/planet 🔭","/next_full_moon 🔮", "When will be the next full moon?🔮"]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    def start_talking(self, update, context): # update - что прешло от платформы телеграм, context - используется для отправки информации платформе, а не self.USER
        nick = update.message.chat.username
        if not context.user_data.get("language"):
            context.user_data["language"] = "EN"
        # Отправляем сообщение с клавиатурой
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["start_talking"]
            .format(emojize(":waving_hand:"), nick), 
            reply_markup = self.reply_markup_keyboard(), 
            parse_mode = "HTML")

    def change_language(self, update, context):
        new_language = update.message.text.replace("/", "")
        if new_language == "RU":
            context.user_data["language"] = "RU"
        else:
            context.user_data["language"] = "EN"
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["change_language"])       
    
    def talking(self, update, context):
        text = update.message.text.lower()
        if "yes" in text.lower():
            answer = "Oh, my God! I'm just a genius! Let's try something else. :)"
        elif "no" in text.lower():
            answer = (f"Oh, I'm so sorry! Let's try again" 
            f"{emojize(':face_with_crossed_out_eyes:')}")
        else:
            answer = (f"I don't know {get_smile()}, "
                      "let's try something else.")
        update.message.reply_text(answer, reply_markup = self.reply_markup_keyboard())

    def end_talking(self, update, context):
        nickname = context.user_data.get("nickname")
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["end_talking"]
            .format(nickname, emojize(":saluting_face:")), 
            reply_markup = self.reply_markup_keyboard(), 
            parse_mode = "HTML")

    def bot_looks(self, update, context):
        pictures_emotion = glob("images/emot*.jpg")
        picture_emotion = choice(pictures_emotion)
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id = chat_id, photo = open(picture_emotion, "rb")) #rb - "read binary" (чтение в бинарном режиме)
    
    def user_location(self, update, context):
        coords = update.message.location
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["user_location"]
            .format(coords),
            reply_markup = self.reply_markup_keyboard())

    def stop(self, update, context):
        text = update.message.text
        if context.user_data.get("country"):
            country = context.user_data["country"]
            context.user_data[country]["history_list"] = list()
            context.user_data[country]["last_letter"] = ""
        if "stop" in text:
            update.message.reply_text(
                translation.translator[get_language(context.user_data)]["stop"]
                .format(emojize(":paw_prints:")),
                reply_markup = self.reply_markup_keyboard())
        return ConversationHandler.END

    # rename an appeal 
    def start_changing_nickname(self, update, context):
        # Начинаем разговор 
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["start_changing_nickname"]
            .format(context.user_data.get("nickname")),
            reply_markup = self.reply_markup_keyboard(), 
            parse_mode = "HTML")
        
        return NICKNAME

    def new_nickname(self, update, context):
        user_text = update.message.text
        context.user_data["nickname"] = user_text.capitalize()
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["new_nickname"]
            .format(context.user_data.get("nickname")), 
        reply_markup = self.reply_markup_keyboard(), parse_mode = "HTML")
        
        return ConversationHandler.END
#----------

# entertainments--

    #####----- астрономия
    def keyboard_for_planet(self, update, context):
        keyboard_planets = list()
        for key in self.planets:
            keyboard_planets.append([InlineKeyboardButton(key, callback_data=key)]) #callback_data - то что отправится в бота при нажатии кнопки

        reply_markup = InlineKeyboardMarkup(keyboard_planets)
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["keyboard_for_planet"]
            .format(emojize(":telescope:")),
            reply_markup = reply_markup)

    def find_constellation(self, update, context):
        planet = self.planets.get(update.callback_query.data)(date.today().strftime("%Y/%m/%d"))
        plant_name = update.callback_query.data.capitalize()
        constellation = ephem.constellation(planet)
        update.callback_query.answer()  # Оповещаем Telegram, что запрос обработан
        update.callback_query.edit_message_text(
            translation.translator[get_language(context.user_data)]["find_constellation"]
            .format(plant_name, constellation[1]))
    
    def next_full_moon(self, update, context):
        current_date = ephem.now()
        next_full_moon = ephem.next_full_moon(current_date)
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["next_full_moon"]
            .format(emojize(":telescope:"), next_full_moon),
            reply_markup = self.reply_markup_keyboard())
    ####------

    # count words
    def start_wordcount(self, update, context):
        # Начинаем разговор 
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["start_wordcount"]
            .format(emojize(":teacher:")), 
            reply_markup = self.reply_markup_keyboard())
        return WORDCOUNT_SENTENCE

    def count_words(self, update, context):
        user_text = (del_symbol(update.message.text)).split()
        if len(user_text) == 0:
            answer = (
                translation.translator[get_language(context.user_data)]["count_words_0"]
                .format(emojize(":face_screaming_in_fear:")))
        else:
            answer = (
                translation.translator[get_language(context.user_data)]["count_words"]
                .format(len(user_text), emojize(':check_mark_button:')))
        update.message.reply_text(answer, reply_markup = self.reply_markup_keyboard())
        return WORDCOUNT_SENTENCE
        # другой способ:
            #words = len(re.findall(r"\w+", update.message.text))
            #if words == 1:
            #    answer = "You don"t write words. Write something and I can count how many words you wrote to me"
            #else:
            #    answer = f"You wrote {words - 1} words. Is it correct?"
            #update.message.reply_text(answer)

    #игра в числа
    def guess_number(self, update, context):
        language = get_language(context.user_data)
        if not context.args: 
            answer = (translation.translator[language]["guess_number_empty"]
                      .format(emojize(':face_screaming_in_fear:')))
        else:
            try:
                user_number =  int(context.args[0])
                answer = play_random_numbers(user_number, language)
            except(TypeError, ValueError):
                answer = (
                translation.translator[language]["guess_number_integer"]
                .format(emojize(":input_number:")))
        update.message.reply_text(answer, reply_markup = self.reply_markup_keyboard())
    
    #игра в города

    def choose_contry(self, update, context):
        keyboard_country = [
            [InlineKeyboardButton("Russia", callback_data = "Russia")],
            [InlineKeyboardButton("UK", callback_data = "UK")]]
        reply_markup = InlineKeyboardMarkup(keyboard_country)
        update.message.reply_text(
            translation.translator[get_language(context.user_data)]["choose_contry"]
            .format(emojize(":pool_8_ball:")),
            reply_markup = reply_markup)
        return CITIES_GAME

    def start_city_game(self, update, context):
        country = update.callback_query.data
        self.city_dict = City(country).city
        context.user_data["country"] = country
        context.user_data[country] = dict()
        context.user_data[country]["history_list"] = list()
        context.user_data[country]["last_letter"] = ""
        update.callback_query.answer()  # Оповещаем Telegram, что запрос обработан
        update.callback_query.edit_message_text(
            translation.translator[get_language(context.user_data)]["start_city_game"]
            .format(country), 
            parse_mode = "HTML")
        return CITIES_GAME

    def cities_game(self, update, context):
        user_city = update.message.text.lower()
        country = context.user_data["country"]
        language = get_language(context.user_data)
        city_list = self.city_dict.get(language)
        letter_for_user = context.user_data[country]["last_letter"]
        letter_for_bot = user_city[-1]
        if country == "Russia" and language == "RU" and letter_for_bot in ("ь", "ы", "ъ"):
            letter_for_bot = user_city[-2]
        history_cites = context.user_data[country]["history_list"]
        if len(user_city) == 0:
            answer = (translation.translator[language]["cities_game_empty"]
                      .format(context.user_data.get("nickname"), 
                              emojize(":face_screaming_in_fear:")))
        elif letter_for_user.lower() != user_city[0].lower() and letter_for_user.lower() != "":
            answer = (translation.translator[language]["wrong_letter_city"]
                      .format(letter_for_user.lower(), user_city[0]))
        elif not check_city(user_city, city_list):
            answer = (translation.translator[language]["wrong_city"]
                      .format(user_city.capitalize()))
        elif check_city(user_city, history_cites):
            answer = (translation.translator[language]["repeat_city"]
                      .format(user_city.capitalize()))
        else:
            context.user_data[country]["history_list"].append(user_city)
            bot_city = cities(letter_for_bot.lower(), history_cites, city_list)
            if bot_city:
                context.user_data[country]["history_list"].append(bot_city.lower())
                next_letter = bot_city[-1]
                if bot_city[-1] in ("ь", "ы", "ъ"):
                    next_letter = bot_city[-2]
                context.user_data["last_letter"] = next_letter
                answer = (translation.translator[language]["cities_game"]
                          .format(context.user_data.get("nickname"), 
                                  user_city[-1], bot_city, bot_city[-1]))
            else:
                answer = (translation.translator[language]["city_lose"]
                          .format(letter_for_bot))
        update.message.reply_text(answer, reply_markup = self.reply_markup_keyboard(), 
                                  parse_mode = "HTML")
        return CITIES_GAME

    #математические операции 
    def arithmetic_operations(self, update, context):
        language = get_language(context.user_data)
        user_example = update.message.text.replace("/calc", "").replace(" ", "")
        if not context.args: 
            answer = (translation.translator[language]["arithmetic_operations_empty"]
                      .format(emojize(":face_screaming_in_fear:")))
        elif user_example.count("(") != user_example.count(")"):
            answer = translation.translator[language]["arithmetic_operations_()"]
        elif not re.search("[0-9-+*/()]", user_example):
            answer = translation.translator[language]["arithmetic_operations_symbol"]
        else:
            instance_ex  = prepared_example(user_example)
            answer = calculation(instance_ex)
        update.message.reply_text(answer, reply_markup = self.reply_markup_keyboard(), 
                                  parse_mode = "HTML")

    def check_user_photo(self, update, context):
        language = get_language(context.user_data)
        update.message.reply_text(
            translation.translator[language]["check_user_photo_1"])
        os.makedirs("downlowds", exist_ok = True)
        photo = update.message.photo[-1]
        photo_file = context.bot.get_file(photo.file_id)
        file_name = os.path.join("downlowds", f"{photo.file_id}.jpg")
        photo_file.download(file_name)
        update.message.reply_text(
            translation.translator[language]["check_user_photo_2"])
        if has_object_on_picture(file_name, "people"):
            update.message.reply_text(
                translation.translator[language]["check_user_photo_people"]
                .format(emojize(":face_blowing_a_kiss:")))
            os.makedirs("images/human", exist_ok = True)
            new_file_name = os.path.join("images/human", f"human_{photo_file.file_id}.jpg")
            os.rename(file_name, new_file_name)
        else:
            os.remove(file_name)
            update.message.reply_text(
                translation.translator[language]["check_user_photo_no"])
        #print(update.message.photo)


    def main(self):

        mybot = Updater(self.TOKEN, use_context=True)#, request_kwargs = PROXY)

        dp = mybot.dispatcher # просто для сохращения вводим переменную dp
        dp.add_handler(CommandHandler("start", self.start_talking)) # добавим обработчик CommandHandler который будет реагировать на коману start функцией hello_self.USER 
        dp.add_handler(CallbackQueryHandler(self.callbacks))
        dp.add_handler(CommandHandler("planet", self.keyboard_for_planet))
        dp.add_handler(CommandHandler("end", self.end_talking))
        dp.add_handler(CommandHandler("guess", self.guess_number))
        dp.add_handler(CommandHandler("bot_looks", self.bot_looks))
        dp.add_handler(MessageHandler(Filters.photo, self.check_user_photo))
        dp.add_handler(CommandHandler("next_full_moon", self.next_full_moon))
        dp.add_handler(MessageHandler(Filters.regex("When will be the next full moon?"), self.next_full_moon))
        dp.add_handler(CommandHandler("RU", self.change_language))
        dp.add_handler(CommandHandler("EN", self.change_language))
        dp.add_handler(MessageHandler(Filters.regex("RU"), self.change_language))
        dp.add_handler(MessageHandler(Filters.regex("EN"), self.change_language))
        dp.add_handler(CommandHandler("calc", self.arithmetic_operations))
        dp.add_handler(CommandHandler("help", self.help))
        dp.add_handler(MessageHandler(Filters.location, self.user_location))
        
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
        conv_nickname = ConversationHandler(
            entry_points=[CommandHandler("change_nickname", self.start_changing_nickname)],
            states={
                NICKNAME: [MessageHandler(Filters.text & ~Filters.command, self.new_nickname)],
            },
            fallbacks=[CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_nickname)
           
    # cities game    
        conv_cities_game = ConversationHandler(
            entry_points = [CommandHandler("cities_game", self.choose_contry)],
            states = {
                START_CITIES_GAME: [MessageHandler(Filters.text & ~Filters.command, self.start_city_game)],
                CITIES_GAME: [MessageHandler(Filters.text & ~Filters.command, self.cities_game)],
            },
            fallbacks = [CommandHandler("stop", self.stop)],
        )
        dp.add_handler(conv_cities_game)

 
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.talking)) # общий и перехватывает все


        logging.info("The bot started")
        mybot.start_polling()
        mybot.idle()


if __name__ == "__main__":
    bot = TelegramBot()
    bot.main()
