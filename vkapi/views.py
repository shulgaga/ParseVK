from django.shortcuts import render
import requests
import datetime

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
    for post in data:
        try:
            if post['attachments'][0]['type']:
                img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                img_url = 'pass'
        except:
            pass
        text = post['text']
        timestamp = post['date']
        value = datetime.datetime.fromtimestamp(timestamp)
        value = value.strftime('%Y-%m-%d %H:%M:%S')
        if post['marked_as_ads'] == 0:
            return text, value, img_url

data = wall_get()
print(file_writer(data))

