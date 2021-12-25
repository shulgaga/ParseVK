import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
# from .models import Main
# import schedule
# import time
# from parse import html

from vkapi.parse import search_wall


@api_view(['GET'])
def parse_request(request):
    json_data = json.loads(request.body)
    all_info = search_wall(group_name=json_data['group_name'], search_word=json_data['search_word'])
    return HttpResponse(all_info)


def following(request):
    pass
    # data = wall_get()
    # data.save()
    # schedule.every(30).minutes.do(following)
    # while Main.status is True:
    #     schedule.run_pending()
    #     time.sleep(1)
    #     if Main.status is False:
    #         break
    # return HttpResponse(data)
