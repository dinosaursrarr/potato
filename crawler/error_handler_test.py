import pytest

from .error_handler import LoggingHandler, ThrowingHandler, RetryingHandler


def noop_callback():
    pass


def test_throwing():
    with pytest.raises(ValueError, match='foo'):
        ThrowingHandler().handle(ValueError('foo'), noop_callback)


def test_logging(caplog):
    LoggingHandler().handle(ValueError('foo'), noop_callback)
    assert 'foo' in caplog.text


def test_retrying(caplog):
    output = []

    def callback() -> None:
        output.append('bar')

    RetryingHandler(LoggingHandler()).handle(ValueError('foo'), callback)

    assert output == ['bar']
    assert 'foo' in caplog.text
