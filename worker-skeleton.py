from xmlrpc.server import SimpleXMLRPCServer
import sys

# Storage of data
data_table = {}


def load_data(group):
    # TODO load data based which portion it handles (am or nz)
    pass


def getbyname(name):
    # TODO
    return {
        'error': False,
        'result': []
    }

def getbylocation(location):
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
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # TODO register RPC functions
    server.serve_forever()

if __name__ == '__main__':
    main()