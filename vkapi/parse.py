import requests
import datetime


def search_wall():
    access_token = '4a8bc3a1cef6e1a959d97d532fda7f1a37faee693d6ad7f85691b906b3aedad81adef33cbaaaf433e5feb'
    api_token = '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463'
    version = '5.131'
    q = str(input('Введите имя групп: '))
    query = str(input('Введите нужное слово: '))
    domain = 'autosale_rus'
    all_info = []
    all_screen_name_group = []

    group = requests.get('https://api.vk.com/method/groups.search',
                         params={
                             'access_token': access_token,
                             'v': version,
                             'q': q,
                             'country_id': 1,
                             'type': 'group',
                             'count': 3,
                             'sort': 6,
                             'market': 1
                         }).json()['response']['items']
    for i in group:
        all_screen_name_group.append(i['screen_name'])
    print(all_screen_name_group)

    for i in all_screen_name_group:
        sear = requests.get('https://api.vk.com/method/wall.search',
                            params={
                                'access_token': api_token,
                                'v': version,
                                'domain': i,
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
