import abc

from enum import Enum
from typing import Dict, List, NamedTuple, Union


class SignalName(Enum):
    PARENT_OF = 1
    CHILD_OF = 2
    YEAR_OF_INTRODUCTION = 3


class Signal(NamedTuple):
    name: SignalName
    value: Union[str, int, float]


class Extractor(abc.ABC):
    """
    Interface for extracting signals from crawl results.
    """

    @abc.abstractmethod
    def extract(self) -> Dict[str, List[Signal]]:
        """
        :return: Dictionary with value of a given signal for each entity.
        """
        raise NotImplementedError('Cannot fetch from abstract base class Extractor')
