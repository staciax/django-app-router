<h2 align="center">Django App Router</h2>

<h4 align="center">
    A library for creating routes in Django with a similar structure to
    <a href="https://nextjs.org/docs/app/building-your-application/routing"> Next.js App Router. </a>
</h4>

<p align="center">
    <a href="https://pypi.org/project/django-app-router/">
        <img
            alt="Releases"
            src="https://img.shields.io/github/release/staciax/django-app-router.svg?style=for-the-badge&logo=github&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"
        />
    </a>
    <a href="https://github.com/staciax/django-app-router/stargazers">
        <img
            alt="Stars"
            src="https://img.shields.io/github/stars/staciax/django-app-router?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"
        />
    </a>
    <a href="https://github.com/staciax/django-app-router/issues">
        <img
            alt="Issues"
            src="https://img.shields.io/github/issues/staciax/django-app-router?colorA=363a4f&colorB=f5a97f&style=for-the-badge"
        />
    </a>
    <a href="https://github.com/staciax/django-app-router/contributors">
        <img
            slt="Contributors"
            src="https://img.shields.io/github/contributors/staciax/django-app-router?colorA=363a4f&colorB=a6da95&style=for-the-badge"
        />
    </a>
</p>

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
