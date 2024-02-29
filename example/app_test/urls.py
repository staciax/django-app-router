import django_app_router

urlpatterns = []

urlpatterns += django_app_router.get_view_urls('app_test.templates')
