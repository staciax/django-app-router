import pytest
from django.http.response import HttpResponse
from django.test.client import Client


@pytest.mark.urls('tests.urls')
def test_view_action(client: Client):
    response = client.get('/view_action/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'view-action' in response.content


@pytest.mark.urls('tests.urls')
def test_view_action_get(client: Client):
    response = client.get('/view_action_get/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'view-action-get' in response.content


@pytest.mark.urls('tests.urls')
def test_view_action_post(client: Client):
    response = client.post('/view_action_post/')

    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'view-action-post' in response.content

    response = client.get('/view_action_post/')
    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 405
