from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render

name = 'get_user'


def page(request: HttpRequest, user_id: int) -> HttpResponse:
    context = {
        'user_id': user_id,
    }
    return render(request, 'user/[user_id]/page.html', context)
