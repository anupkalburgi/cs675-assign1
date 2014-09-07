__author__ = 'anupkalburgi'

import unittest
from can_zone import CAN_Zone
from can_zone import Point

class Test_Can_Zone(unittest.TestCase):

    def test_virtical_split(self):
        zone = CAN_Zone((0,0),(10,10))

        self.assertEqual(zone.height,10)
        self.assertEqual(zone.width,10)

        can1, can2 = zone.split()
        self.assertEqual(can1.min.x,0)
        self.assertEqual(can1.min.y,0)
        self.assertEqual(can1.max.x,5)
        self.assertEqual(can1.max.y,10)

        self.assertEqual(can2.min.x,5)
        self.assertEqual(can2.min.y,0)
        self.assertEqual(can2.max.x,10)
        self.assertEqual(can2.max.y,10)

        can3, can4 = can1.split()
        self.assertEqual(can3.height,5)
        self.assertEqual(can3.width,5)

        self.assertEqual(can3.min.x,0)
        self.assertEqual(can3.min.y,0)
        self.assertEqual(can3.max.x,5)
        self.assertEqual(can3.max.y,5)

        self.assertEqual(can4.min.x,0)
        self.assertEqual(can4.min.y,5)
        self.assertEqual(can4.max.x,5)
        self.assertEqual(can4.max.y,10)

        can5, can6 = can2.split()
        self.assertEqual(can6.min.x,5)
        self.assertEqual(can6.min.y,5)
        self.assertEqual(can6.max.y,10)
        self.assertEqual(can6.max.x,10)


        can5, can6 = can2.split()
        self.assertEqual(can5.min.x,5)
        self.assertEqual(can5.min.y,0)
        self.assertEqual(can5.max.x,10)
        self.assertEqual(can5.max.y,5)

    def test_within(self):
        zone = CAN_Zone((0, 0), (10, 10))
        can1, can2 = zone.split()
        can1, can3 = can1.split()
        can1, can4 = can1.split()
        # print can1.sides()
        # print can2.sides()
        # print can3.sides()
        # print can4.sides()
        self.assertFalse(can1.within(can2))
        self.assertTrue(can3.within(can2))
        self.assertTrue(can4.within(can2))

    def test_distance(self):
        point1 = Point((2, 2))
        point2 = Point((2, 2))
        zone = CAN_Zone((0, 0), (2, 2))
        print zone.sides()
        print zone.distance(point1)








if __name__ == '__main__':
    unittest.main()
