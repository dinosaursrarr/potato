import pathlib
import queue

import pytest

from .file_state_manager import FileStateManager


def test_bad_visited_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        FileStateManager(queue.Queue, pathlib.Path(tmp_path), tmp_path / "queue.log")


def test_bad_queue_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        FileStateManager(queue.Queue, tmp_path / "visited.log", pathlib.Path(tmp_path))


def test_pop_empty(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    with pytest.raises(IndexError, match="empty queue"):
        m.pop_next()


def test_is_finished_empty_queue(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    assert m.is_finished()


def test_not_finished_nonempty_queue(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    m.enqueue('a')
    assert not m.is_finished()


def test_finished_queue_empty_again(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    m.enqueue('a')
    m.pop_next()
    assert m.is_finished()


def test_enqueue_and_pop(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'a'
    assert m.pop_next() == 'b'
    assert m.pop_next() == 'c'


def test_enqueue_and_pop_lifo(tmp_path):
    m = FileStateManager(queue.LifoQueue, tmp_path / "visited.log", tmp_path / "queue.log")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'c'
    assert m.pop_next() == 'b'
    assert m.pop_next() == 'a'


def test_cannot_enqueue_already_visited(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log")
    m.mark_completed('a')
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'b'
    assert m.pop_next() == 'c'


def test_cannot_enqueue_already_in_queue(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('a')

    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == ['a', 'b']


def test_cannot_enqueue_in_progress_page(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)
    m.enqueue('a')
    assert m.pop_next() == 'a'
    m.enqueue('a')
    m.mark_completed('a')

    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == []


def test_write_visited_log(tmp_path):
    log_path = tmp_path / "visited.log"
    m = FileStateManager(queue.Queue, log_path, tmp_path / "queue.log")
    with open(log_path, 'r') as f:
        assert f.read().splitlines() == []

    m.mark_completed('a')
    with open(log_path, 'r') as f:
        assert f.read().splitlines() == ['a']

    m.mark_completed('b')
    with open(log_path, 'r') as f:
        assert f.read().splitlines() == ['a', 'b']


def test_write_queue_log(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)
    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == []

    m.enqueue('a')
    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == ['a']

    m.enqueue('b')
    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == ['a', 'b']


def test_do_not_update_queue_log_on_pop(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)
    m.enqueue('a')

    m.pop_next()

    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == ['a']


def test_update_queue_log_on_mark_completed(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)
    m.enqueue('a')

    m.pop_next()
    m.mark_completed('a')

    with open(queue_path, 'r') as f:
        assert f.read().splitlines() == []


def test_restore_visited_log(tmp_path):
    log_path = tmp_path / "visited.log"
    with open(log_path, 'w') as f:
        f.writelines([
            'a\n',
            'b\n',
        ])
    m = FileStateManager(queue.Queue, log_path, tmp_path / "queue.log")

    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'c'


def test_restore_queue_log(tmp_path):
    queue_path = tmp_path / "queue.log"
    with open(queue_path, 'w') as f:
        f.writelines([
            'a\n',
            'b\n',
        ])
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path)

    assert m.pop_next() == 'a'
    assert m.pop_next() == 'b'
