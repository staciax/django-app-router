from django.urls import include, path

from django_app_router import routers

router = routers.AppRouter()
router.add_app('app_test')

urlpatterns = [
    path('', include(router.urls)),
]
