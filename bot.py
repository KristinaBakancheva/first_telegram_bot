import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

TOKEN = settings.API_KEY

logging.basicConfig(filename='bot.log', level = logging.INFO) # логирование при ошибке информационных сообщений

#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME , 'password': settings.PROXY_PASSWORD}} 
# прокси для обхода блокировки телеграмм в РФ

def hello_user(update, context): # update - что прешло от платформы телеграм, context - используется для отправки информации платформе, а не user
    print('Вызван старт')
    update.message.reply_text('Здравствуй пользователь!')

def talking(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    
    mybot = Updater(TOKEN, use_context=True)#, request_kwargs = PROXY)

    dp = mybot.dispatcher # просто для сохращения вводим переменную dp
    dp.add_handler(CommandHandler('start', hello_user)) # добавим обработчик CommandHandler который будет реагировать на коману start функцией hello_user 
    dp.add_handler(MessageHandler(Filters.text, talking))


    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()



if __name__ == '__main__':
    main()

