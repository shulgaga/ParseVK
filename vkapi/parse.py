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
print(wall_get())

