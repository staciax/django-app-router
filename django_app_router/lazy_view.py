from __future__ import annotations

from functools import partial
from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from django.urls.resolvers import RegexPattern, RoutePattern, URLPattern
from django.views.decorators.http import require_http_methods

__all__ = (
    'get',
    'post',
    'view',
    'get_view_urls',
)

if TYPE_CHECKING:
    from types import ModuleType

_F = TypeVar('_F', bound=Callable[..., Any])


def _make_lazy_view(
    route: str,
    /,
    *,
    name: str | None = None,
    re_path: bool = False,
    methods: list[str] | None = None,
    **kwargs: Any,
) -> Callable[[_F], _F]:
    def decorator(func: Any) -> Any:

        if methods is not None:
            func = require_http_methods(methods)(func)

        # make the view lazy
        Pattern = RoutePattern if not re_path else RegexPattern
        pattern = Pattern(route, name=name, is_endpoint=True)
        url = URLPattern(pattern, func, kwargs, name)
        setattr(func, '__url__', url)

        return func

    return decorator


view = partial(_make_lazy_view)

get = partial(_make_lazy_view, methods=['GET'])
post = partial(_make_lazy_view, methods=['POST'])

re_get = partial(_make_lazy_view, re=True, methods=['GET'])
re_post = partial(_make_lazy_view, re=True, methods=['POST'])


def get_view_urls(urlconf_module: str) -> list[URLPattern]:
    urlpatterns = []

    module: ModuleType = import_module(urlconf_module)

    for func in module.__dict__.values():

        if not callable(func):
            continue

        if not hasattr(func, '__url__'):
            continue

        url = getattr(func, '__url__')

        urlpatterns.append(url)

    return urlpatterns
