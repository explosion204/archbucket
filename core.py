from importlib import import_module
from queue import Queue

_modules = dict()
_users = dict()

def init_core():
    '''Load names of modules'''
    with open('modules/.modules') as file:
        for line in file.readlines():
            items = line.split()
            module = import_module(f"modules.{items[0]}")
            module_type = items[1]
            _modules[items[0]] = (module, module_type)

class Pipeline:
    def __init__(self, bot_interface):
        self.request_queue = Queue()
        self.count = 0
        self.busy = False
        self.bot_interface = bot_interface

    def start(self):
        while True:
            if self.request_queue.qsize() != 0:
                self.count -= 1
                self.busy = True
                request = self.request_queue.get()
                call(request)
                self.bot_interface.send_response(request)
                self.busy = False

    def push_request(self, request):
        self.request_queue.put(request)
        self.count += 1

class Request:
    def __init__(self, id: int, request_type: str, command: str, args: list):
        self.id = id
        self.request_type = request_type
        self.command = command
        self.args = args
        self.response = str()

def call(request: Request):
    command = request.command
    # check if user has an active session
    if request.id in _users:
        # get name of active module
        module_name = _users[request.id]
        # module of active session treats command as request argument too
        request.args.insert(0, request.command)
        # enter module
        _modules[module_name][0].run(request)
        return
    # if user has no active session then check type of module type
    if _modules[command][1] == 'single':
        _modules[request.command][0].run(request)
        return
    if _modules[command][1] == 'multi':
        # create active session for certain user
        _users[request.id] = request.command
        _modules[request.command][0].run(request)
        return
