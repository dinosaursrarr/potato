import pytest
import pytest_httpbin
import pytest_httpbin.certs
import requests

from . import http_fetcher


def test_fetch_http(httpbin):
    fetcher = http_fetcher.HttpFetcher()
    response = fetcher.fetch(httpbin.url + '/get')
    assert isinstance(response, str)
    assert len(response) > 0


def test_send_user_agent(httpbin):
    fetcher = http_fetcher.HttpFetcher(user_agent='foo')
    response = fetcher.fetch(httpbin.url + '/headers')
    assert '"User-Agent":"foo"' in response


def test_raise_on_empty_url():
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ValueError, match='empty'):
        fetcher.fetch('')


def test_raise_on_no_url():
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ValueError, match='empty'):
        fetcher.fetch(None)


def test_raise_on_bad_protocol():
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(NotImplementedError, match='Cannot fetch'):
        fetcher.fetch('ftp://example.com')


def test_raise_on_connection_error(httpbin):
    fetcher = http_fetcher.HttpFetcher(timeout_seconds=0.001)
    with pytest.raises(ConnectionError, match='Failed to establish'):
        fetcher.fetch('http://127.0.0.1')


def test_raise_on_too_many_redirects(httpbin):
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ConnectionError, match='redirects'):
        fetcher.fetch(httpbin.url + f'/redirect/{requests.models.DEFAULT_REDIRECT_LIMIT + 1}')


def test_raise_on_http_error(httpbin):
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ConnectionError, match='404 Client Error'):
        fetcher.fetch(httpbin.url + '/status/404')


def test_raise_on_timeout(httpbin):
    fetcher = http_fetcher.HttpFetcher(timeout_seconds=0.001)
    with pytest.raises(TimeoutError, match='timed out'):
        fetcher.fetch(httpbin.url + f'/delay/0.002')


def test_fetch_https(httpbin_secure, monkeypatch):
    monkeypatch.setenv('REQUESTS_CA_BUNDLE', pytest_httpbin.certs.where())
    fetcher = http_fetcher.HttpFetcher()
    response = fetcher.fetch(httpbin_secure.url + '/get')
    assert isinstance(response, str)
    assert len(response) > 0


def test_send_user_agent_https(httpbin_secure, monkeypatch):
    monkeypatch.setenv('REQUESTS_CA_BUNDLE', pytest_httpbin.certs.where())
    fetcher = http_fetcher.HttpFetcher(user_agent='foo')
    response = fetcher.fetch(httpbin_secure.url + '/headers')
    assert '"User-Agent":"foo"' in response


def test_raise_on_too_many_redirects_https(httpbin_secure, monkeypatch):
    monkeypatch.setenv('REQUESTS_CA_BUNDLE', pytest_httpbin.certs.where())
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ConnectionError, match='redirects'):
        fetcher.fetch(httpbin_secure.url + f'/redirect/{requests.models.DEFAULT_REDIRECT_LIMIT + 1}')


def test_raise_on_https_error(httpbin_secure, monkeypatch):
    monkeypatch.setenv('REQUESTS_CA_BUNDLE', pytest_httpbin.certs.where())
    fetcher = http_fetcher.HttpFetcher()
    with pytest.raises(ConnectionError, match='404 Client Error'):
        fetcher.fetch(httpbin_secure.url + '/status/404')


def test_raise_on_timeout(httpbin_secure, monkeypatch):
    monkeypatch.setenv('REQUESTS_CA_BUNDLE', pytest_httpbin.certs.where())
    fetcher = http_fetcher.HttpFetcher(timeout_seconds=0.001)
    with pytest.raises(TimeoutError, match='timed out'):
        fetcher.fetch(httpbin_secure.url + f'/delay/0.002')
