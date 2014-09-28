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
        logger.info("Zone Value in Constructor:{0} for ID: {1}".format(zone,id))
        if self._id == id:
            self._zone = zone
            self._neighbours = neighbours
            self._hash_table = hash_table or {}
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

    @property
    def hash_table(self):
        return self._hash_table

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

    def _split_hash_table(self,new_zone):
        old_zone = {}
        new_zone = {}
        for k,v in self._hash_table.iteritems():
            if self.get_coordinates_for_key_word(k) in self._zone:
                old_zone[k] = v
            else:
                new_zone[k] = v
        return old_zone, new_zone



    def join(self, id, point=None):
        #Generate random x,y for the given node,Use self.zone to divide and assign it to the new node
        if not point:
            point = self.can_node_point()
            logger.info("New Point Generated:{0}".format(point))
        print "point:", point, "zone:", self._zone
        if point in self._zone:
            self._zone, new_zone = self._zone.split()
            self._hash_table, new_hash_table = self._split_hash_table(new_zone)
            pyro_node = Pyro4.Proxy("PYRONAME:node.%s" %id)
            neighbours = self._neighbours + [self]
            logger.info("Got a remote node to update:{0}".format(pyro_node.id))
            new_node = pyro_node.pyro_node_constructor(id, new_zone,neighbours,new_hash_table)
            self.update_neighbours(new_node)
            self._neighbours.append(new_node)
            logger.info("Finished Join")

        else:
            logger.info("Point {0} was not found in zone {1}".format(point, self._zone))
            next_node = self._next_best_node(point)
            logger.info("Next Best point choosen was {0}".format(next_node.id))
            pyro_node = Pyro4.Proxy('PYRONAME:node.%s'%next_node.id)
            logger.info("PyroNode:{0} is being connected to".format(pyro_node))
            new_node = pyro_node.join(id, point)

        return new_node

    def view(self, visited=None,to_visit= None, run=0 ):
        logger.info("View for node {0}".format(self._id))
        if visited and to_visit and self._neighbours:
            logger.info("".format(self._id))
            to_visit = to_visit + list(set(self._neighbours)^set(visited))


        if run == 0:
            visited = [self]
            to_visit = self._neighbours
            run = 1

            to_visit = [node for node in to_visit if self._id != node.id ]
            if to_visit:
                next_visit = min(to_visit, key=lambda n_node:n_node.id)
                logger.info("View moving on to Min() Node {0}".format(next_visit.id))
                pyro_node = Pyro4.Proxy("PYRONAME:node.%s" % next_visit.id)
                logger.info("Connected to {0} with type {1}".format(pyro_node.id, pyro_node._pyroUri ))
                return pyro_node.view(visited, to_visit,run)
                logger.info("Got across the call may be ? to {0}".format(next_visit.id))

        return visited


    def remote_updater(self,zone,new_neighbours,hash_table):
        logger.info("Node Gettting updated via leave {0}".format(self._id))
        self._zone = zone
        self._neighbours = new_neighbours
        self._hash_table = hash_table
        return self

    def leave(self,id):
        #Thing is i got to hold a list of node somewhere, or else how would even know what is the xy
        # For a node merge to be proper either it's width or height must be the same or both have to be same
        if self._id == id:
            logger.info("Leave Method for {0}".format(id))
            valid_merge_nodes = filter(lambda node: node.zone.is_valid_merge(self._zone), self._neighbours )
            if valid_merge_nodes:
                merging_node = min(valid_merge_nodes, key = lambda node: node.zone.area)
            else:
                merging_node = min(self._neighbours, key = lambda node: node.zone.area)


            logger.info(" Selecting from here -->Node {0} selected for merger".format(merging_node.id))
            logger.info("Pyr-obj:{0}".format(merging_node.id))

            new_zone = self._zone.merge(merging_node.zone)
            new_hash_table = self._hash_table
            logger.info("Self Hash Table:{0}".format(self._hash_table))
            logger.info("Merging Hash Table:{0}".format(merging_node.hash_table ))
            new_hash_table.update(merging_node.hash_table)

            new_neighbours = list(set(self._neighbours + merging_node.neighbours))
            new_neighbours = [node for node in new_neighbours if node.id != self._id ]
            new_neighbours = [node for node in new_neighbours if node.id != merging_node.id ]

            #Still have to update neighbours
            logger.info("New zone is {0} along with new neighbours {1} and hashtable {2} ".format(new_zone,new_neighbours,new_hash_table))
            pyro_node = Pyro4.Proxy("PYRONAME:node.%s" %merging_node.id )
            merged_node = pyro_node.remote_updater(new_zone,new_neighbours,new_hash_table)
            logger.info("New With zone {0}".format(merged_node.zone))
            logger.info("Megre Finished")

        else:
            pyro_node = Pyro4.Proxy("PYRONAME:node.{0}".format(id))
            merged_node = pyro_node.leave(id)

        return merged_node

    def get_odd_positions(self,keyword):
        word = []
        for count,i in enumerate(list(keyword)):
            if count % 2 == 1:
                word.append(i)
        return word

    def get_even_positions(self,keyword):
        word = []
        for count,i in enumerate(list(keyword)):
            if count % 2 == 0:
                word.append(i)
        return word

    def get_coordinates_for_key_word(self,keyword):
        char_odd = self.get_odd_positions(keyword)
        char_even = self.get_even_positions(keyword )
        x = 0
        for i in char_odd:
            x = x + ord(i)
        x = x % 10

        y = 0
        for i in char_even:
            y = y + ord(i)
        y = y % 10

        return Point((x,y))


    def insert_file(self,keyword,filename,point=None):
        if not point:
            point = self.get_coordinates_for_key_word(keyword)
        if point in self._zone:
            self._hash_table[keyword] = filename
            id =  self._id
        else:
            logger.info("File Insertion point {0} ".format(point))
            next_node = self._next_best_node(point)
            pyro_node = Pyro4.Proxy('PYRONAME:node.%s'%next_node.id)
            logger.info("PyroNode:{0} is being connected, for keyword insertion".format(pyro_node))
            id = pyro_node.insert_file(keyword,filename,point)
        return id


    def search(self,keyword,point=None):
        if not point:
            point = self.get_coordinates_for_key_word(keyword)
        if point in self._zone:
            if self._hash_table.get(keyword):
                message =  self._id
            else:
                message = "Searched File not found, search landed on to node {0}".format(self._id)
        else:
            next_node = self._next_best_node(point)
            pyro_node = Pyro4.Proxy('PYRONAME:node.%s'%next_node.id)
            message = pyro_node.search(keyword,point)
        return message



