import datetime
import queue
import time
from typing import Callable, Dict, Optional

import pytest

from . import crawler, error_handler, fetcher, handler


class FakeFetcher(fetcher.Fetcher):
    def __init__(self, return_values: Dict[str, str], error: Optional[Exception] = None):
        self.return_values = return_values
        self.error = error

    def fetch(self, url: str) -> str:
        if self.error:
            raise self.error
        return self.return_values[url]


class FakeHandler(handler.Handler):
    def __init__(self, action: Callable[[str, str, Callable[[str], None]], None]):
        self.action = action

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str], None]) -> None:
        self.action(content, url, enqueue_callback)


def test_crawl_root():
    f = FakeFetcher({'root': 'foo'})
    processed = []
    h = FakeHandler(lambda content, url, callback: processed.append(f'{url}: {content}'))
    e = error_handler.ThrowingHandler()

    crawler.Crawler(f, h, e, queue.Queue).crawl('root')

    assert processed == ['root: foo']


def test_crawl_discovered_pages_bfs():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz', 'c': 'qux', 'd': 'quux'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('a')
            callback('b')
        elif content == 'bar':
            callback('c')
        elif content == 'baz':
            callback('d')

    h = FakeHandler(handle)
    e = error_handler.ThrowingHandler()

    crawler.Crawler(f, h, e, queue.Queue).crawl('root')

    assert processed == ['root: foo', 'a: bar', 'b: baz', 'c: qux', 'd: quux']


def test_crawl_discovered_pages_dfs():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz', 'c': 'qux', 'd': 'quux'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('a')
            callback('b')
        elif content == 'bar':
            callback('c')
        elif content == 'baz':
            callback('d')

    h = FakeHandler(handle)
    e = error_handler.ThrowingHandler()

    crawler.Crawler(f, h, e, queue.LifoQueue).crawl('root')

    assert processed == ['root: foo', 'b: baz', 'd: quux', 'a: bar', 'c: qux']


def test_do_not_crawl_same_page_twice():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz', 'c': 'qux', 'd': 'quux'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('root')
            callback('a')
            callback('b')
        elif content == 'bar':
            callback('a')
            callback('c')
        elif content == 'baz':
            callback('a')
            callback('b')
            callback('d')

    h = FakeHandler(handle)
    e = error_handler.ThrowingHandler()

    crawler.Crawler(f, h, e, queue.Queue).crawl('root')

    assert processed == ['root: foo', 'a: bar', 'b: baz', 'c: qux', 'd: quux']


def test_crawl_delay():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('a')
            callback('b')

    h = FakeHandler(handle)
    e = error_handler.ThrowingHandler()
    crawl_delay = datetime.timedelta(seconds=0.25)

    start = time.time()
    crawler.Crawler(f, h, e, queue.Queue, crawl_delay=crawl_delay).crawl('root')
    end = time.time()

    assert len(processed) == 3
    assert end - start > len(processed) * crawl_delay.total_seconds()


def test_error_fetching():
    f = FakeFetcher({}, ValueError('foo'))
    h = FakeHandler(lambda page, url, callback: None)
    e = error_handler.ThrowingHandler()

    with pytest.raises(ValueError, match='foo'):
        crawler.Crawler(f, h, e, queue.Queue).crawl('root')


def test_error_handling():
    f = FakeFetcher({'root': 'foo'})

    def handle(page: str, url: str, callback: Callable[[str], None]) -> None:
        raise ValueError('bar')

    h = FakeHandler(handle)
    e = error_handler.ThrowingHandler()

    with pytest.raises(ValueError, match='bar'):
        crawler.Crawler(f, h, e, queue.Queue).crawl('root')
