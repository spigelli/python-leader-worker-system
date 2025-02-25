from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys


workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}

def parseResponse(responses):
    # Filter out the error responses
    successful_responses = [r for r in responses if not r['error']]
    print("[LEADER] Successful Responses: ", successful_responses)
    if len(successful_responses) == 0:
        return {
            'error': "No successful responses",
            'result': []
        }
    else:
        return {
            'error': False,
            'result': [response['result'] for response in successful_responses]
        }

def try_or_error(func):
    def do_try_or_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("[LEADER] Error: ", e)
            return {
                'error': str(e),
                'result': []
            }
    return do_try_or_error

# Gets the location from the worker processes
def getbylocation(location):
    # Call both workers simultaneously and return the
    # record that is not error
    def getbylocation_worker(worker):
        return worker.getbylocation(location)
    
    print("[LEADER] Requesting workers for locations...")
    # Collect results mapping over the workers
    results = list(map(try_or_error(getbylocation_worker), workers.values()))
    print("[LEADER] Got Results: ", results)
    return parseResponse(results)

def getbyname(name):
    def get_by_name_worker(worker):
        return worker.getbyname(name)


    print("[LEADER] Requesting workers for names...")
    results = list(map(try_or_error(get_by_name_worker), workers.values()))
    print("[LEADER] Got Results: ", results)
    return parseResponse(results)

def getbyyear(location, year):
    def get_by_year_worker(worker):
        return worker.getbyyear(location, year)

    print("[LEADER] Requesting workers for years...")
    results = list(map(try_or_error(get_by_year_worker), workers.values()))
    print("[LEADER] Got Results: ", results)
    return parseResponse(results)

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # Register RPC functions
    server.register_function(getbylocation, 'getbylocation')
    server.register_function(getbyname, 'getbyname')
    server.register_function(getbyyear, 'getbyyear')
    server.serve_forever()


if __name__ == '__main__':
    main()