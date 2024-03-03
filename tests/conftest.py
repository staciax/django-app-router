import pytest

from django_app_router import routers


@pytest.fixture
def router():
    router = routers.AppRouter()
    return router
