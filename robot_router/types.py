from collections import namedtuple
from typing import Dict

CellLocation = namedtuple('CellLocation', ('x', 'y'))
Wormholes = Dict[CellLocation, CellLocation]
