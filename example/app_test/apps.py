from django.apps import AppConfig


class AppTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # pyright: ignore[reportAssignmentType]
    name = 'app_test'
