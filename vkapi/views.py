from django.shortcuts import render
from .parse import wall_get, file_writer
from django.http import HttpResponse
from .models import Main
import schedule
import time


def parse_request(request):
    data = wall_get()
    html = file_writer(data)
    return HttpResponse(html)

def following(request):
    data = wall_get()
    data.save()
    schedule.every(30).minutes.do(following)
    while Main.status is True:
        schedule.run_pending()
        time.sleep(1)
        if Main.status is False:
            break
    return HttpResponse(data)




