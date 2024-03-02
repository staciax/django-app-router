from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest) -> HttpResponse:
    """test_about"""
    return render(request, '(test_group)/about/page.html')
