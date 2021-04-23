from typing import List
from collections import deque

from .types import CellLocation


class RotatingLaser:
    """
    Rotating laser with a position and initial shooting direction.

    Obstacles will be taken into account if passed.
    """
    def __init__(self, x: int, y: int, direction: str, obstacles: List[CellLocation]):
        self._position = CellLocation(x, y)
        self.directions = deque(['N', 'E', 'S', 'W'])
        self.current_direction = direction

        # left-rotate deque to start at initial direction
        self.rotate(-1 * self.directions.index(direction))
        # rotate() sets current_direction, make sure it didn't mess up
        assert self.current_direction == direction

        self.cell_filters = {
            'N': lambda cell: self._position.x == cell.x and self._position.y < cell.y,
            'E': lambda cell: self._position.y == cell.y and self._position.x < cell.x,
            'S': lambda cell: self._position.x == cell.x and self._position.y > cell.y,
            'W': lambda cell: self._position.y == cell.y and self._position.x > cell.x
        }
        # determine the obstacles per direction once
        self.obstacle_filters = {
            'N': filter(self.cell_filters['N'], obstacles),
            'E': filter(self.cell_filters['E'], obstacles),
            'S': filter(self.cell_filters['S'], obstacles),
            'W': filter(self.cell_filters['W'], obstacles)
        }

    def hits_cell(self, cell: CellLocation) -> bool:
        """Determines whether the laser shoots the given cell."""
        # Bail early if there's no way the laser can shoot the cell
        hit: bool = self.cell_filters[self.current_direction](cell)
        if not hit:
            return False

        potential_obstacles = list(self.obstacle_filters[self.current_direction])
        # if no obstacle in the way, the cell will be shot
        if not potential_obstacles:
            return True

        # return True if no obstacle is between the laser and the given cell
        if self.current_direction == 'N':
            closest_obstacle = min(potential_obstacles, key=lambda o: o.y)
            return closest_obstacle.y > cell.y
        elif self.current_direction == 'E':
            closest_obstacle = min(potential_obstacles, key=lambda o: o.x)
            return closest_obstacle.x > cell.x
        elif self.current_direction == 'S':
            closest_obstacle = max(potential_obstacles, key=lambda o: o.y)
            return closest_obstacle.y < cell.y
        elif self.current_direction == 'W':
            closest_obstacle = max(potential_obstacles, key=lambda o: o.x)
            return closest_obstacle.x < cell.x

    def rotate(self, places: int = -1):
        """Rotates the laser's direction by 90° clockwise."""
        self.directions.rotate(places)
        self.current_direction = self.directions[0]
