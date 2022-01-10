from telegram.ext import Updater, MessageHandler, \
    Filters  # Подключаем компонент отвечающий за коммуникацию с сервером проверка
from telegram.ext import CommandHandler  # Подключаем обработчик который реагирует на команды
from telegram import ReplyKeyboardMarkup  # Импорт кнопок
import re
import requests

from config import BOT_API_KEY


def greet_user(update, context):
    my_buttons = ReplyKeyboardMarkup([['Parse оne announcement']], resize_keyboard=True)
    update.message.reply_text(f'Привет {update.message.from_user.full_name}', reply_markup=my_buttons)


def parse(update, context):
    response = requests.get('https://9630-145-255-9-3.ap.ngrok.io')
    discription = response.text
    link_img = re.search(r"https.*", discription).group(0)
    update.message.reply_photo(photo=link_img, caption=discription.replace(link_img, ""))


def main():
    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^Parse оne announcement$'), parse))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
