import requests
import datetime
import schedule
import time
from .models import Main

API_KEY = '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463'
v = '5.131'
domain = 'autosale_rus'
def wall_get():
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': API_KEY,
                                'v': v,
                                'domain': domain,
                                'count': 100,
                                'offset': 1
                            }
                            )
    data = response.json()['response']['items']
    return data


def file_writer(data):
    all_info = []
    for post in data:
        if post['marked_as_ads'] == 0:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                    all_info.append(img_url)
                else:
                    img_url = 'pass'
            except:
                pass
            text = post['text']
            all_info.append(text)
            timestamp = post['date']
            value = datetime.datetime.fromtimestamp(timestamp)
            value = value.strftime('%Y-%m-%d %H:%M:%S')
            all_info.append(value)
        else:
            pass
    return all_info





if __name__=='__main__':
    following()