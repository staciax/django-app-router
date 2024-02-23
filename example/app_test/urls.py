from pathlib import Path

import django_app_router

urlpatterns = []

urlpatterns += django_app_router.get_urlpatterns(
    Path(__file__).resolve().parent / 'templates',
)

print(urlpatterns)