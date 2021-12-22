from django.shortcuts import render
from .parse import html
from django.http import HttpResponse
from .models import Main
import schedule
import time


def parse_request(request):
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




