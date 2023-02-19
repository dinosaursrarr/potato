import json
import pathlib
import urllib.parse
from typing import Callable, List, Optional

import bs4

from crawler import handler


class Handler(handler.Handler):
    def __init__(self, output_root: pathlib.Path):
        self.output_root = output_root

    @staticmethod
    def _output_filename(url: str):
        url_path = urllib.parse.urlsplit(url).path
        return pathlib.Path(url_path).name

    @staticmethod
    def _extract_name(doc: bs4.BeautifulSoup) -> Optional[str]:
        h2 = doc.find('h2')
        if not h2:
            return None
        return h2.text.strip()

    @staticmethod
    def _extract_breed_info(doc: bs4.BeautifulSoup):
        breed_info = doc.find(id='breed-info')
        if not breed_info:
            return None
        result = {}
        for div in breed_info.findAll('div'):
            h, v = div.findAll('span')
            header = h.text.strip().replace('[Pedigree History ]', '')
            value_links = v.findAll('a')
            if len(value_links) > 1:
                value = [a.text.strip() for a in value_links]
            else:
                value = v.text.strip()
            result[header] = value
        return result

    @staticmethod
    def _extract_table(table: bs4.BeautifulSoup):
        result = {}
        rows = table.findAll('tr')
        header = None
        values = []
        for row in rows:
            if row.th:
                continue
            left, right = row.find_all('td')
            if left.text:
                if header:
                    result[header] = values
                header = left.text
                values = [right.text]
            else:
                values.append(right.text)
        result[header] = values
        return result

    @staticmethod
    def _extract_tab_links(doc: bs4.BeautifulSoup) -> List[str]:
        results = []
        for ul in doc.findAll('ul', class_='nav-tabs'):
            results.extend([a['href'] for a in ul.findAll('a')])
        return results

    """
    Handles detail pages from europotato.org. These contain details about a given
    variety of potato. Data is written as json to files named for the url. 
    """

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str], None]) -> None:
        # Collect information in a dict, which we will dump to JSON.
        variety = {
            'url': url,
        }

        doc = bs4.BeautifulSoup(content, 'html.parser')

        name = Handler._extract_name(doc)
        if name:
            variety['name'] = name

        breed_info = Handler._extract_breed_info(doc)
        if breed_info:
            variety['breed-info'] = breed_info

        for table in doc.findAll('table', class_="variety-characters"):
            title = table.find('th').text
            table_details = Handler._extract_table(table)
            if table_details:
                variety[title] = table_details

        tab_links = Handler._extract_tab_links(doc)
        for tab_link in tab_links:
            enqueue_callback(urllib.parse.urljoin(url, tab_link))

        output_path = self.output_root / f'{Handler._output_filename(url)}.json'
        with open(output_path, 'w') as f:
            json.dump(variety, f)
