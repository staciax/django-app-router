from django.http.request import HttpRequest
from django.http.response import HttpResponse


def page(request: HttpRequest) -> HttpResponse:
    """info"""
    return HttpResponse('<h1>info</h1>'.encode())
