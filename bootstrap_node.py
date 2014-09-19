import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone
import socket


Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')


def get_host():
    #return socket.gethostbyname(socket.gethostname())
    return socket.gethostname()

def main():
    zone = CAN_Zone((0, 0), (10, 10))
    node = CAN_Node(1,zone)
    daemon = Pyro4.Daemon(host=get_host(), port=5150);
    Pyro4.Daemon.serveSimple(
            {
                node: "bootstrap."+str(node.id)
            },
            daemon= daemon,
            ns = False )

if __name__=="__main__":
    main()
