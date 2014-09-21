import cmd
import Pyro4

class CANSHELL(cmd.Cmd):
    def __init__(self):
        self.nameserver = None

    prompt = 'canshell>: '
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

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    CANSHELL().cmdloop()