from __future__ import annotations

from functools import partial
from typing import Any, Callable, TypeVar

from django.urls.resolvers import RegexPattern, RoutePattern, URLPattern
from django.views.decorators.http import require_http_methods

from . import utils

__all__ = (
    'get',
    'post',
    'view_action',
    'get_view_actions_urls',
)

_F = TypeVar('_F', bound=Callable[..., Any])


def _make_view_action(
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


view_action = partial(_make_view_action)

get = partial(_make_view_action, methods=['GET'])
post = partial(_make_view_action, methods=['POST'])

re_get = partial(_make_view_action, re=True, methods=['GET'])
re_post = partial(_make_view_action, re=True, methods=['POST'])


def get_view_actions_urls(urlconf_module: str) -> list[URLPattern]:

    urlpatterns: list[URLPattern] = []

    target_path = utils.get_module_path(urlconf_module).parent

    action_files = target_path.glob('**/actions.py')

    for action in action_files:
        module = utils.import_module_from_path(action)
        for method_name in dir(module):
            method = getattr(module, method_name)
            if url := getattr(method, '__url__', None):
                urlpatterns.append(url)

    return urlpatterns
