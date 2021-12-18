import requests
import datetime
import  json

import vkapi.token


def search_group():
    access_token = vkapi.token.access_token
    version = '5.131'
    q = str(input('Введите имя групп: '))
    group = requests.get('https://api.vk.com/method/groups.search',
                         params={
                             'access_token': access_token,
                             'v': version,
                             'q': q,
                             'type': 'group',
                             'count': 1,
                             'sort': 6,
                             'market': 1
                         }).json()['response']['items']
    print(group)
    d = json.loads(*group)
    print(d)


search_group()


def search_wall():
    access_token = '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463'
    version = '5.131'
    domain = 'autosale_rus'
    query = str(input('Введите нужное слово: '))
    all_info = []

    sear = requests.get('https://api.vk.com/method/wall.search',
                        params={
                            'access_token': access_token,
                            'v': version,
                            'domain': domain,
                            'count': 10,
                            'offset': 0,
                            'query': query,
                            'owners_only': 1
                        }
                        )
    data = sear.json()['response']['items']

    for post in data:
        try:
            if post['attachments'][0]['type']:
                img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                all_info.append(img_url)
            else:
                return 'pass'
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


html = search_wall()
