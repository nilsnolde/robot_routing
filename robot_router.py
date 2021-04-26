#!/usr/bin/env python3.9

import sys
from pathlib import Path
import re
from typing import List, Dict

from robot_router.queue import PriorityQueue
from robot_router.graph import InfiniteCellGraph
from robot_router.types import CellLocation
from robot_router.algos import astar
from robot_router.rotatinglaser import RotatingLaser
from robot_router.logger import LOGGER


def reconstruct_path(came_from: Dict[CellLocation, CellLocation],
                     origin: CellLocation, dest: CellLocation) -> List[List[int]]:
    """Reconstruct the path taken by the routing algorithm."""
    current: CellLocation = dest
    path: List[List[int]] = []
    while current != origin:
        path.append(list(current))
        current = came_from[current]
    path.append(list(origin))
    path.reverse()

    return path


help = """
robot_router.py
Routing robots with all the fancy stuff: obstacles and (rotating) laser beams.

Usage: ./robot_router.py INPUT OUTPUT
"""

if __name__ == '__main__':
    # Parse args and throw in case of unexpected arguments
    args = sys.argv
    if len(args) != 3:
        LOGGER.error(f"Not the right number of arguments!\n{help}")
        sys.exit(1)
    in_file = Path(args[1])
    if not in_file.exists():
        LOGGER.error(f"Input file doesn't exist!\n{help}")
        sys.exit(1)

    # Read the input and extract the interesting bits
    with (open(in_file)) as f:
        # make sure nothing evil gets executed
        lines = f.readlines()
        if not len(lines) == 5:
            LOGGER.error("Input file must have exactly 5 entries/lines.")
            sys.exit(1)
        # no line should contain characters other than the ones below
        if all([re.search('[^\d\s\'\"NESW{1,4}\(\)\[\]]', line) for line in lines]):
            LOGGER.error("Input file seems corrupt.")
            sys.exit(1)
        # Eval the objects (hopefully safely) into lists/tuples
        origin, destination, barriers, lasers, wormholes = [eval(line) for line in lines]

    if not origin or not destination:
        LOGGER.error("Origin or destination not supplied.")
        sys.exit(1)

    # calculate the route
    barriers = [CellLocation(*loc) for loc in barriers]
    route = astar(
        InfiniteCellGraph(
            barriers,
            {CellLocation(*start): CellLocation(*finish) for start, finish in wormholes},
            []
        ),
        PriorityQueue(),
        CellLocation(*origin),
        CellLocation(*destination),
        [RotatingLaser(*laser, barriers) for laser in lasers]
    )

    # Write the output
    out_file = Path(args[2])
    if out_file.exists():
        LOGGER.warning(f"{out_file.name} exists, replacing...")

    with open(out_file, 'w') as f:
        f.write(str(reconstruct_path(route, origin, destination)))
