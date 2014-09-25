import cmd
import Pyro4
from can_node import CAN_Node
from can_zone import CAN_Zone


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

    def do_prompt(self, line):
        "Change the interactive prompt"
        print self.nameserver
        self.prompt = line + ': '

    def do_join(self):
        node1 = Pyro4.Proxy('PYRONAME:bootstrap.node')
        #Get the key,
        id = 'Raw input'
        new_node = node1.join(id)
        pass

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    CANSHELL().cmdloop()