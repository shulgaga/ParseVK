from django.contrib import admin
from .models import Subscription, Profile, Message, Category


admin.site.register(Subscription)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Category)



