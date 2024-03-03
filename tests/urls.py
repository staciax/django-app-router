import django_app_router

router = django_app_router.AppRouter()
router.include_app('tests')

urlpatterns = []

urlpatterns += router.urls
