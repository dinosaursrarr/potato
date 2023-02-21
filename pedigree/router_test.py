import inspect
import os
import re
from typing import Callable, Set

import pytest

from .router import Handler


def inspect_callback(container: Set[str]) -> Callable[[str, str], None]:
    def enqueue_fn(current_url: str, new_url: str):
        container.add(inspect.stack()[1].filename)

    return enqueue_fn


def test_search_router(tmp_path):
    content = open('pedigree/search.html').read()
    handled_by: Set[str] = set()
    Handler(output_root=tmp_path).handle(content, 'https://www.plantbreeding.wur.nl/PotatoPedigree/multilookup.php',
                                         inspect_callback(handled_by))

    assert len(handled_by) == 1
    assert handled_by.pop().endswith('pedigree/search.py')


@pytest.mark.parametrize(
    ["url", "output_file"],
    [
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9184&depth=8', "9184.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9184', "9184.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=1&depth=8', "1.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2&depth=8', "2.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=3&depth=8', "3.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=4&depth=8', "4.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=5&depth=8', "5.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9038&depth=8', "9038.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9039&depth=8', "9039.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9040&depth=8', "9040.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9041&depth=8', "9041.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9042&depth=8', "9042.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9043&depth=8', "9043.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9044&depth=8', "9044.json"),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9045&depth=8', "9045.json"),
    ]
)
def test_imagemap_router(url, output_file, tmp_path):
    content = open('pedigree/imagemap.html').read()
    handled_by: Set[str] = set()
    Handler(output_root=tmp_path).handle(content, url, inspect_callback(handled_by))

    assert os.path.exists(tmp_path / output_file)


@pytest.mark.parametrize(
    ["url"],
    [
        ('https://www.plantbreeding.wur.nl/potatopedigree/pedigree_imagemap.php?id=9184&depth=8',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.phP?id=9184&depth=8',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_Imagemap.php?id=9184&depth=8',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/Pedigree_imagemap.php?id=9184&depth=8',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.ph',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?depth=8',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree/',),
        ('https://www.plantbreeding.wur.nl/PotatoPedigree',),
        ('http://www.google.com',),
    ]
)
def test_unknown_url_pattern(url, tmp_path):
    with pytest.raises(NotImplementedError, match=re.escape(f'No handler for URL: {url}')):
        Handler(output_root=tmp_path).handle('', url, None)
