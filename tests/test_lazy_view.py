import pytest
from django.http.response import HttpResponse
from django.test.client import Client


@pytest.mark.urls('tests.urls')
def test_lazy_view(client: Client):
    response = client.get('/lazy_view/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>lazy view</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_lazy_get(client: Client):
    response = client.get('/lazy_get/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>lazy get</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_lazy_post(client: Client):
    response = client.post('/lazy_post/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>lazy post</h1>' in response.content

    response = client.get('/lazy_post/')
    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 405
