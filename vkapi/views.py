import requests
from typing import List
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from .models import Subscription
import json
from apscheduler.schedulers.background import BackgroundScheduler
from config import API_TOKEN_VK, ACCESS_TOKEN_VK, VERSION, METHOD_GROUP_SEARCH, METHOD_WALL_SEARCH


def search_wall(group_name: str, search_word: str) -> List[str]:
    """Функция отпраляет запрос по поиску групп в вк.
    После, циклом, добавляет нужное кол-во screen_name-групп в пустой список.
    И далее отправляет по каждой найденной группе циклом запрос на нужные нам объявления.
    Далее всю нужную информацию добавялет в новый пустой список и вот уже этот список нам возвращает.
    """
    all_info = []
    all_screen_name_group = []

    group = requests.get('https://api.vk.com/method/groups.search',
                         params={
                             'access_token': '4a8bc3a1cef6e1a959d97d532fda7f1a37faee693d6ad7f85691b906b3aedad81adef33cbaaaf433e5feb',
                             'v': '5.131',
                             'q': group_name,
                             'type': 'group',
                             'count': 2,
                             'sort': 6,
                         }).json()['response']['items']
    for i in group:
        all_screen_name_group.append(i['screen_name'])
    print(all_screen_name_group)

    for i in all_screen_name_group:
        sear = requests.get('https://api.vk.com/method/wall.search',
                            params={
                                'access_token': '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463',
                                'v': '5.131',
                                'domain': i,
                                'count': 2,
                                'offset': 0,
                                'query': search_word,
                                'owners_only': 1
                            }
                            )

        data = sear.json()['response']['items']

        for post in data:
            text = post['text'] + '\n'
            all_info.append(text)
            all_info.append("\n")
            try:
                if post['attachments'][0]['type'] not in all_info:
                    url_photo = post['attachments'][-1]['photo']['sizes'][-1]['url']
                    all_info.append(url_photo)
                else:
                    print('pass')
            except KeyError:
                print('Нет фото')
    return all_info


def create_user(request): #create user in DB
    data = json.loads(request.body)
    user_name = data.get('user_name')
    user = User.objects.get(username=user_name)
    status = data.get('status')
    category = data.get('category')
    main_info = data.get('main_info')
    p = Subscription.objects.create(tg_user=user, status=status, category=category, main_info=main_info)
    return HttpResponse()


def edit_info(request):
    ''' EDITING PARSING INFORMATION '''
    data = json.loads(request.body)
    user_name = data.get('user_name')
    user = User.objects.get(username=user_name)
    main_info = data.get('main_info')
    edit = Subscription.objects.filter(tg_user=user).update(main_info=main_info)
    return HttpResponse()


def sch():
    ''' STARTS SCHEDULER '''
    scheduler = BackgroundScheduler(timezone='Europe/Moscow')
    scheduler.add_job(edit_info_off, 'interval', seconds=50)
    scheduler.start()


def edit_info_off():
    user = User.objects.get(username='user')
    edit = Subscription.objects.filter(tg_user=user).update(main_info=search_wall('auto', 'bmv'))
    return

