import logging  # Подключаем логгирование

from telegram.ext import Updater  # Подключаем компонент отвечающий за коммуникацию с сервером проверка
from telegram.ext import CommandHandler  # Подключаем обработчик который реагирует на команды
from telegram.ext import MessageHandler  # Подключаем обработчик который реагирует на любые сообщения(много типов)
from telegram.ext import Filters  # Импорт фильтров
from telegram import ReplyKeyboardMarkup  # Импорт клавиатуры

from config import TOKEN

logging.basicConfig(filename="bot.log", level=logging.INFO)


def greet_user(update, context):
    my_buttons = ReplyKeyboardMarkup([['Parse']], resize_keyboard=True)
    update.message.reply_text(f'Привет {update.message.from_user.full_name}', reply_markup=my_buttons)
    logging.info(f'{update.message.from_user.full_name} подключился')


def help_user(update, context):
    update.message.reply_text('Далее тут будет информация о боте')
    logging.info(f'{update.message.from_user.full_name} нажал команду /help')


def talk_to_me(update, context):
    text = '''Я не знаю, что с этим делать. Я просто напомню, что есть меню'''
    update.message.reply_text(text)


def main():
    mybot = Updater(TOKEN, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    # dp.add_handler(MessageHandler(Filters.regex('^(Parse)&'), )
    dp.add_handler(MessageHandler(Filters.all, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
