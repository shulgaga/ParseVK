from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from vkapi.models import Subscription, Profile
import requests
import datetime
import os



def search_wall(all_screen_name_group: list, search_word: str):
    """
    Функция отправляет запрос в группы на нужные нам объявления.
    Далее всю нужную информацию добавялет в пустой список и возвращает нам его.

    :param all_screen_name_group: list
    :param search_word: str
    :return: список словарей
    """
    all_info: list = []
    for i in all_screen_name_group:
        sear = requests.get("https://api.vk.com/method/wall.search",
                            params={
                                'access_token': os.getenv('ACCESS_TOKEN_VK'),
                                'v': "5.131",
                                'domain': i,
                                'count': 2,
                                'offset': 1,
                                'query': search_word
                            })
        for data in sear.json()['response']['items']:
            text_data = data['text']
            id_data = data['id']
            from_id = data['from_id']
            timestamp = data['date']
            value = datetime.datetime.fromtimestamp(timestamp)
            value = value.strftime('%Y-%m-%d %H:%M:%S')
            wall_url = f'https://vk.com/{i}?w=wall{from_id}_{id_data}'
            all_info.append({'text': text_data,
                             'wall_url': wall_url,
                             'date': value,
                             })
    return all_info


def parse_main_keyboard():
    return ReplyKeyboardMarkup([['Найти товар'], ['Отменить подписку']], resize_keyboard=True)


def greet_parse(update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    Subscription.objects.get_or_create(tg_user=p)
    update.message.reply_text('Чтобы найти товар, я задам несколько вопросов',
                              reply_markup=ReplyKeyboardMarkup([['Хорошо'], ['Назад']], resize_keyboard=True))
    return 'category'


def parse_category(update: Update, _):
    update.message.reply_text('Что вы ищете? Выберите категорию',
                              reply_markup=ReplyKeyboardMarkup([['Авто']], resize_keyboard=True,
                                                               one_time_keyboard=True))
    return 'save_category'


def parse_save_category(update: Update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    key = update.message.text
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    if key == 'Авто':
        Subscription.objects.filter(tg_user=p).update(category=1)
    update.message.reply_text("Введите ключевое слово для поиска")
    return 'keyword'


def parse_dialog_keyword(update: Update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    key = update.message.text
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    Subscription.objects.filter(tg_user=p).update(key_word=key)
    c = Subscription.objects.get(tg_user=p)
    cc = c.category.category_name
    update.message.reply_text(
        f'Проверьте внесенные данные: категория - {cc}, ключевое слово - {key}\nЕсли нашли ошибку можете вернуться назад в меню',
        reply_markup=ReplyKeyboardMarkup([['Далее'], ['Назад']], resize_keyboard=True)
    )
    return 'main_parse'


def main_parse(update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    sub = Subscription.objects.get(tg_user=p)
    sub = sub.key_word
    all_groups = []
    cat = Subscription.objects.get(tg_user=p)
    cat0 = cat.category.group_one
    cat1 = cat.category.group_two
    cat2 = cat.category.group_three
    all_groups.append(cat0)
    all_groups.append(cat1)
    all_groups.append(cat2)
    response = search_wall(all_screen_name_group=all_groups, search_word=sub)
    if response == []:
        update.message.reply_text('Ничего не нашел, проверьте данные и введите еще раз /back',
                                  reply_markup=ReplyKeyboardMarkup([['Назад']], resize_keyboard=True))
    else:
        Subscription.objects.filter(tg_user=p).update(main_info=response)
        for post in response:
            update.message.reply_text(
                text='\nДата публикации объявления:\n' + post['date'] + "\n" + "\nОписание объявления:\n" +
                     post['text'] + f"Ссылка в вк:\n{post['wall_url']}")
        update.message.reply_text('Отлично, что дальше? Можете задать другие параметры поиска /back',
                                  reply_markup=ReplyKeyboardMarkup(
                                      [['Подписаться на обновления объявлений этого поиска'], ['Назад']],
                                      resize_keyboard=True))
    return 'sub'


def back(update, _):
    update.message.reply_text('Подтвердите действия',
                              reply_markup=ReplyKeyboardMarkup([['Ввести другие параметры поиска'], ['Выйти']]))
    return 'category'


def sub(update: Update, _):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    Subscription.objects.filter(tg_user=p).update(status=True)
    update.message.reply_text(
        'Подписка успешно оформлена!\n Каждый день я буду проверять наличие новых объявлений в заданном поиске и присылать вам новые',
        reply_markup=parse_main_keyboard())
    '''Тут запуск шедулера который каждый 30 минут отправляет парсинг в базу и выдает пользователю'''
    return ConversationHandler.END


def end_conv(update, _):
    update.message.reply_text('Вернулись назад', reply_markup=parse_main_keyboard())
    return ConversationHandler.END
