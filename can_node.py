from can_zone import CAN_Zone
import random
from can_zone import Point
from itertools import ifilterfalse
import socket
import Pyro4


class CAN_Node(object):

    def __init__(self, id=None, zone=None):
        self.id = id or id(self)
        self.zone = zone
        self.hash_table = {}
        self.neighbours = []

    @staticmethod
    def can_node_point():
        return Point((random.randint(0, 10), random.randint(0, 10)))

    def __repr__(self):
        return '{%s} id->%s' % (self.zone, self.id)

    def is_neighbours(self, other_node):
        # Ask zones for its sides, intersect the sides of both of them using set if there is something in
        # common we have a winner
        return bool(set(self.zone.sides()).intersection(other_node.zone.sides()))

    def update_neighbours(self, new_node):
        #get all my past neighbours and remove myself from the list
        past_neighbours = [ngh for ngh in self.neighbours if not self.is_neighbours(ngh)]

        for ngh in past_neighbours:
            if self in ngh.neighbours:
                ngh.neighbours.remove(self)

        #Checks if i am still neighbour to the old guys
        self.neighbours = [ngh for ngh in self.neighbours if self.is_neighbours(ngh)]

        tmp = []
        for ngh in self.neighbours:
            if ngh.is_neighbours(new_node) and new_node not in ngh.neighbours:
                ngh.neighbours.append(new_node)

    def _next_best_node(self, point):
        #get the distance from all the nodes and select a node with minimum distance
        #Might be i should just sort ? or using a min function and mention ke !!!!!
        return min(self.neighbours, key=lambda node: node.zone.distance(point))

    def join(self, id, point=None):
        #Generate random x,y for the given node,Use self.zone to divide and assign it to the new node
        if not point:
            point = self.can_node_point()
        print "point:", point, "zone:", self.zone
        if point in self.zone:
            self.zone, new_zone = self.zone.split()
            new_node = CAN_Node(id, new_zone)
            new_node.neighbours = self.neighbours + [self]
            self.update_neighbours(new_node)
            self.neighbours.append(new_node)
            print "Finished Join"

        else:
            print point, "Not Found in Zone", self.zone
            next_node = self._next_best_node(point)
            new_node = next_node.join(id, point)

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

'''
def main():
    node = CAN_Node(1)
    daemon = Pyro4.Daemon(host=get_host(), port=5150);
    Pyro4.Daemon.serveSimple(
            {
                node: "can_node."+str(node.id)
            },
            daemon= daemon,
            ns = False )

if __name__=="__main__":
    main()
'''
