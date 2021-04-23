from collections import defaultdict
from typing import Optional, Dict

from robot_router.graph import InfiniteCellGraph
from robot_router.types import CellLocation
from robot_router.logger import LOGGER
from robot_router.queue import PriorityQueue


def astar_heuristic(location: CellLocation, destination: CellLocation):
    return abs(location.x - destination.x) + abs(location.y - destination.y)


def astar(graph: InfiniteCellGraph,
           queue: PriorityQueue,
           origin: CellLocation,
           dest: CellLocation):
    # Initialize the most important data structures
    queue.put((0.0, origin))
    costs_visited: Dict[CellLocation, float] = defaultdict(lambda: float('inf'))  # initialize with infinity
    costs_visited[origin] = 0.0
    path: Dict[CellLocation, Optional[CellLocation]] = dict()
    path[origin] = None

    current_time = 0

    while not queue.empty():
        # Get the next cell to settle
        current_cell = queue.get()

        # see if this is a wormhole
        wormhole_destination = graph.wormhole(current_cell) if current_time % 3 == 0 else None
        if current_cell == dest:
            break
        elif wormhole_destination:
            LOGGER.info(f"Entered wormhole at {current_cell}, teleporting to {wormhole_destination}")
            current_cell = wormhole_destination

        current_time += 1

        # maybe add adjacent cells to the priority queue
        for next_cell in graph.adjacent(current_cell):
            next_cost = costs_visited[current_cell] + graph.cost()
            # add the neighbor to the open set if
            # - we've not seen it before OR
            # - it has lower cost than before
            if next_cost < costs_visited[next_cell] or not costs_visited[next_cell]:
                priority = next_cost + astar_heuristic(next_cell, dest)
                queue.put((priority, next_cell))
                costs_visited[next_cell] = next_cost
                path[next_cell] = current_cell

    return path
