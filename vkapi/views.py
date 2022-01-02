from django.http import HttpResponse
import requests
import datetime
from typing import List

# from .models import Main
# import schedule
# import time

from config import API_TOKEN_VK, ACCESS_TOKEN_VK, VERSION, METHOD_GROUP_SEARCH, METHOD_WALL_SEARCH


def search_wall(group_name: str, search_word: str) -> List[str]:
    all_info = []
    all_screen_name_group = []
    group_name += ' объявления'

    group = requests.get(METHOD_GROUP_SEARCH,
                         params={
                             'access_token': ACCESS_TOKEN_VK,
                             'v': VERSION,
                             'q': group_name,
                             'type': 'group',
                             'count': 3,
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
            if post['marked_as_ads'] == 0:
                try:
                    if post['attachments'][0]['type']:
                        img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                        all_info.append(img_url)
                    else:
                        pass
                except KeyError:
                    print('Нет фото')

                text = post['text']
                all_info.append(text)
                timestamp = post['date']
                value = datetime.datetime.fromtimestamp(timestamp)
                value = value.strftime('%Y-%m-%d %H:%M:%S')
                all_info.append(value)
        else:
            pass

    return all_info


def parse_request(request):
    all_info = search_wall('купить_машины', 'bmw')
    return HttpResponse(all_info)


def following(request):
    pass
#     data = search_wall()
#     data.save()
#     schedule.every(30).minutes.do(following)
#     while Main.status is True:
#         schedule.run_pending()
#         time.sleep(1)
#         if Main.status is False:
#             break
#     return HttpResponse(data)
