import inspect
from typing import Callable, Set

import pytest

from . import router


def inspect_callback(container: Set[str]) -> Callable[[str], None]:
    def enqueue_fn(url: str):
        container.add(inspect.stack()[1].filename)

    return enqueue_fn


@pytest.mark.parametrize(
    ["url"],
    [
        ('https://www.europotato.org/varieties/index',),
        ('https://www.europotato.org/varieties/index/0',),
        ('https://www.europotato.org/varieties/index/page:6',),
    ]
)
def test_index_router(url, tmp_path):
    content = open('europotato/varieties.html').read()
    handled_by: Set[str] = set()
    router.Handler(output_root=tmp_path).handle(content, url, inspect_callback(handled_by))

    assert len(handled_by) == 1
    assert handled_by.pop().endswith('europotato/index.py')


@pytest.mark.parametrize(
    ["url"],
    [
        ('https://www.europotato.org/varieties/view/King%20Edward-E',),
        ('https://www.europotato.org/varieties/view/King%20Edward-P',),
        ('https://www.europotato.org/varieties/view/00C133%20020-E',),
        ('https://www.europotato.org/varieties/view/02%20Z%20216%20A6-E',),
        ('https://www.europotato.org/varieties/view/02C053%20016-E',),
        ('https://www.europotato.org/varieties/view/03%20N%208A81-E',),
        ('https://www.europotato.org/varieties/view/03%20Z%206%20A5-E',),
        ('https://www.europotato.org/varieties/view/03C114%20006-E',),
        ('https://www.europotato.org/varieties/view/06%20Z%20266%20A%2015-E',),
        ('https://www.europotato.org/varieties/view/06.Z.266%20A4-E',),
        ('https://www.europotato.org/varieties/view/1%20119%20021%2060%20E-E',),
        ('https://www.europotato.org/varieties/view/1%20480%20009%2058%20E-E',),
        ('https://www.europotato.org/varieties/view/1017B28-E',),
        ('https://www.europotato.org/varieties/view/1033-E',),
        ('https://www.europotato.org/varieties/view/1036B34-E',),
        ('https://www.europotato.org/varieties/view/1037B18-E',),
        ('https://www.europotato.org/varieties/view/103B2-E',),
        ('https://www.europotato.org/varieties/view/103B3-E',),
        ('https://www.europotato.org/varieties/view/103B4-E',),
        ('https://www.europotato.org/varieties/view/1043-E',),
        ('https://www.europotato.org/varieties/view/1067-E',),
        ('https://www.europotato.org/varieties/view/10C4-E',),
        ('https://www.europotato.org/varieties/view/11%2079-E',),
        ('https://www.europotato.org/varieties/view/112B3-E',),
        ('https://www.europotato.org/varieties/view/1135C2-E',),
        ('https://www.europotato.org/varieties/view/1136C10-E',),
        ('https://www.europotato.org/varieties/view/1167D107-E',),
        ('https://www.europotato.org/varieties/view/1169D271-E',),
        ('https://www.europotato.org/varieties/view/1174D110-E',),
        ('https://www.europotato.org/varieties/view/1179D103-E',),
        ('https://www.europotato.org/varieties/view/118-E',),
        ('https://www.europotato.org/varieties/view/1180D113-E',),
        ('https://www.europotato.org/varieties/view/1183D251-E',),
        ('https://www.europotato.org/varieties/view/119-E',),
        ('https://www.europotato.org/varieties/view/120-E',),
        ('https://www.europotato.org/varieties/view/122-E',),
        ('https://www.europotato.org/varieties/view/1222-E',),
    ]
)
def test_pages_router(url, tmp_path):
    content = open('europotato/king_edward.html').read()
    handled_by: Set[str] = set()
    router.Handler(output_root=tmp_path).handle(content, url, inspect_callback(handled_by))

    assert len(handled_by) == 1
    assert handled_by.pop().endswith('europotato/view.py')


@pytest.mark.parametrize(
    ["url"],
    [
        ('https://www.europotato.org/varieties/View/King%20Edward-E',),
        ('https://www.europotato.org/varieties/view',),
        ('https://www.europotato.org/varieties/Index',),
        ('https://www.europotato.org/varieties/reports',),
        ('https://www.europotato.org/reports/',),
        ('https://www.europotato.com/varieties/view/03%20N%208A81-E',),
        ('http://www.google.com',),
        ('http://www.europotato.org/varieties/view/03C114%20006-E',),
        ('http://www.europotato.org/varieties/index',),
    ]
)
def test_unknown_url_pattern(url, tmp_path):
    with pytest.raises(NotImplementedError, match=f'No handler for URL: {url}'):
        router.Handler(output_root=tmp_path).handle('', url, None)
