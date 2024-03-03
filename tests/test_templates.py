from django.template.loader import get_template


def test_get_home_template():
    page = get_template('page.html')
    assert page is not None


def test_get_group_about_template():
    page = get_template('(test_group)/about/page.html')
    assert page is not None


def test_get_group_info_template():
    page = get_template('(test_group)/info/page.html')
    assert page is not None


def test_get_nested_lv1_template():
    page = get_template('test_nested/page.html')
    assert page is not None


def test_get_nested_lv2_template():
    page = get_template('test_nested/test_nested_2/page.html')
    assert page is not None


def test_get_slug_template():
    page = get_template('test_slug/[slug]/page.html')
    assert page is not None
