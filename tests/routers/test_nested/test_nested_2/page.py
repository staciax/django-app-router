from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest) -> HttpResponse:
    """test_nested_2"""
    return render(request, 'test_nested/test_nested_2/page.html')
