import pathlib
import queue
from typing import Dict, Optional, Set

from .state_manager import StateManager


class FileStateManager(StateManager):
    """
    Maintains crawl state using in-memory collections, which are also written to
    log files with one URL per line. This allows resuming the crawl if interrupted.
    """

    def __init__(self,
                 queue_type: type[queue.Queue],
                 visited_path: pathlib.Path,
                 queue_path: pathlib.Path,
                 queue_counter_path: pathlib.Path,
                 max_failures_per_url: int = 3):
        self._visited: Set[str] = set()
        self._queue = queue_type()
        self._queue_counter: int = 0
        self._in_progress: Optional[str] = None
        self._failed: Dict[str, int] = {}
        self._max_failures_per_url = max_failures_per_url

        try:
            self._visited_file = open(visited_path, 'r+')
            self._visited.update(set(self._visited_file.read().splitlines()))
        except FileNotFoundError:
            print(f'No existing checkpoint file at {visited_path}')
            self._visited_file = open(visited_path, 'a')  # Only ever visit more pages

        try:
            self._queue_counter_file = open(queue_counter_path, 'r+')
            self._queue_counter = int(self._queue_counter_file.read())
        except (FileNotFoundError, ValueError):
            print(f'No valid existing queue counter file at {visited_path}')
            self._queue_counter_file = open(queue_counter_path, 'w')  # Only ever visit more pages
            self._queue_counter_file.write(str(self._queue_counter))
            self._queue_counter_file.flush()

        try:
            self._queue_file = open(queue_path, 'r+')
            queue_lines = self._queue_file.read().splitlines()[self._queue_counter:]
            self._in_progress = next(iter(queue_lines), None)
            for url in queue_lines:
                self._queue.put(url)
        except FileNotFoundError:
            print(f'No existing queue file at {queue_path}')
            self._queue_file = open(queue_path, 'w')

    def _update_counter(self):
        self._queue_counter += 1
        self._queue_counter_file.seek(0)
        self._queue_counter_file.write(str(self._queue_counter))
        self._queue_counter_file.truncate()
        self._queue_counter_file.flush()

    def is_finished(self) -> bool:
        return self._queue.qsize() == 0

    def enqueue(self, url: str) -> None:
        if url in self._visited:
            return
        if url == self._in_progress:
            return
        if url in self._queue.queue:
            return
        if self._failed.get(url, 0) >= self._max_failures_per_url:
            return
        self._queue.put(url)
        self._queue_file.write(f'{url}\n')
        self._queue_file.flush()

    def pop_next(self) -> str:
        try:
            url = self._queue.get_nowait()
            self._in_progress = url
            return url
        except queue.Empty:
            raise IndexError('Cannot pop from empty queue')

    def mark_failed(self, url) -> None:
        if url != self._in_progress:
            return

        self._in_progress = None
        self._failed[url] = self._failed.get(url, 0) + 1
        self._update_counter()

    def mark_completed(self, url: str) -> None:
        if url != self._in_progress:
            return

        # We know we're finished with it. We do this here, and not
        # on popping, since otherwise a page can re-enqueue itself while
        # it is not on the queue, but before it has been marked visited.
        # Duplicate effort is bad.
        self._in_progress = None

        # Make sure we don't visit completed URL again.
        self._visited.add(url)
        self._visited_file.write(f'{url}\n')
        self._visited_file.flush()

        # Update queue log with the current state of the queue.
        # We only want to do this when a URL is done, since if we
        # abort while it is in progress, we'll want to do it again.
        # And since we can't guarantee `url` was even in the queue
        # (though it should be), it's safer and faster to just dump
        # the whole state, rather than try to find the entry to remove.
        self._update_counter()
