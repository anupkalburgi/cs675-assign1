from can_zone import CAN_Zone
import random
from can_zone import Point
from itertools import ifilterfalse
import socket
import Pyro4

import logging
logger = logging.getLogger('can_node')
hdlr = logging.FileHandler('logs/can_node.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


@Pyro4.expose
class CAN_Node(object):

    def __init__(self, id, zone=None):
        logger.info("New Node {0} was created by Can_Node constructor".format(id))
        self._id = id
        self._zone = zone
        self._hash_table = {}
        self._neighbours = []

    def pyro_node_constructor(self,id,zone,neighbours,hash_table=None):
        if self.id == id:
            self.zone = zone
            self.neighbours = neighbours
            self.hash_table = hash_table
        return self
        # Else Will have to raise a exception, because the request was not right
        # Nor raising a Exception can make debugging harder !!!! Ah ok


    @property
    def id(self):
        return self._id

    @property
    def zone(self):
        return self._zone

    @property
    def neighbours(self):
        return self._neighbours

    @staticmethod
    def can_node_point():
        return Point((random.randint(0, 10), random.randint(0, 10)))

    def __repr__(self):
        return '{%s} id->%s' % (self._zone, self._id)

    def is_neighbours(self, other_node):
        # Ask zones for its sides, intersect the sides of both of them using set if there is something in
        # common we have a winner
        return bool(set(self._zone.sides()).intersection(other_node.zone.sides()))

    def update_neighbours(self, new_node):
        #get all my past neighbours and remove myself from the list
        past_neighbours = [ngh for ngh in self._neighbours if not self.is_neighbours(ngh)]

        for ngh in past_neighbours:
            if self in ngh.neighbours:
                ngh.neighbours.remove(self)

        #Checks if i am still neighbour to the old guys
        self._neighbours = [ngh for ngh in self._neighbours if self.is_neighbours(ngh)]

        tmp = []
        for ngh in self._neighbours:
            if ngh.is_neighbours(new_node) and new_node not in ngh.neighbours:
                ngh.neighbours.append(new_node)

    def _next_best_node(self, point):
        #get the distance from all the nodes and select a node with minimum distance
        #Might be i should just sort ? or using a min function and mention ke !!!!!
        return min(self._neighbours, key=lambda node: node.zone.distance(point))

    def join(self, id, point=None):
        #Generate random x,y for the given node,Use self.zone to divide and assign it to the new node
        if not point:
            point = self.can_node_point()
            logger.info("New Point Generated:{0}".format(point))
        print "point:", point, "zone:", self._zone
        if point in self._zone:
            self._zone, new_zone = self._zone.split()
            pyro_node = Pyro4.Proxy('PYRONAME:node.%s'%id)
            neighbours = self._neighbours + [self]
            new_node = pyro_node.pyro_node_constructor(id, new_zone,neighbours)
            self.update_neighbours(new_node)
            self.neighbours.append(new_node)
            print "Finished Join"

        else:
            logger.info("Point {0} was not found in zone {1}".format(point, self._zone))
            next_node = self._next_best_node(point)
            logger.info("Next Best point choosen was {0}".format(next_node.id))
            pyro_node = Pyro4.Proxy('PYRONAME:node.%s'%next_node.id)
            logger.info("PyroNode:{0} is being connected to".format(pyro_node))
            new_node = pyro_node.join(id, point)

        return new_node

    def view(self):
        pass

    def _merge(self):
        pass

    def leave(self):
        #Thing is i got to hold a list of node somewhere, ya or else how would even know what is the xy
        # For a node merge to be proper either it's width or height must be the same or both have to be same
        mergeing_node = min(self.neighbours, key = self.neighbours.zone.area)
        mergeing_node.zone = self.zone.merge(mergeing_node.zone)
        mergeing_node.neighbours = self.neighbours + (mergeing_node.neighbours - self.neighbours)
        return mergeing_node

    def insert_file(self):
        pass

    def search(self):
        pass

