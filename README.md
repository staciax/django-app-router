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

## Setup and Usage

<app_name>/urls.py:

```python
from pathlib import Path

import django_app_router

urlpatterns = [
    # Your other urlpatterns
]

urlpatterns += django_app_router.init(
    # The path to the templates folder
    Path(__file__).resolve().parent / 'templates',
)
```

## Example

for example, you have a page in the app folder:

```python
from django.shortcuts import render

def page(request):
    """home"""
    # You can also name the page
    # path(..., ..., name='home')

    return render(request, 'page.html')

```

| Route                              | Example URL | params           |
| ---------------------------------- | ----------- | ---------------- |
| `templates/page.py`                | `/`         | ` `              |
| `templates/info/page.py`           | `/info`     | ` `              |
| `templates/user/[user_id]/page.py` | `/user/1`   | `{'user_id': 1}` |
| `templates/(group)/login/page.py`  | `/login`    |                  |

### Example folder structure

```
app
├── migrations
│   └── __init__.py
├── templates
│   ├── (group)
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
│   ├── base.html
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
