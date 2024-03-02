import django_app_router

router = django_app_router.AppRouter()
router.add_app('tests')

urlpatterns = []

urlpatterns += router.urls
