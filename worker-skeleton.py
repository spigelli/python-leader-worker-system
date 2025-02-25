import json
from xmlrpc.server import SimpleXMLRPCServer
import sys

file_by_group = {
    'am': 'data-am.json',
    'nz': 'data-nz.json'
}

global data_table

def load_data(group):
    # Load the file
    file = file_by_group[group]
    with open(file, 'r') as f:
        data_table = json.load(f)
    return data_table

def try_or_error(func):
    try:
        return func()
    except Exception as e:
        print("[WORKER] Error: ", e)
        return {
            'error': str(e),
            'result': []
        }

def getbyname(data_table, name):
    def do_get_by_name():
        print("[WORKER] Getting by name: ", name, data_table.get(name, []), data_table)
        if data_table.get(name, False):
            return {
                'error': False,
                'result': [data_table[name]]
            }
        return {
            'error': False,
            'result': []
        }
    response = try_or_error(do_get_by_name)
    print("[WORKER] Responding with: ", response)
    return response

def getbylocation(data_table, location):
    def do_get_by_location():
        results = [record for record in data_table.values() if record['location'] == location]
        return {
            'error': False,
            'result': results
        }
    response = try_or_error(do_get_by_location)
    print("[WORKER] Responding with: ", response)
    return response

def getbyyear(data_table, location, year):
    def do_get_by_year():
        results = [record for record in data_table.values() if record['location'] == location and record['year'] == year]
        return {
            'error': False,
            'result': results
        }
    response = try_or_error(do_get_by_year)
    print("[WORKER] Responding with: ", response)
    return response

def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")
    global data_table
    data_table = load_data(group)



    # Register RPC functions
    server.register_function(lambda name: getbyname(data_table, name), 'getbyname')
    server.register_function(lambda location: getbylocation(data_table, location), 'getbylocation')
    server.register_function(lambda location, year: getbyyear(data_table, location, year), 'getbyyear')
    server.serve_forever()

if __name__ == '__main__':
    main()