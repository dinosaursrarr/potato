import datetime
import time
import urllib.parse
from typing import Callable

from .error_handler import ErrorHandler
from .fetcher import Fetcher
from .handler import Handler
from .state_manager import StateManager


class Crawler:
    """
    Framework for crawling URLs beginning at a certain root, and adding new URLs
    as they are discovered.

    This class is generic and handles the orchestration logic. It delegates to
    handlers for fetching URLs, processing their content, and handling errors.
    """

    def __init__(self,
                 fetcher: Fetcher,
                 handler: Handler,
                 state_manager: StateManager,
                 error_handler: ErrorHandler,
                 crawl_delay: datetime.timedelta = datetime.timedelta(0)):
        """
        :param fetcher: Fetcher to be used to fetch URLs.
        :param handler: Handler to process fetched URLs.
        :param state_manager: Manages the crawl queue.
        :param error_handler: Determines how any errors raised during crawl are handled.
        :param crawl_delay: Specifies how long to wait before making each request.
        """
        self.fetcher = fetcher
        self.handler = handler
        self.state_manager = state_manager
        self.error_handler = error_handler
        self.crawl_delay = crawl_delay

    def _enqueue_fn(self) -> Callable[[str, str], None]:
        """
        Enqueues new URLs while ensuring we do not revisit pages seen already. URLs can be
        relative to the current URL, or absolute.
        :return: Function that adds a URL to the queue if it has not been seen before.
        """

        def put_fn(current_url, new_url: str) -> None:
            # Resolves relative URLs relative to the current URL. If new_url is
            # absolute, then current_url will be ignored.
            url = urllib.parse.urljoin(current_url, new_url)
            self.state_manager.enqueue(url)

        return put_fn

    def _retry_fn(self, url: str) -> Callable[[], None]:
        def retry_fn() -> None:
            return self._enqueue_fn()('', url)

        return retry_fn

    def crawl(self, root: str) -> None:
        """
        Initiates a crawl beginning at a given URL and continuing until there are
        no more pages to discover.
        :param root: URL from which to begin crawling
        """

        # TODO: Check constraints from robot.txt before starting.
        self.state_manager.enqueue(root)

        # TODO: Multithreading to parallelize.
        while not self.state_manager.is_finished():
            url = self.state_manager.pop_next()
            time.sleep(self.crawl_delay.total_seconds())
            try:
                content = self.fetcher.fetch(url)
                self.handler.handle(content, url, self._enqueue_fn())
            except Exception as e:
                self.error_handler.handle(e, self._retry_fn(url))
            finally:
                self.state_manager.mark_completed(url)
