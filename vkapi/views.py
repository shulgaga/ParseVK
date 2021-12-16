from django.shortcuts import render
from .parse import wall_get, file_writer
from django.http import HttpResponse


def parse_request(request):
    data = wall_get()
    html = file_writer(data)
    return HttpResponse(html)


