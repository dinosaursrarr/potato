from typing import Callable

import bs4

from crawler import handler


class Handler(handler.Handler):
    """
    Handles index pages from europotato.org. These contain links to other index pages,
    and to pages with details about specific varieties.
    """

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        doc = bs4.BeautifulSoup(content, 'html.parser')

        # Enqueue links to details on varieties.
        varieties = doc.find(id='advanced-search-results')
        for variety in varieties.findAll('a', class_='result-item'):
            enqueue_callback(url, variety['href'])

        # Enqueue links to other index letters.
        letters = doc.findAll('a', class_='variety_letter') + doc.findAll('a', class_='variety_letter_selected')
        for letter in letters:
            enqueue_callback(url, letter['href'])

        # Enqueue links to other index pages.
        paging = doc.find('div', class_='paging')
        for page in paging.findAll('a'):
            enqueue_callback(url, page['href'])
