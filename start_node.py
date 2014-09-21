import Pyro4
import socket
from can_node import CAN_Node

def get_host():
    return socket.gethostbyname(socket.gethostname())

def main():
    node = CAN_Node(1)
    daemon = Pyro4.Daemon(host=get_host(), port=5150)
    node_uri = daemon.register(node)
    ns = Pyro4.locateNS(host='medusa-node1.vsnet.gmu.edu', port=9090)
    ns.register("node."+str(node.id), node_uri)
    print "node."+str(node.id)
    print("Can Node running.")
    daemon.requestLoop()

if __name__=="__main__":
    main()
