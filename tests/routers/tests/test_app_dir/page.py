from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest) -> HttpResponse:
    """test_app_dir"""
    return render(request, 'tests/test_app_dir/page.html')
