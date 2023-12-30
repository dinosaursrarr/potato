from typing import Dict, List

from .extractor import Extractor, Name, Namespace, Signal, SignalName

_NAME = "name"


class PedigreeNameExtractor(Extractor):
    """
    Extracts name of a given entry in the Potato Pedigree database.
    """
    def __init__(self, pedigrees: List[Dict[str, object]]):
        self.pedigrees = pedigrees

    def extract(self) -> Dict[Name, List[Signal]]:
        return {
            Name(p[_NAME], Namespace.PEDIGREE): [Signal(SignalName.PEDIGREE_NAME, p[_NAME])]
            for p in self.pedigrees if _NAME in p
        }


class EuropotatoPedigreeNameExtractor(Extractor):
    """
    Extracts expected name of a potato breed in the Europotato database
    according to the Potato Pedigree database.
    """
    def __init__(self,
        pedigrees: Dict[str, Dict[str, object]],
        name_map: Dict[str, str]):
        
        self.pedigrees = pedigrees
        self.name_map = name_map

    def extract(self) -> Dict[Name, List[Signal]]:
        results = {}
        for filename, europotato_name in self.name_map.items():
            if not europotato_name:
                continue
            pedigree = self.pedigrees.get(filename + '.json')
            if not pedigree:
                continue
            pedigree_name = pedigree.get(_NAME)
            if not pedigree_name:
                continue
            results[Name(pedigree_name, Namespace.PEDIGREE)] = [
                Signal(SignalName.EUROPOTATO_NAME, europotato_name)
            ]
        return results
