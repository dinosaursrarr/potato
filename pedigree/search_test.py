import pytest
import json
import urllib.parse

from .search import Handler

SEARCH_URL = 'https://www.plantbreeding.wur.nl/PotatoPedigree/multilookup.php'


def test_extract_links(tmp_path):
    extracted_urls = set()

    def callback(current_url: str, new_url: str) -> None:
        extracted_urls.add(urllib.parse.urljoin(current_url, new_url))

    with open('pedigree/search.html', 'r') as f:
        content = f.read()
        Handler(tmp_path).handle(content, SEARCH_URL, callback)

    assert extracted_urls == {
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=1&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9184&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=3&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=4&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=5&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9038&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9039&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9040&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9041&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9042&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9043&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9044&depth=8',
        'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=9045&depth=8',
    }


def test_write_europotato_urls(tmp_path):
    def noop_callback(current_url: str, new_url: str) -> None:
        pass

    with open('pedigree/search.html', 'r') as f:
        content = f.read()
        Handler(tmp_path).handle(content, SEARCH_URL, noop_callback)

    with open(tmp_path / 'europotato_names.json', 'r') as f:
        result = json.load(f)
        assert result == {
            '1': '002/9',
            '9184': '01-EDQ-1',
            '2': '1-65.209/102 B',
            '3': '1-65.751/132 N',
            '4': '1-67.254/13 N',
            '5': '1-70.486/108 N',
            '9038': 'ZUBELDIA',
            '9039': 'ZUBRENOK',
            '9040': 'ZUNTA',
            '9041': 'ZVIKOV',
            '9042': 'ZWARTJES',
            '9043': 'ZWICKAUER FRUHE',
            '9044': 'ZWICKAUER FRUHE GELBE',
            '9045': 'ZWICKAUER VIERZIGKNOLLIGE',
        }
