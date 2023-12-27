from typing import Callable, Optional

import json
import natsort
import os
import pathlib

from types import SimpleNamespace

class JsonLoader:
    """
    Loads all the numbered JSON files in a directory into a dict.
    """

    def __init__(self,
                 path: pathlib.Path,
                 filter: Optional[Callable[[str], bool]] = None):
        """
        path: path to directory containing numbered JSON files.
        filter: optional predicate returning true if base filename should be loaded.
        """
        self.path = path
        self.filter = filter

    def load(self):
        """
        Loads all the files in the relevant path ending in '.json' into a dictionary keyed
        by base filename.
        """
        results = {}
        for filename in natsort.natsorted(os.listdir(self.path)):
            if not filename[-5:] == '.json':
                continue
            id = filename[:-5]
            if self.filter is not None and not self.filter(id):
                continue
            results[id] = json.load(open(self.path / filename))
        return results