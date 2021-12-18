from django.shortcuts import render
from .parse import html
from django.http import HttpResponse


def parse_request(request):
    return HttpResponse(html)

