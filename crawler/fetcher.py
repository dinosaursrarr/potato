import abc


class Fetcher(abc.ABC):
    """
    Interface for fetching content from some source URL.
    """

    @abc.abstractmethod
    def fetch(self, url: str) -> str:
        """
        :param url: The URL to be fetched.
        :return: The raw content of the fetched URL, as a string.
        """
        raise NotImplementedError('Cannot fetch from abstract base class Fetcher')
