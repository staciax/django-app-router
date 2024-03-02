from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest, slug: str) -> HttpResponse:
    """test_slug"""
    context = {'slug': slug}
    return render(request, 'test_slug/[slug]/page.html', context)
