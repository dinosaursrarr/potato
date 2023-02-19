import json
import urllib.parse

from . import view


def noop_callback(current_url: str, new_url: str) -> None:
    pass


def test_extract_name(tmp_path):
    content = open('europotato/king_edward.html').read()
    url = 'https://www.europotato.org/varieties/view/King%20Edward-E'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    view.Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "King%20Edward-E.json") as f:
        result = json.load(f)
        assert result['name'] == 'King Edward'


def test_include_url(tmp_path):
    content = open('europotato/king_edward.html').read()
    url = 'https://www.europotato.org/varieties/view/King%20Edward-E'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    view.Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "King%20Edward-E.json") as f:
        result = json.load(f)
        assert result['url'] == url


def test_extract_breed_info(tmp_path):
    content = open('europotato/king_edward.html').read()
    url = 'https://www.europotato.org/varieties/view/King%20Edward-E'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    view.Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "King%20Edward-E.json") as f:
        result = json.load(f)
        assert result['breed-info'] == {
            'Higher Taxon': 'Solanaceae',
            'Genus': 'Solanum L.',
            'Species': 'Solanum tuberosum L. cv. King Edward',
            'Parentage': ['Magnum Bonum x Beauty of Hebron', 'Magnum Bonum x Beauty of Hebron (tbr)'],
            'Breeder': '7',
            'Breeder Agent': 'GB Seed Industry',
        }


def test_extract_tables(tmp_path):
    content = open('europotato/king_edward.html').read()
    url = 'https://www.europotato.org/varieties/view/King%20Edward-E'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    view.Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "King%20Edward-E.json") as f:
        result = json.load(f)
        assert result['administration'] == {
            'Data source': ['AR', 'ARCHE NOAH', 'DEPT', 'DEU416', 'FRA179', 'GBR165', 'IRL001', 'POL IPR BON'],
            'Plant material maintained as': ['Tuber', 'In-vitro', 'Tuber and in-vitro', 'In-vitro and '
                                                                                        'cryopreservation'],
            'Plant health directive EC77/93, requirements': ['Fully tested', 'Part tested', 'Untested'],
            'Country of origin': ['UNITED KINGDOM'],
            'Sample status': ['Advanced cultivar'],
            'Test conditions': ['Organic', 'Non organic'],
        }


def test_enqueue_tab_links(tmp_path):
    content = open('europotato/king_edward.html').read()
    page_url = 'https://www.europotato.org/varieties/view/King%20Edward-E'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    expected_urls = [
        'https://www.europotato.org/varieties/view/King%20Edward-E',
        'https://www.europotato.org/varieties/view/King%20Edward-P'
    ]
    enqueued_urls = []

    def enqueue_callback(current_url: str, new_url: str) -> None:
        enqueued_urls.append(urllib.parse.urljoin(current_url, new_url))

    view.Handler(output_dir).handle(content, page_url, enqueue_callback)

    assert enqueued_urls == expected_urls
