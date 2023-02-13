import abc
from typing import Callable


class Handler(abc.ABC):
    """
    Interface for doing something with fetched content, such as:
     - extracting key information.
     - writing data to some output.
     - updating counters or other monitoring.
     - determining other pages to be crawled.
     - adding other pages to the crawl queue.
    """

    @abc.abstractmethod
    def handle(self, page: str, enqueue_callback: Callable[[str], None]) -> None:
        """
        :param page: Raw content to be processed, as a string.
        :param enqueue_callback: Callback to add a newly discovered URL to the crawl queue.
        """
        raise NotImplementedError('Cannot handle from abstract base class Handler')
