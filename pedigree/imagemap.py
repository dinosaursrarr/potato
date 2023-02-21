import html
import json
import pathlib
import re
import urllib.parse
from typing import Any, Callable, Dict, List, Optional

import bs4

from crawler import handler

_VARIETY_NAME = re.compile(r'pedigree image for \'([^\']+)\'')
_YEAR_OF_INTRODUCTION = re.compile(r'\(year: (\d+)\)  \[depth=8\]')


class Handler(handler.Handler):
    """
    Handles image map pages from https://www.plantbreeding.wur.nl/PotatoPedigree.
    These contain an interactive image showing the ancestors of a given variety
    of potato. Data is written as json to files named for the url. 
    """

    def __init__(self, output_root: pathlib.Path):
        self.output_root = output_root

    @staticmethod
    def _extract_name(doc: bs4.BeautifulSoup) -> Optional[str]:
        tag = doc.find('h1').findNext('font').b
        if not tag:
            return None
        match = _VARIETY_NAME.match(tag.text.strip())
        if not match:
            return None
        return match.group(1)

    @staticmethod
    def _extract_year_of_introduction(doc: bs4.BeautifulSoup) -> Optional[int]:
        tag = doc.find('h1').findNext('font').b.next_sibling
        if not tag:
            return None
        match = _YEAR_OF_INTRODUCTION.match(tag.text.strip())
        if not match:
            return None
        return int(match.group(1))

    @staticmethod
    def _extract_area_year(long: str, short: str) -> int:
        # May need a more general solution if other HTML entities crop up.
        return int(html.unescape(long)
                   .removeprefix(short)
                   .strip()
                   .replace('<', '')
                   .replace('(', '')
                   .replace(')', ''))

    @staticmethod
    def _extract_area(area: bs4.Tag) -> Dict[str, Any]:
        """
        Just pulling out the details that are in the HTML page, rather than trying to recreate
        the graph structure based on locations. That task seems fiddly and I'm unlikely to get
        it right first time, so we should separate it from the task of just getting hold of data.
        """
        result = {'name': area['title'],
                  'coordinates': [int(c) for c in area['coords'].split(',')]}
        try:
            result['year_of_introduction'] = Handler._extract_area_year(area['alt'], area['title'])
        except (TypeError, ValueError):
            pass
        return result

    @staticmethod
    def _extract_parentage(doc: bs4.BeautifulSoup) -> List[Dict[str, Any]]:
        tag = doc.find('map')
        if tag is None:
            return []
        return [Handler._extract_area(area) for area in tag.findAll('area')]

    @staticmethod
    def _output_filename(url: str):
        query = urllib.parse.urlsplit(url).query
        id_param = urllib.parse.parse_qs(query)['id'][0]
        return pathlib.Path(id_param)

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        # Collect information in a dict, which we will dump to JSON.
        variety = {
            'url': url,
        }

        doc = bs4.BeautifulSoup(content, 'html.parser')

        name = Handler._extract_name(doc)
        if name:
            variety['name'] = name

        year_of_introduction = Handler._extract_year_of_introduction(doc)
        if year_of_introduction:
            variety['year_of_introduction'] = year_of_introduction

        parentage = Handler._extract_parentage(doc)
        if parentage:
            variety['parentage'] = parentage

        output_path = self.output_root / f'{Handler._output_filename(url)}.json'
        with open(output_path, 'w') as f:
            json.dump(variety, f)
