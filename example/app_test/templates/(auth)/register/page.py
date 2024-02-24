from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest) -> HttpResponse:
    """register"""
    return render(request, '(auth)/register/page.html')
