from telegram.ext import Updater, MessageHandler, Filters  # Подключаем компонент отвечающий за коммуникацию с сервером проверка
from telegram.ext import CommandHandler  # Подключаем обработчик который реагирует на команды
from telegram import ReplyKeyboardMarkup  # Импорт кнопок

from config import BOT_API_KEY

import requests


def greet_user(update, context):
    my_buttons = ReplyKeyboardMarkup([['Parse оne announcement']], resize_keyboard=True)
    update.message.reply_text(f'Привет {update.message.from_user.full_name}', reply_markup=my_buttons)


def parse(update, context):
    response = requests.get('https://f11f-145-255-9-3.ap.ngrok.io')
    update.message.reply_text(response.text)


def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Parse оne announcement)$'), parse))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
