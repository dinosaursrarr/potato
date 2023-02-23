import queue

import pytest

from .file_state_manager import FileStateManager


def test_bad_visited_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        FileStateManager(queue.Queue, tmp_path, tmp_path / "queue.log", tmp_path / "counter.log")


def test_bad_queue_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path, tmp_path / "counter.log")


def test_bad_queue_counter_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path)


def test_pop_empty(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    with pytest.raises(IndexError, match="empty queue"):
        m.pop_next()


def test_is_finished_empty_queue(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    assert m.is_finished()


def test_not_finished_nonempty_queue(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    m.enqueue('a')
    assert not m.is_finished()


def test_finished_queue_empty_again(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    m.enqueue('a')
    m.pop_next()
    assert m.is_finished()


def test_enqueue_and_pop(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'a'
    assert m.pop_next() == 'b'
    assert m.pop_next() == 'c'


def test_enqueue_and_pop_lifo(tmp_path):
    m = FileStateManager(queue.LifoQueue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'c'
    assert m.pop_next() == 'b'
    assert m.pop_next() == 'a'


def test_cannot_enqueue_already_visited(tmp_path):
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", tmp_path / "queue.log", tmp_path / "counter.log")
    m.enqueue('a')
    m.pop_next()
    m.mark_completed('a')
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'b'
    assert m.pop_next() == 'c'


def test_cannot_enqueue_already_in_queue(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('a')

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    assert m2.pop_next() == 'a'
    assert m2.pop_next() == 'b'
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()


def test_cannot_enqueue_in_progress_page(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    m.enqueue('a')
    assert m.pop_next() == 'a'
    m.enqueue('a')
    m.mark_completed('a')

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()


def test_can_enqueue_after_failure(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path, tmp_path / "counter.log",
                         max_failures_per_url=2)
    m.enqueue('a')
    m.pop_next()
    m.mark_failed('a')
    m.enqueue('a')

    assert m.pop_next() == 'a'


def test_cannot_enqueue_after_too_many_failures(tmp_path):
    queue_path = tmp_path / "queue.log"
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path, tmp_path / "counter.log",
                         max_failures_per_url=1)
    m.enqueue('a')
    m.pop_next()
    m.mark_failed('a')

    m.enqueue('a')
    with pytest.raises(IndexError, match='empty queue'):
        m.pop_next()


def test_can_restore_from_disk(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match='empty queue'):
        m2.pop_next()

    m.enqueue('a')
    m.pop_next()
    m.mark_completed('a')
    m3 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match='empty queue'):
        m3.pop_next()

    m.enqueue('b')
    m.pop_next()
    m.mark_completed('b')
    m4 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match='empty queue'):
        m4.pop_next()

    m.enqueue('c')
    m.enqueue('d')
    m5 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    assert m5.pop_next() == 'c'
    assert m5.pop_next() == 'd'


def test_do_not_update_disk_on_pop(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    m.enqueue('a')

    m.pop_next()

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    assert m2.pop_next() == 'a'


def test_update_disk_on_mark_completed(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    m.enqueue('a')
    m.pop_next()

    m.mark_completed('a')

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()


def test_update_disk_on_mark_failed(tmp_path):
    visited_path = tmp_path / "visited.log"
    queue_path = tmp_path / "queue.log"
    counter_path = tmp_path / "counter.log"
    m = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    m.enqueue('a')
    m.pop_next()

    m.mark_failed('a')

    m2 = FileStateManager(queue.Queue, visited_path, queue_path, counter_path)
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()


def test_restore_visited_log(tmp_path):
    log_path = tmp_path / "visited.log"
    with open(log_path, 'w') as f:
        f.writelines([
            'a\n',
            'b\n',
        ])
    m = FileStateManager(queue.Queue, log_path, tmp_path / "queue.log", tmp_path / "counter.log")

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
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path, tmp_path / "counter.log")

    assert m.pop_next() == 'a'
    assert m.pop_next() == 'b'


def test_restore_queue_log_with_counter(tmp_path):
    queue_path = tmp_path / "queue.log"
    with open(queue_path, 'w') as f:
        f.writelines([
            'a\n',
            'b\n',
        ])
    counter_path = tmp_path / "counter.log"
    with open(counter_path, 'w') as f:
        f.write('1')
    m = FileStateManager(queue.Queue, tmp_path / "visited.log", queue_path, counter_path)

    assert m.pop_next() == 'b'
