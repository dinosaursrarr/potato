import abc

from enum import Enum
from typing import Dict, List, NamedTuple, Union


class Namespace(Enum):
    EUROPOTATO = 1
    PEDIGREE = 2


class Name(NamedTuple):
    name: str
    namespace: Namespace


class SignalName(Enum):
    PARENT_OF = 1
    CHILD_OF = 2
    YEAR_OF_INTRODUCTION = 3
    PEDIGREE_NAME = 4
    EUROPOTATO_NAME = 5


class Signal(NamedTuple):
    name: SignalName
    value: Union[str, int, float]


class Extractor(abc.ABC):
    """
    Interface for extracting signals from crawl results.
    """

    @abc.abstractmethod
    def extract(self) -> Dict[Name, List[Signal]]:
        """
        :return: Dictionary with value of a given signal for each entity.
        """
        raise NotImplementedError('Cannot fetch from abstract base class Extractor')
