import pathlib
import queue
from typing import Dict, Set

from .state_manager import StateManager


class FileStateManager(StateManager):
    """
    Maintains crawl state using in-memory collections, which are also written to
    log files with one URL per line. This allows resuming the crawl if interrupted.
    """

    def __init__(self, queue_type: type[queue.Queue], visited_path: pathlib.Path, queue_path: pathlib.Path,
                 max_failures_per_url: int = 3):
        self._visited: Set[str] = set()
        self._queue = queue_type()
        self._in_progress: Set[str] = set()
        self._failed: Dict[str, int] = {}
        self._max_failures_per_url = max_failures_per_url

        try:
            self._visited_file = open(visited_path, 'r+')
            self._visited.update(set(self._visited_file.read().splitlines()))
        except FileNotFoundError:
            print(f'No existing checkpoint file at {visited_path}')
            self._visited_file = open(visited_path, 'a')  # Only ever visit more pages

        try:
            self._queue_file = open(queue_path, 'r+')
            for url in self._queue_file.read().splitlines():
                self._in_progress.add(url)
                self._queue.put(url)
        except FileNotFoundError:
            print(f'No existing queue file at {queue_path}')
            self._queue_file = open(queue_path, 'w')

    def is_finished(self) -> bool:
        return self._queue.qsize() == 0

    def enqueue(self, url: str) -> None:
        if url in self._visited:
            return
        if url in self._in_progress:
            return
        if self._failed.get(url, 0) >= self._max_failures_per_url:
            return
        self._in_progress.add(url)
        self._queue.put(url)
        self._queue_file.write(f'{url}\n')
        self._queue_file.flush()

    def pop_next(self) -> str:
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            raise IndexError('Cannot pop from empty queue')

    def mark_failed(self, url) -> None:
        if url not in self._in_progress:
            return

        self._in_progress.discard(url)
        self._failed[url] = self._failed.get(url, 0) + 1

    def mark_completed(self, url: str) -> None:
        if url not in self._in_progress:
            return

        # We know we're finished with it. We do this here, and not
        # on popping, since otherwise a page can re-enqueue itself while
        # it is not on the queue, but before it has been marked visited.
        # Duplicate effort is bad.
        self._in_progress.discard(url)

        # Make sure we don't visit completed URL again.
        self._visited.add(url)
        self._visited_file.write(f'{url}\n')
        self._visited_file.flush()

        # Update queue log with the current state of the queue.
        # We only want to do this when a URL is removed done,
        # since if we abort while it is in progress,  we'll want to
        # do it again. And since we can't guarantee `url` was even
        # in the queue (though it should be), it's safer and faster
        # to just dump the whole state, rather than try to find the
        # entry to remove.
        self._queue_file.seek(0)
        self._queue_file.writelines([f'{url}\n' for url in self._queue.queue])
        self._queue_file.truncate()
        self._queue_file.flush()
