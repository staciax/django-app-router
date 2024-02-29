"""
MIT License

Copyright (c) 2024-present STACiA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import re
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, List, Union, get_type_hints

from django.urls.resolvers import RoutePattern, URLPattern

from . import utils

# fmt: off
__all__ = (
    'init',
)
# fmt: on


log = logging.getLogger('django_app_router')

SEGMENT_REGEX = re.compile(r'^(\[.+\])$')
PATH_IGNORE_REGEX = re.compile(r'^(\(.+\))|^(_.+)$')


def _normalize_route(
    route_path: Path,
    func: Callable[..., Any],
    *,
    trailing_slash: bool = True,
) -> str:

    # TODO: route_path regex validation

    normal_route = []
    func_type_hints = get_type_hints(func)

    route_path_string = str(route_path)
    for param in route_path_string.split('/'):
        if SEGMENT_REGEX.match(param):
            param = param[1:-1]
            param_type = func_type_hints.get(param, str)
            segment = f'<{param_type.__name__}:{param}>'
            normal_route.append(segment)
        elif param == '.':
            normal_route.append('')
        elif PATH_IGNORE_REGEX.match(param):
            continue
        else:
            normal_route.append(param)

    route = '/'.join(normal_route)
    if trailing_slash and route != '' and not route.endswith('/'):
        route += '/'
    return route


def init(urlconf_module: Union[Path, str]) -> List[URLPattern]:

    url_patterns = []

    if isinstance(urlconf_module, str):
        module = import_module(urlconf_module)
        if module.__file__ is None:
            raise ImportError(f'Can\'t import module from {urlconf_module}')

        module_path = Path(module.__file__).parent
    else:
        module_path = urlconf_module

    if not module_path.exists():
        raise FileNotFoundError(f'{module_path} does not exist')

    pages = module_path.glob('**/page.py')

    for page_path in pages:

        module = utils.get_module_from_path(page_path)

        if not hasattr(module, 'page'):
            log.warning(f'Should have a page function in {page_path}')
            continue

        func = getattr(module, 'page')

        route = page_path.relative_to(module_path).parent

        route_string = _normalize_route(route, func)
        route_name = func.__doc__

        # TODO: support kwargs
        kwargs: Any = None

        route_pattern = RoutePattern(route_string, name=route_name, is_endpoint=True)
        url_pattern = URLPattern(route_pattern, func, kwargs, route_name)

        url_patterns.append(url_pattern)

    return url_patterns
