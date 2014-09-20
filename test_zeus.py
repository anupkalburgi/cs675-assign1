import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone


Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

#uri = "PYRO:can_node.1@129.174.126.30:5150"
uri = 'PYRO:bootstrap.1@Zeus.vse.gmu.edu:5150'
node = Pyro4.Proxy(uri)

node2 = node.join(3)
print node2
