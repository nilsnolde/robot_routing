from typing import List, Iterator, Optional

from .rotatinglaser import RotatingLaser

__all__ = ['InfiniteCellGraph']

from .types import CellLocation, Wormholes


class InfiniteCellGraph:
    """
    A graph of uniform cells, from 0 at the SW corner to infinity in N & E.
    """
    def __init__(self, obstacles: List[CellLocation], wormholes: Wormholes, lasers: List[RotatingLaser]):
        super().__init__()
        self._obstacles = obstacles
        self._wormholes = wormholes
        self._lasers = lasers

    def _passable(self, cell: CellLocation) -> bool:
        """Determines whether the next step might be crossing a barrier or a laser"""
        passable = cell not in self._obstacles
        if not passable:
            return False
        # for laser in self._lasers:
        #     # First rotate to simulate the next time step
        #     laser.rotate()
        #     if laser.hits_cell(cell):
        #         passable = False
        #         break

        return passable

    def adjacent(self, cell: CellLocation) -> Iterator[CellLocation]:
        """
        Dynamically calculates the _valid_ neighbors of a :class:`CellLocation`
        which are not equal to a barrier or crossing a laser.
        """
        neighbors = [CellLocation(cell.x + 1, cell.y), CellLocation(cell.x - 1, cell.y),
                     CellLocation(cell.x, cell.y - 1), CellLocation(cell.x, cell.y + 1)]
        temp = filter(self._passable, neighbors)
        return filter(lambda x: x.x >= 0 and x.y >= 0, temp)

    def cost(self) -> float:
        """In this simple graph we have constant cost of 1 between adjacent cells."""
        return 1.0

    def wormhole(self, cell: CellLocation) -> Optional[CellLocation]:
        """Returns the destination of a wormhole if it exists at the passed cell."""
        return self._wormholes.get(cell)

