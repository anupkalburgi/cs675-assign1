import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone


Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

obj = Pyro4.Proxy('PYRONAME:bootstrap.node')
try:
        node2 = obj.join(3)
except Exception:
        print "Pyro traceback:"
        print "".join(Pyro4.util.getPyroTraceback())
try:
        print node2.join(2)
except Exception:
        print "Pyro traceback:"
        print "".join(Pyro4.util.getPyroTraceback())