from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys


workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}
      
def getbylocation(location):
    # TODO
    return {
            'error': False,
            'result': []
     }


def getbyname(name):
    # TODO
    return {
        'error': False,
        'result': []
    }

def getbyyear(location, year):
    # TODO
    return {
            'error': False,
            'result': []
     }    

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # TODO: register RPC functions
    server.serve_forever()


if __name__ == '__main__':
    main()