from collections import namedtuple
from typing import Dict

CellLocation = namedtuple('Location', ('x', 'y'))
Wormholes = Dict[CellLocation, CellLocation]
