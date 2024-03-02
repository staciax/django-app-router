from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def page(request: HttpRequest, user_id: int) -> HttpResponse:
    """get_user"""
    context = {
        'user_id': user_id,
    }
    return render(request, 'user/[user_id]/page.html', context)
