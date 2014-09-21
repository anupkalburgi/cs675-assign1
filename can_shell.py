import cmd
import Pyro4

class CANSHELL(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'canshell>: '
    intro = "Welcome! You can interact witht he CAN network using this shell."

    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'

    ruler = '-'

    def preloop(self):
        #Locate NameServer and register your self
        ns = Pyro4.locateNS(host='medusa-node1.vsnet.gmu.edu')
        print "Your are now connected to {0}".format(ns._pyroUri.location)
        print "I will have to connect to boot strap server here"

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + ': '

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    CANSHELL().cmdloop()