import requests
import datetime

from config import API_TOKEN, ACCESS_TOKEN, VERSION


def search_wall(group_name, search_word):
    all_info = []
    all_screen_name_group = []
    group_name += ' объявления'

    group = requests.get('https://api.vk.com/method/groups.search',
                         params={
                             'access_token': ACCESS_TOKEN,
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
        sear = requests.get('https://api.vk.com/method/wall.search',
                            params={
                                'access_token': API_TOKEN,
                                'v': VERSION,
                                'domain': i,
                                'count': 10,
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
