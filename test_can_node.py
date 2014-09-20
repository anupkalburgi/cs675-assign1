import unittest
from can_node import CAN_Node
from can_zone import CAN_Zone


class TestCanNode(unittest.TestCase):

    # def test_join(self):
    #     zone = CAN_Zone((0, 0), (10, 10))
    #     node = CAN_Node(zone)
    #     self.assertTrue(node.join())

    def test_is_neighbours(self):
        zone = CAN_Zone((0, 0), (10, 10))
        node1 = CAN_Node(1, zone)
        node2 = node1.join(2)
        node3 = node2.join(3)
        node4 = node3.join(4)
        print "#########"
        print node1
        print node2
        print node3
        print node4,node4.url
        print "-----------"
        print len(node1.neighbours)
        print len(node2.neighbours)
        print len(node3.neighbours)

        # print(node1)
        # print(node)
        # node4, node5 = node4.join()
        # print node4
