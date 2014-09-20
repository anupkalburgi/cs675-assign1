import Pyro4
#from can_node import CAN_Node

uri = "PYRO:can_node.1@129.174.55.248:5150"
node = Pyro4.Proxy(uri)
node2= node.join(1)
print node2
