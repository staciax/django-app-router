from django.urls import include, path

import django_app_router

router = django_app_router.AppRouter()
router.add_app('app_test')

urlpatterns = [
    path('', include(router.urls)),
]
