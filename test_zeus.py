import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone


Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.REQUIRE_EXPOSE = True
Pyro4.config.DETAILED_TRACEBACK = True

node1 = Pyro4.Proxy('PYRONAME:node.1')
node2 = node1.join(2)
try:
        node = node2.view()
except Exception:
        print "".join(Pyro4.util.getPyroTraceback())
try:
        print node2.join(2)
except Exception:
        print "Pyro traceback:"
        print "".join(Pyro4.util.getPyroTraceback())