import sqlite3

import pytest

from .sqlite_state_manager import SqlStateManager


def test_bad_database_path(tmp_path):
    with pytest.raises(sqlite3.OperationalError):
        SqlStateManager(tmp_path)


def test_pop_empty(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    with pytest.raises(IndexError, match="empty queue"):
        m.pop_next()


def test_is_finished_empty_queue(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    assert m.is_finished()


def test_not_finished_nonempty_queue(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    assert not m.is_finished()


def test_finished_queue_empty_again(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    m.pop_next()
    m.mark_completed('a')
    assert m.is_finished()


def test_enqueue_and_pop(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'a'
    m.mark_completed('a')
    assert m.pop_next() == 'b'
    m.mark_completed('b')
    assert m.pop_next() == 'c'


def test_enqueue_and_pop_lifo(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db", sort_order=SqlStateManager.SortOrder.LIFO)
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'c'
    m.mark_completed('c')
    assert m.pop_next() == 'b'
    m.mark_completed('b')
    assert m.pop_next() == 'a'


def test_cannot_enqueue_already_visited(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    m.pop_next()
    m.mark_completed('a')
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('c')

    assert m.pop_next() == 'b'
    m.mark_completed('b')
    assert m.pop_next() == 'c'


def test_cannot_enqueue_already_in_queue(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    m.enqueue('b')
    m.enqueue('a')
    assert m.pop_next() == 'a'

    m.mark_completed('a')
    assert m.pop_next() == 'b'

    m.mark_completed('b')
    with pytest.raises(IndexError, match="empty queue"):
        m.pop_next()


def test_cannot_enqueue_in_progress_page(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    assert m.pop_next() == 'a'
    m.enqueue('a')
    m.mark_completed('a')

    with pytest.raises(IndexError, match="empty queue"):
        m.pop_next()


def test_can_enqueue_after_failure(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db")
    m.enqueue('a')
    m.pop_next()
    m.mark_failed('a')
    m.enqueue('a')

    assert m.pop_next() == 'a'


def test_cannot_enqueue_after_too_many_failures(tmp_path):
    m = SqlStateManager(tmp_path / "queue.db", max_failures_per_url=1)
    m.enqueue('a')
    m.pop_next()
    m.mark_failed('a')

    m.enqueue('a')
    with pytest.raises(IndexError, match='empty queue'):
        m.pop_next()


def test_can_restore_from_disk(tmp_path):
    db_path = tmp_path / "queue.db"
    m = SqlStateManager(db_path)

    m2 = SqlStateManager(db_path)
    with pytest.raises(IndexError, match='empty queue'):
        m2.pop_next()

    m.enqueue('a')
    m.pop_next()
    m.mark_completed('a')
    m3 = SqlStateManager(db_path)
    with pytest.raises(IndexError, match='empty queue'):
        m3.pop_next()

    m.enqueue('b')
    m.pop_next()
    m.mark_completed('b')
    m4 = SqlStateManager(db_path)
    with pytest.raises(IndexError, match='empty queue'):
        m4.pop_next()

    m.enqueue('c')
    m.enqueue('d')
    m5 = SqlStateManager(db_path)
    assert m5.pop_next() == 'c'
    m.mark_completed('c')
    assert m5.pop_next() == 'd'


def test_do_not_update_disk_on_pop(tmp_path):
    db_path = tmp_path / "queue.db"
    m = SqlStateManager(db_path)
    m.enqueue('a')

    m.pop_next()

    m2 = SqlStateManager(db_path)
    assert m2.pop_next() == 'a'


def test_update_disk_on_mark_completed(tmp_path):
    db_path = tmp_path / "queue.db"
    m = SqlStateManager(db_path)
    m.enqueue('a')
    m.pop_next()

    m.mark_completed('a')

    m2 = SqlStateManager(db_path)
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()


def test_update_disk_on_mark_failed(tmp_path):
    db_path = tmp_path / "queue.db"
    m = SqlStateManager(db_path)
    m.enqueue('a')

    m.mark_failed('a')

    m2 = SqlStateManager(db_path, max_failures_per_url=1)
    with pytest.raises(IndexError, match="empty queue"):
        m2.pop_next()
