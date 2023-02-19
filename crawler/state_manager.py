import abc


class StateManager(abc.ABC):
    """
    Interface for keeping track of crawl state, and ensuring we can resume
    gracefully after a restart. Expects the following lifecycle for a given URL:
     - enqueue() when discovered.
     - pop_next() when it is time to be crawled.
     - mark_completed() after it has been crawled.
    """
    def enqueue(self, url: str) -> None:
        """
        Adds url to the list of URLs to be crawled.
        :param url: URL to be added to the crawl queue.
        """
        raise NotImplementedError('Cannot call enqueue on abstract base class Checkpointer')

    def pop_next(self) -> str:
        """
        Retrieves the next URL that should be visited.
        :return: The next URL to be crawled.
        """

    def mark_completed(self, url: str) -> None:
        """
        Updates crawl state so that we know `url` has been processed.
        :param url: URL to be marked completed.
        """
        raise NotImplementedError('Cannot call mark_completed on abstract base class Checkpointer')