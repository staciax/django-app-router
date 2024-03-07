import django_app_router

router = django_app_router.AppRouter()
router.include_app('tests', app_dir=False)
router.include_app('tests', app_dir=True)

urlpatterns = []

urlpatterns += router.urls
