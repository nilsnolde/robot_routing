import unittest
from collections import deque

from robot_router.rotatinglaser import RotatingLaser
from robot_router.types import CellLocation


class RotatingLaserTest(unittest.TestCase):

    def test_initialization(self):
        direction = 'S'
        obstacles = [CellLocation(x, y) for x, y in [(6, 2), (6, 4), (6, 10)]]
        laser = RotatingLaser(6, 6, direction, obstacles)

        self.assertEqual(laser.directions, deque(['S', 'W', 'N', 'E']))
        self.assertEqual(list(laser.obstacle_filters[direction]), [(6, 2), (6, 4)])

    def test_rotate_hit_cell(self):
        pos = (6, 6)                                    ### N ###        ### E ###        ### S ###      ### W ###
        obstacles = [CellLocation(x, y) for x, y in [(6, 10), (6, 2), (10, 6), (2, 6), (6, 1), (6, 9), (1, 6), (9, 6)]]
        obstacles_visible = {
            'N': {'seen': [CellLocation(6, 10), CellLocation(6, 9)], "hits": CellLocation(6, 6), "misses": CellLocation(6, 11)},
            'E': {'seen': [CellLocation(10, 6), CellLocation(9, 6)], "hits": CellLocation(8, 6), "misses": CellLocation(11, 6)},
            'S': {'seen': [CellLocation(6, 1), CellLocation(6, 2)], "hits": CellLocation(6, 4), "misses": CellLocation(6, 0)},
            'W': {'seen': [CellLocation(1, 6), CellLocation(2, 6)], "hits": CellLocation(4, 6), "misses": CellLocation(0, 6)}
        }

        laser = RotatingLaser(*pos, 'N', obstacles)

        for direction in ['E', 'S', 'W']:
            laser.rotate()
            self.assertEqual(laser.current_direction, direction)
            self.assertListEqual(sorted(laser.obstacle_filters[direction]), sorted(obstacles_visible[direction]['seen']))

            self.assertTrue(laser.hits_cell(obstacles_visible[direction]['hits']))
            self.assertFalse(laser.hits_cell(obstacles_visible[direction]['misses']))
