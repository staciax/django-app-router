from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest) -> HttpResponse:
    """test_ignore"""
    return render(request, 'page.html')
