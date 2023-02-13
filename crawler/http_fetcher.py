import requests

import fetcher


class HttpFetcher(fetcher.Fetcher):
    """
    Fetches pages from URLs over HTTP or HTTPs.
    """

    def __init__(self, user_agent: str = '', timeout_seconds: float = 1.0):
        self.user_agent = user_agent
        self.timeout_seconds = timeout_seconds

    def fetch(self, url) -> str:
        """
        :param url: An HTTP or HTTPs URL to be fetched. Redirects will be followed.
        :return: The raw content of the fetched URL, as a string.
        """
        if not url:
            raise ValueError('Cannot fetch empty URL')
        try:
            headers = {}
            if self.user_agent:
                headers['User-Agent'] = self.user_agent
            response = requests.get(
                url,
                timeout=self.timeout_seconds,
                headers=headers)
            response.raise_for_status()  # If it didn't work
            return response.text
        except requests.exceptions.InvalidSchema:
            raise NotImplementedError('Cannot fetch non-HTTP url: ' + url)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(e)
        except requests.exceptions.TooManyRedirects as e:
            raise ConnectionError(e)
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(e)
        except requests.exceptions.Timeout as e:
            raise TimeoutError(e)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(e)
