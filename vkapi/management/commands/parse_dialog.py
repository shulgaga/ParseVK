from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from vkapi.models import Subscription, Profile
import requests
import datetime


def search_wall(all_screen_name_group: list, search_word: str):
    """Функция отпраляет запрос по поиску групп в вк.
    После, циклом, добавляет нужное кол-во screen_name-групп в пустой список.
    И далее отправляет по каждой найденной группе циклом запрос на нужные нам объявления.
    Далее всю нужную информацию добавялет в новый пустой список и вот уже этот список нам возвращает.
    """
    all_info = []
    for i in all_screen_name_group:
        sear = requests.get('https://api.vk.com/method/wall.search',
                            params={
                                'access_token': '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463',
                                'v': '5.131',
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
    return ReplyKeyboardMarkup([['Найти товар']], resize_keyboard=True)


def greet_parse(update, context):
    update.message.reply_text('Чтобы найти товар, я задам несколько вопросов',
                              reply_markup=ReplyKeyboardMarkup([['Хорошо'], ['Назад']], resize_keyboard=True))
    return 'category'


def parse_category(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    sub = Subscription.objects.get_or_create(tg_user=p)
    update.message.reply_text('Что вы ищете? Выберите категорию',
                              reply_markup=ReplyKeyboardMarkup([['Авто']], resize_keyboard=True,
                                                               one_time_keyboard=True))
    return 'save_category'


def parse_save_category(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    save = Subscription.objects.filter(tg_user=p).update(category=1)
    update.message.reply_text("Введите ключевое слово для поиска")
    return 'keyword'


def parse_dialog_keyword(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    key = update.message.text
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    c = Subscription.objects.get(tg_user=p)
    cc = c.category.category_name
    sub = Subscription.objects.filter(tg_user=p).update(key_word=key)
    update.message.reply_text(
        f'Проверьте внесенные данные: категория - {cc}, ключевое слово - {key}\nЕсли нашли ошибку можете вернуться назад в меню',
        reply_markup=ReplyKeyboardMarkup([['Далее'], ['Назад']], resize_keyboard=True))
    return 'main_parse'


def main_parse(update, context):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    key = update.message.text
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
    main_info_update = Subscription.objects.filter(tg_user=p).update(main_info=response)
    for post in response:
        update.message.reply_text(
            text='\nДата публикации объявления:\n' + post['date'] + "\n" + "\nОписание объявления:\n" + post[
                'text'] + f"Ссылка в вк:\n{post['wall_url']}")
    update.message.reply_text('Отлично, что дальше? Можете задать другие параметры поиска /back',
                              reply_markup=ReplyKeyboardMarkup(
                                  [['Подписаться на обновления объявлений этого поиска'], ['Назад']],
                                  resize_keyboard=True))
    return 'sub'


def back(update, context):
    update.message.reply_text('Подтвердите действия',
                              reply_markup=ReplyKeyboardMarkup([['Ввести другие параметры поиска'], ['Выйти']]))
    return 'category'


def sub(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    defaults = update.message.from_user.username
    p = Profile.objects.get(external_id=chat_id, name=defaults)
    sub = Subscription.objects.filter(tg_user=p).update(status=True)
    update.message.reply_text(
        'Подписка успешно оформлена!\n Каждые полчаса я буду проверять наличие новых объявлений в заданном поиске и присылать вам новые',
        reply_markup=parse_main_keyboard())
    '''Тут запуск шедулера который каждый 30 минут отправляет парсинг в базу и выдает пользователю'''
    return ConversationHandler.END


def end_conv(update, context):
    update.message.reply_text('Вернулись назад', reply_markup=parse_main_keyboard())
    return ConversationHandler.END
