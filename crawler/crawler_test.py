import datetime
import queue
import time
from typing import Callable, Dict, Optional

import pytest

from .crawler import Crawler
from .error_handler import ThrowingHandler
from .fetcher import Fetcher
from .handler import Handler
from .state_manager import StateManager


class FakeFetcher(Fetcher):
    def __init__(self, return_values: Dict[str, str], error: Optional[Exception] = None):
        self.return_values = return_values
        self.error = error

    def fetch(self, url: str) -> str:
        if self.error:
            raise self.error
        return self.return_values[url]


class FakeHandler(Handler):
    def __init__(self, action: Callable[[str, str, Callable[[str, str], None]], None]):
        self.action = action

    def handle(self, content: str, url: str, enqueue_callback: Callable[[str, str], None]) -> None:
        self.action(content, url, enqueue_callback)


class FakeStateManager(StateManager):
    def __init__(self, queue_type = queue.Queue):
        self.queue = queue_type()

    def is_finished(self) -> bool:
        return self.queue.qsize() == 0

    def enqueue(self, url: str) -> None:
        self.queue.put_nowait(url)

    def pop_next(self) -> str:
        return self.queue.get_nowait()

    def mark_completed(self, url: str) -> None:
        pass


def test_crawl_root():
    f = FakeFetcher({'root': 'foo'})
    processed = []
    h = FakeHandler(lambda content, url, callback: processed.append(f'{url}: {content}'))

    Crawler(f, h, FakeStateManager(), ThrowingHandler()).crawl('root')

    assert processed == ['root: foo']


def test_crawl_discovered_pages_bfs():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz', 'c': 'qux', 'd': 'quux'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str, str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('', 'a')
            callback('', 'b')
        elif content == 'bar':
            callback('', 'c')
        elif content == 'baz':
            callback('', 'd')

    Crawler(f, FakeHandler(handle), FakeStateManager(), ThrowingHandler()).crawl('root')

    assert processed == ['root: foo', 'a: bar', 'b: baz', 'c: qux', 'd: quux']


def test_crawl_discovered_pages_dfs():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz', 'c': 'qux', 'd': 'quux'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str, str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('', 'a')
            callback('', 'b')
        elif content == 'bar':
            callback('', 'c')
        elif content == 'baz':
            callback('', 'd')

    Crawler(f, FakeHandler(handle), FakeStateManager(queue.LifoQueue), ThrowingHandler()).crawl('root')

    assert processed == ['root: foo', 'b: baz', 'd: quux', 'a: bar', 'c: qux']


def test_resolve_relative_urls():
    f = FakeFetcher(
        {'http://root.com/': 'foo', 'http://root.com/a': 'bar', 'http://root.com/b/': 'baz', 'http://root.com/c': 'qux',
         'http://root.com/b/d': 'quux', 'http://root.com/e': 'eranu'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str, str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('http://root.com/', 'a')
            callback('http://root.com/', 'b/')
        elif content == 'bar':
            callback('http://root.com/a', 'c')
        elif content == 'baz':
            callback('http://root.com/b/', 'd')
            callback('http://root.com/b/', '/e')

    Crawler(f, FakeHandler(handle), FakeStateManager(), ThrowingHandler()).crawl('http://root.com/')

    assert processed == ['http://root.com/: foo',
                         'http://root.com/a: bar',
                         'http://root.com/b/: baz',
                         'http://root.com/c: qux',
                         'http://root.com/b/d: quux',
                         'http://root.com/e: eranu']


def test_crawl_delay():
    f = FakeFetcher({'root': 'foo', 'a': 'bar', 'b': 'baz'})
    processed = []

    def handle(content: str, url: str, callback: Callable[[str, str], None]) -> None:
        processed.append(f'{url}: {content}')
        if content == 'foo':
            callback('', 'a')
            callback('', 'b')

    crawl_delay = datetime.timedelta(seconds=0.25)

    start = time.time()
    Crawler(f, FakeHandler(handle), FakeStateManager(), ThrowingHandler(), crawl_delay=crawl_delay).crawl('root')
    end = time.time()

    assert len(processed) == 3
    assert end - start > len(processed) * crawl_delay.total_seconds()


def test_error_fetching():
    f = FakeFetcher({}, ValueError('foo'))
    h = FakeHandler(lambda page, url, callback: None)

    with pytest.raises(ValueError, match='foo'):
        Crawler(f, h, FakeStateManager(), ThrowingHandler()).crawl('root')


def test_error_handling():
    f = FakeFetcher({'root': 'foo'})

    def handle(page: str, url: str, callback: Callable[[str, str], None]) -> None:
        raise ValueError('bar')

    with pytest.raises(ValueError, match='bar'):
        Crawler(f, FakeHandler(handle), FakeStateManager(), ThrowingHandler()).crawl('root')
