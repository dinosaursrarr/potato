import abc
import logging
from typing import Callable


class ErrorHandler(abc.ABC):
    """
    Interface for determining how crawl errors are handled.
    """

    @abc.abstractmethod
    def handle(self, err: Exception, retry_callback: Callable[[], None]) -> None:
        """
        :param err: The exception to be handled.
        :param retry_callback: Callback to add the failed task back to the queue if desired.
        """
        raise NotImplementedError('Cannot handle from abstract base class ErrorHandler')


class ThrowingHandler(ErrorHandler):
    """
    Throws all exceptions, which is likely to stop the crawl immediately. Does not retry failed URLs.
    """

    def handle(self, err: Exception, retry_callback: Callable[[], None]) -> None:
        raise err


class LoggingHandler(ErrorHandler):
    """
    Logs all exceptions and continues. Does not retry failed URLs.
    """

    def handle(self, err: Exception, retry_callback: Callable[[], None]) -> None:
        logging.getLogger(type(self).__name__).error(err)


class RetryingHandler(ErrorHandler):
    """
    Uses callback to add failed URL back to the queue, then delegates to other handler.
    """

    def __init__(self, handler: ErrorHandler):
        self.handler = handler

    def handle(self, err: Exception, retry_callback: Callable[[], None]) -> None:
        retry_callback()
        self.handler.handle(err, retry_callback)
