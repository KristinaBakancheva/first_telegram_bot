from emoji import emojize

translator = {
    "RU": {
        "help": (f" Привет! Я бот, и я могу делать много "
                    "интересных действий, но я все еще развиваюсь.\n"
                    "<b>Команды</b>:\n"
                    " • /start - начать разговор\n"
                    " • /help - Информация о моих способностях\n"
                    " • /change_nickname - вы можете написать слово, и я буду "
                    "использовать его для обращения к вам \n"
                    " • /wordcount - я могу подсчитать, сколько слов вы мне написали\n" 
                    " • /planet - я могу узнать, в каком созвездии сегодня находится"
                    " любая планета. Если вы используете эту команду - \nя показываю "
                    "список планет, вам следует выбрать одну и я покажу, \nв каком "
                    "созвездии сегодня находится эта планета\n" 
                    " • /next_full_moon  - я могу узнать, когда будет "
                    "следующее полнолуние\n" 
                    " • When will be the next full moon? - Я могу узнать, когда "
                    "будет следующее полнолуние\n"
                    " • /bot_looks - Вы можете использовать эту команду, и я покажу "
                    "вам, как я выгляжу. Какие эмоции я испытываю прямо сейчас?\n" 
                    " • /cities_game_ru - Это игра в города России, в которой "
                    "используется русский язык. Вы можете нажать эту команду и "
                    "ознакомиться с правилами этой игры\n"
                    " • /cities_game_UK - Это игра в города Великобритании. "
                    "Вы можете нажать эту команду и ознакомиться с правилами этой игры\n" 
                    " • /guess - это тоже игра. Вы выбираете число, затем я выбираю "
                    "число +- 10. Победит тот, чье число будет больше\n"
                    " • /calc - Вы можете записать любой математический пример с "
                    "помощью +-*/(), и я подсчитаю результат \n"
                    " • /stop - останавливает любую команду/игру. Я рекомендую "
                    "использовать эту команду в конце каждой команды\n" 
                    " • My location - вы можете нажать на эту кнопку, и я покажу "
                    "вам ваши координаты \n"
                    " • Photo - вы можете прислать мне фотографию, и я сохраню "
                    "ее в определенном месте если на фотографии есть человек.\n"
                    " • /end - конец разговора Я говорю тебе 'До свидание'.\n"
                    "{} Я рад поговорить с тобой."),
        "change_language": "Спасибо! Твой язык теперь русский",
        "start_talking": ("Привет, привет! {} "
                          "Я <b>бот</b>. Обычно я говорю по-английски, но "
                          "Я также знаю русский.\nВы можете нажать /RU или написать RU для "
                          " русского языка, или нажать /EN или написать EN для английского.\n"
                          "Я знаю что ты <b>{}</b>, ты можешь нажать команду "
                          "\n/change_nickname, и выбрать новый ник. \nВы также можете" 
                          "нажать команду /help и Я направлю описание всех своих команд"),
        "end_talking": "Пока пока <b>{}</b>! {}",
        "user_location": "Твои координаты - {}",
        "stop": "Ок. Я заканчиваю предыдущую задачу. Ты можешь выбрать новую команду {}.",
        "start_changing_nickname": ("Привет. Ты хотел бы сменить твой ник <b>{}</b>?"
                                    " Напиши свой новый ник"),
        "new_nickname": ("Приятно с тобой познакомиться, <b>{}</b>. Если указан не "
                         "вернй ник ты можешь сменить его снова."),
        "keyboard_for_planet": "Выбери планету {}: ",
        "find_constellation": "Планета {} сегодня находится в созвездии {}.",
        "next_full_moon": "Привет. {} Следующее полнолуние будет {} ",
        "start_wordcount": "Привет. Я могу посчитать сколько слов ты мне напишешь {}.",
        "count_words_0": ("Ты ничего не написал. {} Напиши что-нибудь и  " 
                          "я смогу посчитать сколько слов ты написал"),
        "count_words": ("Ты написал {} слов {}. Если ты хочешь закончить  "
                        "- выбери команду /stop"),
        "guess_number_empty": "Ты ничего не написал {}.",
        "guess_number_integer": "Ты должен написать число {}.",
        "guess_number_lose": "Твой номер {}, мой номер - {}. Ты выиграл {}.",
        "guess_number_draw": "Твой номер {}, мой номер - {}. Ничья {}.",
        "guess_number_win": "Твой номер {}, мой номер - {}. Я выиграл {}.",
        "arithmetic_operations_empty": "Ты не написал ничего {}.",
        "arithmetic_operations_()": ("Ты допустил ошибку с <b>(</b> or <b>)</b>. "
                                     "В твоем примере разное количество этих символов"),
        "arithmetic_operations_symbol": ("Ты можешь использовать только числа и " 
                                         "символы: +-/*(), но ты использовал что-"
                                         "то кроме этого. Попробуй еще раз."),
        "check_user_photo_1": ("Я получил твою картинку и начал процесс ее загрузки "
                               "для дальнейшего анализа"),
        "check_user_photo_2": ("Твоя картинка была успешна загружена и я начал процесс"
                               "поиска людей на каринке"),
        "check_user_photo_people": ("Ооо, Я нашел людей на фото! Я хочу сохранить "
                                    "эту картинку. Спасибо! {}"),
        "check_user_photo_no": ("Я не нашел людей на картинке и удалил её."
                                "Спасибо что поделился."),
        "cities_game_empty": ("<b>{}</b> Ты не написал ничего {}. Пожалуйста напиши название"
                          "любого города. Если ты хочешь закончить игру, нажми "
                          "команду - /stop"),
        "wrong_letter_city": ("Подожди подожди, твоя буква была <b>{}</b>, но ты "
                              "написал город который начинается на <b>{}</b>."),
        "wrong_city": ("Подожди, Я не могу найти город с названием {}. "
                       "Попробуй другой город."),
        "repeat_city": ("Подожди, ты уже называл этот город {}. Это не честно. "
                        "Попробуй другой город."),
        "cities_game": ("Отлично {}! Последняя буква твоего города <b>{}</b> и "
                           "мой город - {}. \nТебе нужно назвать город на букву "
                           " - <b>{}</b>\nЕсли ты Если ты хочешь закончить игру, "
                           "нажми команду - /stop"),
        "city_lose": ("Ты выиграл. Я не знаю больше городовкоторые начинаются с "
                         "буквы <b>{}</b>"),
        "choose_contry": ("Класс, давай поиграем в города. Правила очень простые - "
                          "сначала тебе нужно назвать любой город,\nзатем я "
                          "нозову город, который начинается на последнюю букву "
                          "твоего города(не учитываем ь, ы, ъ). Далее ты должен "
                          "сделать тоже самое. Ты не можешь повторяться {}. \n"
                          "Давай начнем! Сначала выбери страну - /Russia или /UK."),
        "start_city_game": "Ок. Давай начнем. Ты выбрал <b>{}</b>. Назови первый город."
    }, 
    "EN": {
        "help":(f"Hey hey! I am Bot and I can do a lot of "
                    "interesting activities but I'm still developing.\n"
                    "<b>Commands</b>:\n"
                    " • /start - Start conversation\n"
                    " • /help - Information about my abilities\n"
                    " • /change_nickname - You can write a word and I save it "
                    "like your nickname. I will use it for naming you \n"
                    " • /wordcount - I can count how many words you write to me\n" 
                    " • /planet - I can find out in which constellation any planet today. "
                    "If you use this command - \n I show list of planet, you should "
                    "chouse one and I show in which constellation this planet today\n" 
                    " • /next_full_moon - I can find out when will be next full moon\n" 
                    " • When will be the next full moon? -  I can find out when will "
                    "be next full moon\n"
                    " • /bot_looks - You can use this command and I'll show you how "
                    "I looks like. Which emotion I'm feeling right now\n" 
                    " • /cities_game_ru - It's a game in cities in Russia and use russian "
                    "language. You can press this command and see the rule of this game\n"
                    " • /cities_game_UK  - It's a game in cities in UK. You can press "
                    "this command and see the rule of this game\n" 
                    " • /guess - It's also a game. You choose number, then I chose a "
                    "number +- 10. Win  person, whose number will be bigger\n"
                    " • /calc - You can write any examle with +-*/() and I count the result \n"
                    " • /stop - Stop any command/game. I recomend to use this "
                    "command at the end of every command\n" 
                    " • My location - you can press this buttom and I'll show you "
                    "your coordinate\n"
                    " • Photo - you can send me a pictire and I will save it in a "
                    "specific place if there is a human on the photo.\n"
                    " • /end - End conversation. I say to you 'Good bye'\n" 
                    "{} I am happy to speak with you. "),
        "change_language": "Thank you! Your language is english",
        "start_talking": ("Hey hey! {} "
                          "I am <b>Bot</b>. In general I'm speaking in english but "
                          "I also know russian.\nYou can press /RU or write RU for "
                          "russian language or /EN or write EN for english.\n"
                          "I know, that you are <b>{}</b>, you can press a command "
                          "\n/change_nickname and choose new nickname. \nYou also "
                          "can press a command /help and I describe all my commands"),
        "end_talking": "Good bye <b>{}</b>! {}",
        "user_location": "Your coordinate is {}",
        "stop": "Ok. We have finished previous task. You can choose new comand {}.",
        "start_changing_nickname": ("Hello. You would like to change your nickname "
                                    "- <b>{}</b>? Write new nickname."),
        "new_nickname": ("Nice to meet you, <b>{}</b>. If this nickname is incorrect "
                         "you can try to change it again."),
        "keyboard_for_planet": "Choose a planet {}: ",
        "find_constellation": "The planet {} is in the constellation {} today.",
        "next_full_moon": "Hello. {} Next full moon will be {} ",
        "start_wordcount": "Hello. I can count how many words you wrote {}.",
        "count_words_0": ("You don't write words. {} Write something and " 
                          "I can count how many words you wrote to me"),
        "count_words": ("You wrote {} words {}. If you would like to finish "
                        "- choose comand /stop"),
        "guess_number_empty": "You don't right anything {}.",
        "guess_number_integer": "Write an integer {}.",
        "guess_number_lose": "Your number was {}, my number is {}. You win {}.",
        "guess_number_draw": "Your number was {}, my number is {}. It's draw {}.",
        "guess_number_win": "Your number was {}, my number is {}. I win .",
        "arithmetic_operations_empty": "You didn't right anything {}.",
        "arithmetic_operations_()": ("You create a mistake with <b>(</b> or <b>)</b>. "
                                     "Your example has different amount of this symbol"),
        "arithmetic_operations_symbol": ("You can use only integers or symbol: " 
                                         "+-/*(), but you used something else. "
                                         "Try again"),
        "check_user_photo_1": ("I got your pictures and started process of saving "
                               "the picture for future analysis"),
        "check_user_photo_2": ("Your file was saved and I started a process of find "
                               "a human on the picture"),
        "check_user_photo_people": ("Ohhhh, I know it's human! I want to save this "
                                    "picture. Thank you! {}"),
        "check_user_photo_no": ("I didn't find a human on the picture and delited "
                                "it. Thank you for sharing."),
        "cities_game_empty": ("<b>{}</b>, You haven't written anything. {}. Please write "
                          "the name of any city. If you want to finish the game, "
                          "press the command - /stop"),
        "wrong_letter_city": ("Wait, wait, your letter was <b>{}</b>, but you wrote "
                              "a city starting with <b>{}</b>."),
        "wrong_city": ("Please wait, I can't find a city with that name {}. "
                       "Try to choose another city."),
        "repeat_city": ("Please wait, we already wrote this city {}. It's not fair. "
                        "Try it in another city."),
        "cities_game": ("Cool {}! The last lettor of your city was <b>{}</b> and "
                           "my city is {}. \nYou should name a city which start with "
                           "letter - <b>{}</b>\nIf you want to end the game, please "
                           "use the command. - /stop"),
        "city_lose": ("You've won. I do not know the cities which start with "
                         "letter <b>{}</b>"),
        "choose_contry": ("Cool, the rules are very simple - you need to name \n"
                          "any city, then I'll name a city which start with the "
                          "last letter of your city. Then it's your \nturn again "
                          "to name a city which start with the last letter of my "
                          "city. You can't repeat yourself {}. \nLet'go! First of "
                          "all choose a country for game - /Russia or /UK."),
        "start_city_game": "Ok. Let's start. You chose <b>{}</b>. Name first city."

    }}