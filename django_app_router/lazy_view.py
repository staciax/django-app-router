from importlib import import_module
from typing import Any, Callable, List, Optional, TypeVar

from django.urls.resolvers import RoutePattern, URLPattern

__all__ = (
    'view',
    'get_view_urls',
)

T = TypeVar('T')


def view(path: str, *, name: Optional[str] = None) -> Callable[[T], T]:
    def decorator(func: Any) -> Any:
        kwargs: Any = None
        route_pattern = RoutePattern(path, name=name, is_endpoint=True)
        url_pattern = URLPattern(route_pattern, func, kwargs, name)
        setattr(func, '__url__', url_pattern)
        return func

    return decorator


def get_view_urls(urlconf_module: str) -> List[URLPattern]:
    urlpatterns = []

    module = import_module(urlconf_module)

    for name, obj in module.__dict__.items():

        if not callable(obj):
            continue

        if name.startswith('_'):
            continue

        if not hasattr(obj, '__url__'):
            continue

        url = getattr(obj, '__url__')
        urlpatterns.append(url)

    return urlpatterns
