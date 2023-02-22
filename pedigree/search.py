import json
from typing import Callable, Dict
import urllib.parse

import bs4

from crawler import handler


class Handler(handler.Handler):
    """
    Handles search result pages from https://www.plantbreeding.wur.nl/PotatoPedigree.
    These contain links to pages with details about specific varieties.
    """

    def __init__(self, output_root: str):
        self.output_root = output_root

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        doc = bs4.BeautifulSoup(content, 'html.parser')
        table = doc.find('table')

        europotato_urls: Dict[int, str] = {}

        for row in table.find_all('tr', class_='row'):
            row_url = row.td.a['href']
            enqueue_callback(url, f"{row_url}&depth=8")

            # Extract mapping to europotato database to help us match records later.
            # This doesn't seem to always work, but it does give us an extra identifier
            # that we don't seem to have elsewhere.
            row_query = urllib.parse.urlsplit(row_url).query
            id_param = urllib.parse.parse_qs(row_query)['id'][0]  # json only has str keys.

            europotato_url = row.find('a', target='europotato')['href']
            europotato_query = urllib.parse.urlsplit(europotato_url).query
            europotato_name = urllib.parse.parse_qs(europotato_query)['variety_name'][0]

            europotato_urls[id_param] = europotato_name

        with open(self.output_root / 'europotato_names.json', 'w') as f:
            json.dump(europotato_urls, f)
