import urllib.parse

from .search import Handler


def test_extact_links():
    extracted_urls = set()

    def callback(current_url, new_url: str) -> None:
        extracted_urls.add(urllib.parse.urljoin(current_url, new_url))

    with open('pedigree/search.html', 'r') as f:
        content = f.read()
        Handler().handle(content, 'https://www.plantbreeding.wur.nl/PotatoPedigree/multilookup.php', callback)

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
