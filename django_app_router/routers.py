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

from abc import ABC, abstractmethod
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

PATH_IGNORE_PREFIXES = ('(', '_')
# group, and private segments


def _get_route(
    path: Path,
    func: Callable[..., Any],
    *,
    trailing_slash: bool = True,
) -> str:
    """
    Constructs a route string based on the given path and function.
    """
    parameters = []
    func_type_hints = get_type_hints(func)
    for segment in path.parts:

        if segment.startswith(PATH_IGNORE_PREFIXES):
            continue

        if segment.startswith('[') and segment.endswith(']'):
            parameter_name = segment[1:-1]
            parameter_type = func_type_hints.get(parameter_name, str)
            parameter = f'<{parameter_type.__name__}:{parameter_name}>'
            parameters.append(parameter)
        else:
            parameters.append(segment)

    route = '/'.join(parameters)
    if trailing_slash and route and not route.endswith('/'):
        route += '/'

    return route


class BaseRouter(ABC):

    def __init__(self) -> None:
        self.app_router_paths = []

    def include_app(self, app_name: str, /, *, app_dir: bool = True) -> None:
        """
        Includes an app in the router.
        """
        app_path = Path(app_name).resolve()

        if not app_path.exists():
            raise FileNotFoundError(f'No app directory found in {app_name}')

        router_path = app_path.joinpath('routers')
        if not router_path.exists():
            raise FileNotFoundError(f'No routers directory found in {app_name}')

        if app_dir and router_path.joinpath(app_name).exists():
            router_path = router_path.joinpath(app_name)

        self.app_router_paths.append(router_path)

        # invalidate the urls cache
        if hasattr(self, '_urls'):
            del self._urls

    @abstractmethod
    def get_urls(self) -> list[URLPattern]:
        """Return a list of URL patterns."""

    @property
    def urls(self) -> list[URLPattern]:
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


class AppRouter(BaseRouter):

    def __init__(
        self,
        trailing_slash: bool = True,
    ) -> None:
        super().__init__()
        self.trailing_slash = trailing_slash

    def get_urls(self) -> list[URLPattern]:
        """
        Return a list of URL Pattern for the app router.
        """
        urls = []

        for route_path in self.app_router_paths:
            page_files = route_path.glob(r'**/page.py')
            for page_file in page_files:
                module = utils.import_module_from_path(page_file)

                # TODO: Future features
                # - Add support custom method name
                if method := getattr(module, 'page', None):
                    file_path = page_file.relative_to(route_path).parent
                    route = _get_route(
                        file_path,
                        method,
                        trailing_slash=self.trailing_slash,
                    )
                    urls.append(
                        path(
                            route,
                            method,
                            name=method.__doc__,
                        )
                    )

        return urls
