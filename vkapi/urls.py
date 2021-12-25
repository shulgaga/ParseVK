from django.urls import path
from . import views

urlpatterns = [
    path('get_vk/', views.parse_request),
    path('schedule', views.following)
]
