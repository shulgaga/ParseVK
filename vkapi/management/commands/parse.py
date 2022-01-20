import requests




def search_wall(update, context, group_name: str, search_word: str):
    """Функция отпраляет запрос по поиску групп в вк.
    После, циклом, добавляет нужное кол-во screen_name-групп в пустой список.
    И далее отправляет по каждой найденной группе циклом запрос на нужные нам объявления.
    Далее всю нужную информацию добавялет в новый пустой список и вот уже этот список нам возвращает.
    """
    all_info = []

    sear = requests.get('https://api.vk.com/method/wall.search',
                        params={
                            'access_token': '6849ded36849ded36849ded3066833a5ca668496849ded309f148be98d5788daa04f463',
                             'v': '5.131',
                            'domain': group_name,
                            'count': 1,
                            'offset': 1,
                            'query': search_word
                            }
                        )
    for data in sear.json()['response']['items']:
        text_data = data['text']
        img_data = data['attachments'][0]['photo']['sizes'][-1]['url']
        all_info.append({'text': text_data,
                         'img_url': img_data,
                         })
    print(all_info)
    for post in all_info:
        update.message.reply_photo(photo=post['img_url'], caption=post['text'])


