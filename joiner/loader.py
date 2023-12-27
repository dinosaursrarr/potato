from typing import Callable, Optional, Union

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
                 key_fn: Callable[[Union[dict, list], str], str],
                 filter_fn: Optional[Callable[[str], bool]] = None):
        """
        path: path to directory containing numbered JSON files.
        key_fn: function indicating how to extract a key for each entry from either the JSON or filename.
        filter_fn: optional predicate returning true if base filename should be loaded.
        """
        self.path = path
        self.key_fn = key_fn
        self.filter_fn = filter_fn

    def load(self):
        """
        Loads all the files in the relevant path ending in '.json' into a dictionary keyed
        by base filename.
        """
        results = {}
        for filename in natsort.natsorted(os.listdir(self.path)):
            if not filename[-5:] == '.json':
                continue
            if self.filter_fn is not None and not self.filter_fn(filename):
                continue
            j = json.load(open(self.path / filename))
            key = self.key_fn(j, filename)
            results[key] = j
        return results