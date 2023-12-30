from typing import Dict, List

from .extractor import Extractor, Name, Namespace, Signal, SignalName

_NAME = "name"
_PARENTAGE = "parentage"
_YEAR = "year_of_introduction"


class IntroductionExtractor(Extractor):
    """
    Extract details of the year each variety was introducted, according to the Potato
    Pedigree database.
    """
    def __init__(self, pedigrees: List[Dict[str, object]]):
        self.pedigrees = pedigrees

    def extract(self) -> Dict[Name, List[Signal]]:
        years: Dict[str, int] = {}
        for pedigree in self.pedigrees:
            if _PARENTAGE not in pedigree:
                continue
            for parentage in pedigree[_PARENTAGE]:
                if _YEAR not in parentage:
                    continue
                if _NAME not in parentage:
                    continue
                if not isinstance(parentage[_YEAR], int):
                    continue
                years[parentage[_NAME]] = parentage[_YEAR]

        return {
            Name(k, Namespace.PEDIGREE): [Signal(SignalName.YEAR_OF_INTRODUCTION, v)]
            for k, v in years.items()
        }