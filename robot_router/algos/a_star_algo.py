from collections import defaultdict
from typing import Optional, Dict, List

from robot_router.graph import InfiniteCellGraph
from robot_router.rotatinglaser import RotatingLaser
from robot_router.types import CellLocation
from robot_router.queue import PriorityQueue


def astar_heuristic(location: CellLocation, destination: CellLocation):
    return abs(location.x - destination.x) + abs(location.y - destination.y)


def astar(graph: InfiniteCellGraph,
           queue: PriorityQueue,
           origin: CellLocation,
           dest: CellLocation,
           lasers: List[RotatingLaser]):
    # Initialize the most important data structures
    queue.put((0.0, origin))
    costs_visited: Dict[CellLocation, float] = defaultdict(lambda: float('inf'))  # initialize with infinity
    costs_visited[origin] = 0.0
    path: Dict[CellLocation, Optional[CellLocation]] = dict()
    path[origin] = None

    while not queue.empty():
        # Get the next cell to settle
        current_cost, current_cell = queue.get()

        if current_cell == dest:
            break

        # maybe add adjacent cells to the priority queue
        for next_cell in graph.adjacent(current_cell):
            next_cost = current_cost + graph.cost()
            # is there a wormhole active?
            wormhole_dest = graph.wormhole(next_cell)
            if wormhole_dest and current_cost % 3 == 0:
                next_cell = wormhole_dest
                next_cost = 0
            # is there a laser?
            laser_hit = False
            for laser in lasers:
                laser.rotate(int(next_cost))
                if laser.hits_cell(next_cell):
                    laser_hit = True
                    break
            if laser_hit:
                continue
            # add the neighbor to the open set if
            # - we've not seen it before OR
            # - it has lower cost than before
            if next_cost < costs_visited[next_cell]:
                priority = next_cost + astar_heuristic(next_cell, dest)
                queue.put((priority, next_cell))
                costs_visited[next_cell] = next_cost
                path[next_cell] = current_cell

    return path
