import requests
import datetime
from typing import List
from django.contrib.auth.models import User
from django.shortcuts import render
#from .parse import html
from django.http import HttpResponse, HttpRequest
from .models import Subscription
from .parse import search_wall
import json
import schedule
import time

# from .models import Main
# import schedule
# import time

from config import API_TOKEN_VK, ACCESS_TOKEN_VK, VERSION, METHOD_GROUP_SEARCH, METHOD_WALL_SEARCH


def search_wall(group_name: str, search_word: str) -> List[str]:
    """Функция отпраляет запрос по поиску групп в вк.
    После, циклом, добавляет нужное кол-во screen_name-групп в пустой список.
    И далее отправляет по каждой найденной группе циклом запрос на нужные нам объявления.
    Далее всю нужную информацию добавялет в новый пустой список и вот уже этот список нам возвращает.
    """
    all_info = []
    all_screen_name_group = []
    group_name += ' объявления'

    group = requests.get(METHOD_GROUP_SEARCH,
                         params={
                             'access_token': ACCESS_TOKEN_VK,
                             'v': VERSION,
                             'q': group_name,
                             'type': 'group',
                             'count': 1,
                             'sort': 6,
                         }).json()['response']['items']
    for i in group:
        all_screen_name_group.append(i['screen_name'])
    print(all_screen_name_group)

    for i in all_screen_name_group:
        sear = requests.get(METHOD_WALL_SEARCH,
                            params={
                                'access_token': API_TOKEN_VK,
                                'v': VERSION,
                                'domain': i,
                                'count': 1,
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


def edit_info(request):#update parsing information
    data = json.loads(request.body)
    user_name = data.get('user_name')
    user = User.objects.get(username=user_name)
    main_info = data.get('main_info')
    edit = Subscription.objects.filter(tg_user=user).update(main_info=main_info)
    return HttpResponse()


def following(request):
    x = Subscription.objects.get(status=True)
    p = edit_info(request)
    schedule.every(30).seconds.do(following)
    while x is True:
        schedule.run_pending()
        time.sleep(1)
        if x is False:
            break
    return HttpResponse(x)




