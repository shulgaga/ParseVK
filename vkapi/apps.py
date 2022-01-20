from django.apps import AppConfig
from telegram import Update


class VkapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vkapi'
