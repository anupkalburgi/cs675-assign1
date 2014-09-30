import cmd
import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone
from prettytable import *



Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.REQUIRE_EXPOSE = True
Pyro4.config.DETAILED_TRACEBACK = True



class CANSHELL(cmd.Cmd):
    prompt = 'canshell:-> '
    intro = "Welcome! You can interact witht he CAN network using this shell."

    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'

    ruler = '-'

    def preloop(self):
        #Locate NameServer and register your self
        self.nameserver = Pyro4.locateNS(host='medusa-node1.vsnet.gmu.edu')
        print "Name Lookup services connected at {0}".format(self.nameserver._pyroUri.location)


    def _print_nodes(self,node):
        print "The New Zone is",new_node.zone
        y = PrettyTable(["Neighbour-ID", "Zone"],title = "New Node Details",)
        y.align["Neighbour-ID"] = "l" # Left align
        for neighbour in node.neighbours:
            y.add_row([neighbour.id,neighbour.zone])
        print y

    def do_join(self,s):
        node1 = Pyro4.Proxy('PYRONAME:node.1')
        new_node = node1.join(int(s))
        self._print_nodes(new_node)

    def do_leave(self,s):
        node1 = Pyro4.Proxy('PYRONAME:node.1')
        new_node = node1.leave(int(s))
        self._print_nodes(new_node)

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    CANSHELL().cmdloop()