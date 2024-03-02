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

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, get_type_hints

from django.urls import path

from . import utils

# fmt: off
__all__ = (
    'AppRouter',
)
# fmt: on

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern


def _clean_segment(segment: str) -> str:
    if segment.startswith('[') and segment.endswith(']'):
        return segment[1:-1]
    return segment


def _create_parameter(segment: str, param_type: type) -> str:
    return f'<{param_type.__name__}:{segment}>'


def _get_route(
    path: Path,
    func: Callable[..., Any],
    *,
    ignore_prefixes: tuple[str, ...] = ('(', '_'),
    trailing_slash: bool = True,
) -> str:

    normal_route = []
    func_type_hints = get_type_hints(func)
    for segment in path.parts:
        if segment.startswith('[') and segment.endswith(']'):
            parameter_name = _clean_segment(segment)
            parameter_type = func_type_hints.get(parameter_name, str)
            parameter = _create_parameter(parameter_name, parameter_type)
            normal_route.append(parameter)
        elif segment == '.':
            normal_route.append('')
        elif segment.startswith(ignore_prefixes):
            continue
        else:
            normal_route.append(segment)

    route = '/'.join(normal_route)
    if trailing_slash and route and not route.endswith('/'):
        route += '/'

    return route


class AppRouter:

    def __init__(self, trailing_slash: bool = True) -> None:
        self.trailing_slash = trailing_slash
        self._router_dirs: list[Path] = []

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls

    def add_app(self, app: str, /) -> None:

        app_dir = Path(app).resolve()

        if not app_dir.exists():
            raise FileNotFoundError(f'No app directory found in {app}')

        router_dir = app_dir.joinpath('routers')
        if not router_dir.exists():
            raise FileNotFoundError(f'No routers directory found in {app}')

        self._router_dirs.append(router_dir)

        # invalidate the urls cache
        if hasattr(self, '_urls'):
            del self._urls

    def get_urls(self) -> list[URLPattern]:

        urls = []

        for route_dir in self._router_dirs:
            page_files = route_dir.glob(r'**/page.py')
            for page_file in page_files:
                module = utils.import_module_from_path(page_file)
                if method := getattr(module, 'page', None):
                    file_path = page_file.relative_to(route_dir).parent
                    route = _get_route(
                        file_path,
                        method,
                        trailing_slash=self.trailing_slash,
                    )
                    urls.append(path(route, method, name=method.__doc__))

        return urls
