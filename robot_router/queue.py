from queue import PriorityQueue as _PriorityQueue
from typing import Tuple

from .types import CellLocation

__all__ = ['PriorityQueue']


# tuple(priority, coord tuple)
QueueItem = Tuple[float, CellLocation]


class PriorityQueue(_PriorityQueue):
    """Reimplementation of :class:`queue.PriorityQueue` without blocking."""

    def put(self, item: QueueItem, **kwargs):
        """
        Put a :class:`QueueItem` into the queue. No support for altering
        priorities of existing elements, so it produces duplicates, i.e. RAM.
        """
        return super().put(item, False)

    def get(self, **kwargs) -> QueueItem:
        """
        Get and remove the :class:`QueueItem` with the highest priority/lowest cost
        """
        return super().get(block=False)
