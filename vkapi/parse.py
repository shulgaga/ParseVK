import requests
import datetime


# def search_group():
#     API_KEY = '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463'
#     version = '5.131'
#     q = str(input('Введите название группы: '))
#     all_group = []
#
#     group = requests.get('https://api.vk.com/method/groups.search',
#                          params={
#                              'access_token': API_KEY,
#                              'v': version,
#                              'q': q,
#                              'market': 1,
#                              'sort': 6,
#                              'country_id': 1,
#                              'count': 3
#                          }
#                          )
#     all_group.extend(group)
#     print(all_group)
#     return all_group


def search_wall():
    API_KEY = '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463'
    version = '5.131'
    domain = 'autosale_rus'
    offset = 0
    query = str(input('Введите нужное слово: '))
    owners_only = 1
    all_post = []
    all_info = []

    sear = requests.get('https://api.vk.com/method/wall.search',
                        params={
                            'access_token': API_KEY,
                            'v': version,
                            'domain': domain,
                            'count': 10,
                            'offset': offset,
                            'query': query,
                            'owners_only': owners_only
                        }
                        )
    data = sear.json()['response']['items']
    all_post.extend(data)

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


# html2 = search_group()
html = search_wall()
