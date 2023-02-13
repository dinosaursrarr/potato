import queue
from typing import Callable, Set

import fetcher
import handler


class Crawler:
    """
    Framework for crawling URLs beginning at a certain root, and adding new URLs
    as they are discovered.

    This class is generic and handles the orchestration logic. It delegates to
    handlers for fetching URLs, processing their content, and handling errors.
    """

    def __init__(self, fetcher_impl: fetcher.Fetcher,
                 handler_impl: handler.Handler, queue_type: type[queue.Queue]):
        """
        :param fetcher_impl: Fetcher to be used to fetch URLs.
        :param handler_impl: Handler to process fetched URLs.
        :param queue_type: Use queue.Queue for BFS or queue.LifoQueue for DFS.
        """
        self.fetcher = fetcher_impl
        self.handler = handler_impl
        self.queue_type = queue_type
        self.visited = set()

    def _enqueue_fn(self, q: queue.Queue, visited: Set[str]) -> Callable[[str], None]:
        """
        Enqueues new URLs while ensuring we do not revisit pages seen already.
        :param q: Queue to which to add URLs.
        :param visited: Collection of URLs that have already been added to the queue.
        :return: Function that adds a URL to the queue if it has not been
        seen before.
        """

        def put_fn(url: str) -> None:
            if url in visited:
                return
            visited.add(url)
            q.put(url)

        return put_fn

    def crawl(self, root: str) -> None:
        """
        Initiates a crawl beginning at a given URL and continuing until there are
        no more pages to discover.
        :param root: URL from which to begin crawling
        """
        q = self.queue_type()
        visited = set()

        # TODO: Check constraints from robot.txt before starting.
        q.put(root)
        visited.add(root)

        # TODO: Multithreading to parallelize.
        # TODO: Handle errors raised during crawl.
        while q.qsize() > 0:
            url = q.get()
            page = self.fetcher.fetch(url)
            self.handler.handle(page, self._enqueue_fn(q, visited))
            q.task_done()
