from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

name = 'home'


def page(request: HttpRequest) -> HttpResponse:
    return render(request, 'page.html')
