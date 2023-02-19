import urllib.parse

from . import index


def test_extract_links_to_varieties():
    expected_urls = [
        'https://www.europotato.org/varieties/view/00C133%20020-E',
        'https://www.europotato.org/varieties/view/02%20Z%20216%20A6-E',
        'https://www.europotato.org/varieties/view/02C053%20016-E',
        'https://www.europotato.org/varieties/view/03%20N%208A81-E',
        'https://www.europotato.org/varieties/view/03%20Z%206%20A5-E',
        'https://www.europotato.org/varieties/view/03C114%20006-E',
        'https://www.europotato.org/varieties/view/06%20Z%20266%20A%2015-E',
        'https://www.europotato.org/varieties/view/06.Z.266%20A4-E',
        'https://www.europotato.org/varieties/view/1%20119%20021%2060%20E-E',
        'https://www.europotato.org/varieties/view/1%20480%20009%2058%20E-E',
        'https://www.europotato.org/varieties/view/1017B28-E',
        'https://www.europotato.org/varieties/view/1033-E',
        'https://www.europotato.org/varieties/view/1036B34-E',
        'https://www.europotato.org/varieties/view/1037B18-E',
        'https://www.europotato.org/varieties/view/103B2-E',
        'https://www.europotato.org/varieties/view/103B3-E',
        'https://www.europotato.org/varieties/view/103B4-E',
        'https://www.europotato.org/varieties/view/1043-E',
        'https://www.europotato.org/varieties/view/1067-E',
        'https://www.europotato.org/varieties/view/10C4-E',
        'https://www.europotato.org/varieties/view/11%2079-E',
        'https://www.europotato.org/varieties/view/112B3-E',
        'https://www.europotato.org/varieties/view/1135C2-E',
        'https://www.europotato.org/varieties/view/1136C10-E',
        'https://www.europotato.org/varieties/view/1167D107-E',
        'https://www.europotato.org/varieties/view/1169D271-E',
        'https://www.europotato.org/varieties/view/1174D110-E',
        'https://www.europotato.org/varieties/view/1179D103-E',
        'https://www.europotato.org/varieties/view/118-E',
        'https://www.europotato.org/varieties/view/1180D113-E',
        'https://www.europotato.org/varieties/view/1183D251-E',
        'https://www.europotato.org/varieties/view/119-E',
        'https://www.europotato.org/varieties/view/120-E',
        'https://www.europotato.org/varieties/view/122-E',
        'https://www.europotato.org/varieties/view/1222-E',
    ]
    content = open('europotato/varieties.html').read()
    extracted_urls = set()
    root = 'https://www.europotato.org/varieties/index'

    def callback(url: str) -> None:
        extracted_urls.add(urllib.parse.urljoin(root, url))

    index.Handler().handle(content, root, callback)

    assert set(expected_urls).issubset(extracted_urls)


def test_extract_links_to_letters():
    expected_urls = [
        'https://www.europotato.org/varieties/index/0',
        'https://www.europotato.org/varieties/index/1',
        'https://www.europotato.org/varieties/index/2',
        'https://www.europotato.org/varieties/index/3',
        'https://www.europotato.org/varieties/index/4',
        'https://www.europotato.org/varieties/index/5',
        'https://www.europotato.org/varieties/index/6',
        'https://www.europotato.org/varieties/index/7',
        'https://www.europotato.org/varieties/index/8',
        'https://www.europotato.org/varieties/index/9',
        'https://www.europotato.org/varieties/index/A',
        'https://www.europotato.org/varieties/index/B',
        'https://www.europotato.org/varieties/index/C',
        'https://www.europotato.org/varieties/index/D',
        'https://www.europotato.org/varieties/index/E',
        'https://www.europotato.org/varieties/index/F',
        'https://www.europotato.org/varieties/index/G',
        'https://www.europotato.org/varieties/index/H',
        'https://www.europotato.org/varieties/index/I',
        'https://www.europotato.org/varieties/index/J',
        'https://www.europotato.org/varieties/index/K',
        'https://www.europotato.org/varieties/index/L',
        'https://www.europotato.org/varieties/index/M',
        'https://www.europotato.org/varieties/index/N',
        'https://www.europotato.org/varieties/index/O',
        'https://www.europotato.org/varieties/index/P',
        'https://www.europotato.org/varieties/index/Q',
        'https://www.europotato.org/varieties/index/R',
        'https://www.europotato.org/varieties/index/S',
        'https://www.europotato.org/varieties/index/T',
        'https://www.europotato.org/varieties/index/U',
        'https://www.europotato.org/varieties/index/V',
        'https://www.europotato.org/varieties/index/W',
        'https://www.europotato.org/varieties/index/X',
        'https://www.europotato.org/varieties/index/Y',
        'https://www.europotato.org/varieties/index/Z',
    ]
    content = open('europotato/varieties.html').read()
    extracted_urls = set()
    root = 'https://www.europotato.org/varieties/index'

    def callback(url: str) -> None:
        extracted_urls.add(urllib.parse.urljoin(root, url))

    index.Handler().handle(content, root, callback)

    assert set(expected_urls).issubset(extracted_urls)


def test_extract_links_to_pages():
    expected_urls = [
        'https://www.europotato.org/varieties/index/page:2',
        'https://www.europotato.org/varieties/index/page:3',
        'https://www.europotato.org/varieties/index/page:4',
        'https://www.europotato.org/varieties/index/page:5',
        'https://www.europotato.org/varieties/index/page:6',
        'https://www.europotato.org/varieties/index/page:7',
        'https://www.europotato.org/varieties/index/page:8',
        'https://www.europotato.org/varieties/index/page:9',
        'https://www.europotato.org/varieties/index/page:2',
        'https://www.europotato.org/varieties/index/page:177',
    ]
    content = open('europotato/varieties.html').read()
    extracted_urls = set()
    root = 'https://www.europotato.org/varieties/index'

    def callback(url: str) -> None:
        extracted_urls.add(urllib.parse.urljoin(root, url))

    index.Handler().handle(content, root, callback)

    assert set(expected_urls).issubset(extracted_urls)
