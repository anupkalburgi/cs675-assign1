from __future__ import print_function
import Pyro4
import person



Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.REQUIRE_EXPOSE = True
Pyro4.config.DETAILED_TRACEBACK = True


class Warehouse(object):
    def __init__(self):
        self.contents = ["chair", "bike", "flashlight", "laptop", "couch"]

    def list_contents(self):
        return self.contents

    def take(self, name, item):
        self.contents.remove(item)
        print("{0} took the {1}.".format(name, item))

    def store(self, name, item):
        self.contents.append(item)
        print("{0} stored the {1}.".format(name, item))


def main():
    warehouse = Warehouse()
    #Pyro4.config.HOST = "129.174.126.30:5555"
    daemon = Pyro4.Daemon()
    Pyro4.Daemon.serveSimple(
            {
                warehouse: "example.warehouse"
            },
	    daemon=daemon,
            ns = False)

if __name__=="__main__":
    main()


