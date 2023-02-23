from enum import Enum
import pathlib
import sqlite3
import datetime

from .state_manager import StateManager


class SqlStateManager(StateManager):
    """
    Maintains crawl state using an embedded SQLite database. This should perform
    reasonably well as there is no inter-process communication and support resuming.
    """

    SortOrder = Enum('SortOrder', ['FIFO', 'LIFO'])

    def __init__(self,
                 database_path: pathlib.Path,
                 sort_order: SortOrder = SortOrder.FIFO,
                 max_failures_per_url: int = 3):
        self._sort_order = sort_order
        self._max_failures_per_url = max_failures_per_url
        self._db = sqlite3.connect(database_path)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS queue (
              url string PRIMARY KEY,
              visited boolean NOT NULL,
              failures smallint NOT NULL,
              enqueue_time timestamp NOT NULL
            )""")
        self._db.commit()

    def is_finished(self) -> bool:
        try:
            self.pop_next()
            return False
        except IndexError:
            return True

    def enqueue(self, url: str) -> None:
        try:
            self._db.execute("INSERT INTO queue VALUES(?, ?, ?, ?)",
                             (url, False, 0, datetime.datetime.now()))
            self._db.commit()
        except sqlite3.IntegrityError:
            pass

    def _sortorder(self) -> str:
        if self._sort_order == SqlStateManager.SortOrder.FIFO:
            return "ASC"
        if self._sort_order == SqlStateManager.SortOrder.LIFO:
            return "DESC"

    def pop_next(self) -> str:
        res = self._db.execute(f"""
            SELECT url
            FROM queue
            WHERE
                (NOT visited)
                AND failures < {self._max_failures_per_url}
            ORDER BY enqueue_time {self._sortorder()}
            LIMIT 1
        """).fetchone()
        if res:
            return res[0]
        raise IndexError('Cannot pop from empty queue')

    def mark_failed(self, url) -> None:
        self._db.execute("""
            UPDATE queue
            SET
                failures = failures + 1,
                enqueue_time = ?
            WHERE url = ?
        """, (datetime.datetime.now(), url))
        self._db.commit()

    def mark_completed(self, url: str) -> None:
        self._db.execute("""
                        UPDATE queue
                        SET visited = true
                        WHERE url = ?
                    """, (url,))
        self._db.commit()
