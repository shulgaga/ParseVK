from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_wall),
    path('create_user', views.create_user),
    path('update_info', views.edit_info),
    path('scheduler', views.sch)
]
