import unittest
from collections import deque

from robot_router.queue import PriorityQueue
from robot_router.types import CellLocation


class PriorityQueueTest(unittest.TestCase):

    def test_put_get(self):
        q = PriorityQueue()

        for count, (prio, cell) in enumerate(((4, CellLocation(4, 4)), (2, CellLocation(2, 2)), (5, CellLocation(5, 5)))):
            count += 1

            q.put((prio, cell))
            self.assertEqual(count, q.qsize())

        self.assertEqual(q.get()[1], CellLocation(2, 2))
        self.assertEqual(q.get()[1], CellLocation(4, 4))
        self.assertEqual(q.get()[1], CellLocation(5, 5))
        self.assertTrue(q.empty())
