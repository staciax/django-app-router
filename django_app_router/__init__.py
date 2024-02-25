"""
Django App Router
~~~~~~~~~~~~~~~~~~~
A simple Django app to route requests, Inspired by Next.js App Router.
:copyright: (c) 2024-present STACiA
:license: MIT, see LICENSE for more details.
"""

__title__ = 'django_app_router'
__author__ = 'STACiA'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024-present STACiA(staciax)'
__version__ = '0.0.5'


from typing import Literal, NamedTuple

from .app_router import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: Literal['alpha', 'beta', 'final']


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=5, release='final')

del NamedTuple, Literal, VersionInfo
