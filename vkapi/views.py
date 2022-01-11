from django.contrib.auth.models import User
from django.shortcuts import render
#from .parse import html
from django.http import HttpResponse, HttpRequest
from .models import Subscription
from .parse import search_wall
import json
import schedule
import time



def parse_request(request):
    return HttpResponse()

def create_user(request): #create user in DB
    data = json.loads(request.body)
    user_name = data.get('user_name')
    user = User.objects.get(username=user_name)
    status = data.get('status')
    category = data.get('category')
    main_info = data.get('main_info')
    p = Subscription.objects.create(tg_user=user, status=status, category=category, main_info=main_info)
    return HttpResponse()

def edit_info(request):#update parsing information
    data = json.loads(request.body)
    user_name = data.get('user_name')
    user = User.objects.get(username=user_name)
    main_info = data.get('main_info')
    edit = Subscription.objects.filter(tg_user=user).update(main_info=main_info)
    return HttpResponse()



def following(request):
    x = Subscription.objects.get(status=True)
    p = edit_info(request)
    schedule.every(30).seconds.do(following)
    while x is True:
        schedule.run_pending()
        time.sleep(1)
        if x is False:
            break
    return HttpResponse(x)




