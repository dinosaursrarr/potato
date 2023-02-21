from typing import Callable

import bs4

from crawler import handler


class Handler(handler.Handler):
    """
    Handles search result pages from https://www.plantbreeding.wur.nl/PotatoPedigree.
    These contain links to pages with details about specific varieties.
    """

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        doc = bs4.BeautifulSoup(content, 'html.parser')
        table = doc.find('table')
        for row in table.find_all('tr', class_='row'):
            enqueue_callback(url, f"{row.td.a['href']}&depth=8")
