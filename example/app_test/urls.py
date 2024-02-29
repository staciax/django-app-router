import django_app_router

urlpatterns = []

urlpatterns += django_app_router.get_router_urls('app_test.templates')
