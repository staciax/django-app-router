from django.http.request import HttpRequest
from django.http.response import HttpResponse

name = 'info'


def page(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<h1>info</h1>')
