# django app router

A modern, easy to use, and powerful router for Django apps. Inspired by the Next.js app router.

<!-- ![Django App Router](https://raw.githubusercontent.com/staciax/django-app-router/master/docs/django-app-router-800.gif) -->

## Features

- [x] Dynamic routing
- [x] Nested routing
- [x] Route parameters
- [x] Route groups

## Requirements

- Python 3.8+
- Django 4.2+

## Installing

Windows: <br>

```
$ pip install -U django-app-router
```

Linux/MacOS:

```
$ python3 -m pip install -U django-app-router
```

## Setup and Usage

urls.py:

```python
from django_app_router import routers

router = routers.AppRouter()
router.add_app('your_app') # app directory name

urlpatterns = [
    # ...
]

urlpatterns += router.urls
```

Alternatively, you can use the `include` function. like this:

```python
urlpatterns = [
    # ...
    path('', include(router.urls)),
]
```

## Example

for example, define a route with the file `page.py` in the `routers` folder:

```python
from django.shortcuts import render

def page(request):
    """home"""
    # You can also name the page
    # path(..., ..., name='home')

    return render(request, 'page.html')

```

| Route                           | Example URL | params        |
| ------------------------------- | ----------- | ------------- |
| `routers/page.py`               | `/`         | `{}`          |
| `routers/info/page.py`          | `/info/`    | `{}`          |
| `routers/(group)/about/page.py` | `/about/`   | `{}`          |
| `routers/user/[slug]/page.py`   | `/user/1/`  | `{'slug': 1}` |

### Example folder structure

```
your_app
├── migrations
│   └── __init__.py
├── routers
│   ├── (auth)
│   │   ├── login
│   │   │   ├── page.html
│   │   │   └── page.py
│   │   └── register
│   │       ├── page.html
│   │       └── page.py
│   ├── info
│   │   └── page.py
│   ├── user
│   │   └── [user_id]
│   │       ├── page.html
│   │       └── page.py
│   ├── layout.html
│   ├── page.html
│   └── page.py
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

You can see the full example in the [example](example) folder.

## Notes

if you have `.html` files in the `routers` directory. ensure that the `DIRS` setting in the `TEMPLATES` setting includes the `routers` directory.

```python
TEMPLATES = [
    {
        # ...
        'DIRS': [
            # any other directories
            BASE_DIR / 'your_app' / 'routers',
        ],
        # ...
    },
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
