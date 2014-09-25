import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone
import socket


'''
Config:
BOOTSTRAP_SERVER = "medusa-node1.vsnet.gmu.edu"
'''

#PYRO_LOGFILE = '/home/akalburg/github/logs/errors.log' #TODO: Goto make sure tp move it to FAB

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.REQUIRE_EXPOSE = True
Pyro4.config.DETAILED_TRACEBACK = True

def get_host():
    return socket.gethostbyname(socket.gethostname())
    #return socket.gethostname()

def main():
    zone = CAN_Zone((0, 0), (10, 10))
    node = CAN_Node(1,zone)
    daemon = Pyro4.Daemon(host=get_host(), port=5150);
    node_uri = daemon.register(node)
    ns = Pyro4.locateNS(host='medusa-node1.vsnet.gmu.edu', port=9090)
    ns.register("node."+str(1), node_uri)
    print "node."+str(node.id)
    print("Can Node running.")
    daemon.requestLoop()

if __name__=="__main__":
    main()
