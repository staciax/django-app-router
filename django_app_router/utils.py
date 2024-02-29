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

import importlib.util
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType


def import_module_from_path(fp: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location('module', fp)
    if spec is None:
        raise ImportError(f'Can\'t import module from {fp}')
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f'Can\'t import module from {fp}')
    spec.loader.exec_module(module)
    return module


def get_module_path(urlconf_module: str) -> Path:

    module: ModuleType = import_module(urlconf_module)
    if module.__file__ is None:
        raise ImportError(f'Can\'t import module from {urlconf_module}')

    module_path = Path(module.__file__).resolve()
    return module_path
