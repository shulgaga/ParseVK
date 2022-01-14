from django.urls import path
from . import views

urlpatterns = [
    path('', views.parse_request),
    path('schedule', views.following),
    path('create_user', views.create_user),
    path('update_info', views.edit_info),
    path('subscription', views.following)
]
