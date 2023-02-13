import pytest

import error_handler


def noop_callback():
    pass


def test_throwing():
    h = error_handler.ThrowingHandler()
    with pytest.raises(ValueError, match='foo'):
        h.handle(ValueError('foo'), noop_callback)


def test_logging(caplog):
    h = error_handler.LoggingHandler()
    h.handle(ValueError('foo'), noop_callback)
    assert 'foo' in caplog.text


def test_retrying(caplog):
    output = []

    def callback() -> None:
        output.append('bar')

    h = error_handler.RetryingHandler(error_handler.LoggingHandler())
    h.handle(ValueError('foo'), callback)

    assert output == ['bar']
    assert 'foo' in caplog.text
