from typing import Dict, List, Set

from .extractor import Extractor, Name, Namespace, Signal, SignalName


_COORDINATES = "coordinates"
_NAME = "name"
_PARENTAGE = "parentage"


class ParentageExtractor(Extractor):
    """
    Extract details of which breeds are parents and children of other breeds according
    to the Potato Pedigree database.
    """
    def __init__(self, pedigrees: List[Dict[str, object]]):
        self.pedigrees = pedigrees


    class _ChildNode:
        def __init__(self, name):
            self.name = name
            self.left_parent: '_ChildNode' = None
            self.right_parent: '_ChildNode' = None


    def _dfs(self,
             coords: Dict[int, Dict[int, '_ChildNode']],
             root: '_ChildNode',
             x: int,
             y: int,
             y_diff: int,
             x_offset: int,
             results: Dict[str, List[Signal]]) -> None:
        """
        Recursively identify parents (and hence children) of each breed.
        """
        next_x = x + x_offset
        if next_x not in coords:
            return
        for next_y in (y - y_diff, y + y_diff):
            parent = coords[next_x].get(next_y)
            if not parent:
                continue
            if parent.name == 'unknown':
                continue
            parent_name = Name(parent.name, Namespace.PEDIGREE)
            if parent_name not in results:
                results[parent_name] = []
            results[parent_name].append(Signal(SignalName.PARENT_OF, root.name))
            root_name = Name(root.name, Namespace.PEDIGREE)
            if root_name not in results:
                results[root_name] = []
            results[root_name].append(Signal(SignalName.CHILD_OF, parent.name))
            self._dfs(coords, parent, next_x, next_y, y_diff // 2, x_offset, results)


    def _extract_parents(self, pedigree) -> Dict[str, List[Signal]]:
        # Identify dimensions of the image map being processed.
        if _PARENTAGE not in pedigree:
            return {}
        if len(pedigree[_PARENTAGE]) < 2:
            return {}
        first = pedigree[_PARENTAGE][0]
        second = pedigree[_PARENTAGE][1]
        if _COORDINATES not in first or _COORDINATES not in second:
            return {}
        if len(first[_COORDINATES]) != 4 or len(second[_COORDINATES]) != 4:
            return {}
        x_offset = second[_COORDINATES][0] - first[_COORDINATES][0]
        y_offset = (first[_COORDINATES][3] - first[_COORDINATES][1]) // 2

        # Reify all the available entries
        coords = {}
        for p in pedigree[_PARENTAGE]:
            c = p[_COORDINATES]
            if len(c) != 4:
                continue
            x = c[0]
            y = c[1] + y_offset
            if x not in coords:
                coords[x] = {}
            coords[x][y] = self._ChildNode(p[_NAME])

        # Recreate tree structure from graph based on bifurcating locations.
        current_x = 0
        current_y = list(coords[0].keys())[0]
        root = coords[current_x][current_y]
        result = {}

        self._dfs(coords, root, current_x, current_y, current_y // 2, x_offset, result)
        return result


    def extract(self) -> Dict[Name, List[Signal]]:
        result = {}
        for pedigree in self.pedigrees:
            res = self._extract_parents(pedigree)
            for k, v in res.items():
                if k not in result:
                    result[k] = []
                result[k] += v

        for k, v in result.items():
            result[k] = list(set(v))
        return result