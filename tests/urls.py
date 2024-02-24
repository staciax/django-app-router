from pathlib import Path

import django_app_router

urlpatterns = []

urlpatterns += django_app_router.init(
    Path(__file__).resolve().parent / 'templates',
)
