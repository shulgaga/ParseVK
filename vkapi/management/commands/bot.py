from django.core.management.base import BaseCommand
from telegram import Update, ReplyKeyboardMarkup
from datetime import time
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater, CommandHandler, ConversationHandler, \
    JobQueue
from vkapi.models import Subscription, Profile
from .parse_dialog import parse_category, parse_dialog_keyword, parse_save_category, main_parse, sub, back, greet_parse, \
    search_wall, end_conv
from config import BOT_API_KEY
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)


def log_errors(f):
    def inner(*args, **kwargs):
        global e
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
        raise e

    return inner


def main_keyboard():
    return ReplyKeyboardMarkup([['Найти товар'], ['Отменить подписку']], resize_keyboard=True)


@log_errors
def greet_user(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    update.message.reply_text(f'Привет, {update.message.from_user.full_name}', reply_markup=main_keyboard())


def watch(context):
    for i in Subscription.objects.filter(status=True):
        sub = i.key_word
        all_groups = []
        cat = i.category.group_one
        cat1 = i.category.group_two
        cat2 = i.category.group_three
        all_groups.append(cat)
        all_groups.append(cat1)
        all_groups.append(cat2)
        response = search_wall(all_screen_name_group=all_groups, search_word=sub)
        chat_id = i.tg_user.external_id
        Subscription.objects.filter(status=True).update(main_info=response)
        for post in response:
            context.bot.send_message(chat_id, text='\nДата публикации объявления:\n' + post[
                'date'] + "\n" + "\nОписание объявления:\n" + post['text'] + f"Ссылка в вк:\n{post['wall_url']}")


def podpiska_off(update: Update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    user_profile = Subscription.objects.get(tg_user=p)
    if user_profile.status==False:
        update.message.reply_text('У вас нет подписок!', reply_markup=main_keyboard())
    else:
        Subscription.objects.filter(tg_user=p).update(status=False)
        update.message.reply_text('Подписка отменена')


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        mybot = Updater(BOT_API_KEY, use_context=True)
        logging.info('Start bot')
        dp = mybot.dispatcher
        job_queue = JobQueue()
        job_queue.set_dispatcher(dp)
        t = time(12, 30)
        job_queue.run_daily(callback=watch, time=t)

        dp.add_handler(MessageHandler(Filters.regex('^(Отменить подписку)$'), podpiska_off))
        dp.add_handler(CommandHandler('start', greet_user))
        parse_dialog = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('^(Найти товар)$'), greet_parse),
            ],
            states={
                'category': [
                    MessageHandler(Filters.regex('^(Хорошо|Ввести другие параметры поиска)$'), parse_category),
                    MessageHandler(Filters.regex('^(Назад)$'), end_conv)
                ],
                'save_category': [
                    CommandHandler('back', back),
                    MessageHandler(Filters.regex('^(Авто)$'), parse_save_category)

                ],
                'keyword': [
                    CommandHandler('back', back),
                    MessageHandler(Filters.text, parse_dialog_keyword),
                    MessageHandler(Filters.regex('^(Выйти|Назад)$'), end_conv)

                ],
                'main_parse': [
                    MessageHandler(Filters.regex('^(Далее)$'), main_parse),
                    MessageHandler(Filters.regex('^(Выйти|Назад)$'), end_conv)

                ],
                'sub': [
                    CommandHandler('back', back),
                    MessageHandler(Filters.regex('^(Подписаться на обновления объявлений этого поиска)$'), sub),
                    MessageHandler(Filters.regex('^(Выйти|Назад)$'), end_conv)
                ]
            },
            fallbacks=[]
        )
        dp.add_handler(parse_dialog)
        mybot.start_polling()
        job_queue.start()
        mybot.idle()
