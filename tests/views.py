from django.http.request import HttpRequest
from django.http.response import HttpResponse

from django_app_router.lazy_view import get, post, view


@view('lazy_view/', name='lazy-view')
def test_lazy_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b'<h1>lazy view</h1>')


@get('lazy_get/', name='lazy-get')
def test_lazy_get(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b'<h1>lazy get</h1>')


@post('lazy_post/', name='lazy-post')
def test_lazy_post(request: HttpRequest) -> HttpResponse:
    return HttpResponse(b'<h1>lazy post</h1>')
