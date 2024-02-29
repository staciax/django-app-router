from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

from django_app_router.view_actions import get, post, view_action


@view_action('view_action/', name='action-test')
def test_lazy_view(request: HttpRequest) -> HttpResponse:
    context = {'test': 'view-action'}
    return render(request, 'test_view_actions/page.html', context)


@get('view_action_get/', name='action-test-get')
def test_lazy_get(request: HttpRequest) -> HttpResponse:
    context = {'test': 'view-action-get'}
    return render(request, 'test_view_actions/page.html', context)


@post('view_action_post/', name='action-test-post')
def test_lazy_post(request: HttpRequest) -> HttpResponse:
    context = {'test': 'view-action-post'}
    return render(request, 'test_view_actions/page.html', context)
