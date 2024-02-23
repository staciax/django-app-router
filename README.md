# django app router
A modern, easy to use, and powerful router for Django apps. Inspired by the Next.js app router.

![Django App Router](https://raw.githubusercontent.com/staciax/django-app-router/master/docs/django-app-router-800.gif)

## Installing
Python 3.12 or higher is required

Windows: <br>
```
$ pip install -U django-app-router
```
Linux/MacOS:
```
$ python3 -m pip install -U django-app-router
```

## Quick Example
<app_name>/urls.py:
```python
from pathlib import Path

import django_app_router

urlpatterns = []

urlpatterns += django_app_router.get_urlpatterns(
    # The path to the templates folder
    Path(__file__).resolve().parent / 'templates',
)
```
App folder structure:
```
app
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── templates
│   ├── page.html
│   ├── page.py
│   ├── info
│   │   └── page.py
│   └── user
│       └── [user_id]
│           ├── page.html
│           └── page.py
├── tests.py
├── urls.py
└── views.py
```
Above example will generate the following urlpatterns (approximately):
```
urlpatterns = [
    path('', views.page, name='home'),
    path('info/', views.info_page, name='info'),
    path('/user/<int:user_id>/', views.user_page, name='get_user'),
]
```

You can see the full example in the [example](example) folder.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.