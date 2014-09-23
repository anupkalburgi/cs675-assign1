import Pyro4
import socket
from can_node import CAN_Node

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.PYRO_LOGFILE = '/home/akalburg/github/logs/errors.log'
Pyro4.config.DETAILED_TRACEBACK = True
'''
Config:
BOOTSTRAP_SERVER = "medusa-node1.vsnet.gmu.edu"
'''


def get_node_id():
    node = socket.gethostname()
    return node.split('.')[0].split('-')[2]



def get_host():
    return socket.gethostbyname(socket.gethostname())

def main():
    id = get_node_id()
    node = CAN_Node(int(id))
    daemon = Pyro4.Daemon(host=get_host(), port=5150)
    node_uri = daemon.register(node)
    ns = Pyro4.locateNS(host='medusa-node1.vsnet.gmu.edu', port=9090)
    ns.register("node."+str(id), node_uri)
    print "node."+ id
    print("Can Node running.")
    daemon.requestLoop()

if __name__=="__main__":
    main()
