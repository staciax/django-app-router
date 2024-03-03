from pathlib import Path

from django_app_router import utils


def test_import_module_from_path():

    test_path = Path(__file__).parent

    routers = test_path.joinpath('routers')
    assert routers.exists()

    pages = routers.glob(r'**/page.py')

    for page_file in pages:
        module = utils.import_module_from_path(page_file)
        assert module is not None
        assert hasattr(module, 'page')
        assert callable(getattr(module, 'page'))


def test_import_module_from_path_with_invalid_file():

    invalid_file = Path('/path/to/invalid/file.py')

    try:
        utils.import_module_from_path(invalid_file)
    except FileNotFoundError as e:
        assert f'No such file or directory' in e.args[1]


def test_import_module_from_path_with_invalid_module():

    invalid_module = Path('/path/to/invalid/module')

    try:
        utils.import_module_from_path(invalid_module)
    except ImportError as e:
        assert f'Can\'t import module from {invalid_module}' in e.args[0]
