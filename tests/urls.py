import django_app_router

urlpatterns = []

urlpatterns += django_app_router.get_router_urls('tests.templates')

urlpatterns += django_app_router.get_view_urls('tests.views')
