from pathlib import Path

from django.urls.resolvers import URLPattern

from django_app_router import routers
from django_app_router.routers import _get_route


def test_app_router_get_urls(router: routers.AppRouter):

    router.include_app('tests')
    urls = router.get_urls()

    assert len(urls) != 0
    assert isinstance(urls, list)
    assert all(isinstance(url, URLPattern) for url in urls)


def test_app_router_get_urls_with_trailing_slash(router: routers.AppRouter):

    router.include_app('tests')

    router.trailing_slash = True
    urls = router.get_urls()
    assert len(urls) != 0

    assert all(str(url.pattern).endswith('/') for url in urls if str(url.pattern) != '')


def test_app_router_get_urls_without_trailing_slash(router: routers.AppRouter):

    router.include_app('tests')

    router.trailing_slash = False
    urls = router.get_urls()
    assert len(urls) != 0

    assert all(not str(url.pattern).endswith('/') for url in urls)


def test_app_router_add_url_method_1(router: routers.AppRouter):
    router.include_app('tests')

    urlpatterns = []
    urlpatterns += router.urls

    assert len(urlpatterns) != 0


def test_app_router_add_url_method_2(router: routers.AppRouter):
    from django.urls import URLResolver, include, path

    router.include_app('tests')

    urlpatterns = [
        path('', include(router.urls)),
    ]

    assert len(urlpatterns) == 1
    assert isinstance(urlpatterns[0], URLResolver)

    all_urls = getattr(urlpatterns[0], 'url_patterns', [])
    assert len(all_urls) != 0
    assert all(isinstance(url, URLPattern) for url in all_urls)


def test_app_router_invalidate_url_cache(router: routers.AppRouter):

    assert not hasattr(router, '_urls')
    router.urls
    assert hasattr(router, '_urls')

    router.include_app('tests')
    assert not hasattr(router, '_urls')


def test_app_router_app_not_found(router: routers.AppRouter):
    invalid_app = 'invalid_app'

    try:
        router.include_app(invalid_app)
    except FileNotFoundError as e:
        assert f'No app directory found in {invalid_app}' in e.args[0]


def test_app_router_app_routers_not_found(router: routers.AppRouter):
    test_app = 'tests/test_app'

    try:
        router.include_app(test_app)
    except FileNotFoundError as e:
        assert f'No routers directory found in {test_app}' in e.args[0]


def test_get_route_dynamic_segment():
    path = Path('[param]')
    func = lambda param: None
    route = _get_route(path, func)
    assert route == '<str:param>/'


def test_get_route_ignore_segment():
    path = Path('_ignore')
    func = lambda: None
    route = _get_route(path, func)
    assert route == ''


def test_get_route_group_segment():
    path = Path('(group)')
    func = lambda: None
    route = _get_route(path, func)
    assert route == ''


def test_get_route_static_segment():
    path = Path('static')
    func = lambda: None
    route = _get_route(path, func)
    assert route == 'static/'


def test_get_route_multiple_segments():
    path = Path('segment1/segment2')
    func = lambda: None
    route = _get_route(path, func)
    assert route == 'segment1/segment2/'


def test_get_route_trailing_slash():
    path = Path('segment')
    func = lambda: None
    route = _get_route(path, func, trailing_slash=True)
    assert route == 'segment/'


def test_get_route_no_trailing_slash():
    path = Path('segment')
    func = lambda: None
    route = _get_route(path, func, trailing_slash=False)
    assert route == 'segment'


def test_include_app_valid_app_dir_true():
    router = routers.AppRouter()
    router.include_app('tests', app_dir=True)
    assert len(router.app_router_paths) == 1
    assert router.app_router_paths[0].name == 'tests'


def test_include_app_valid_app_dir_false():
    router = routers.AppRouter()
    router.include_app('tests', app_dir=False)
    assert len(router.app_router_paths) == 1
    assert router.app_router_paths[0].name == 'routers'
