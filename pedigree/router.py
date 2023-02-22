from typing import Callable

from crawler import handler
from . import imagemap, search


class Handler(handler.Handler):
    """
    Routes pages from https://www.plantbreeding.wur.nl/PotatoPedigree to appropriate handlers for their templates,
    based on their URLs.
    """

    def __init__(self, output_root: str):
        self.output_root = output_root

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        if url.startswith('https://www.plantbreeding.wur.nl/PotatoPedigree/multilookup.php'):
            search.Handler(self.output_root).handle(content, url, enqueue_callback)
            return
        if url.startswith('https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id='):
            imagemap.Handler(self.output_root).handle(content, url, enqueue_callback)
            return
        raise NotImplementedError(f'No handler for URL: {url}')
