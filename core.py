from importlib import import_module
from queue import Queue

_modules = dict()
_sessions = dict()

def init_core():
    '''Load names of modules'''
    with open('modules/.modules') as file:
        for module_name in file.read().splitlines():
            module = import_module(f"modules.{module_name}")
            _modules[module_name] = module 

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
    if request.id in _sessions:
        # get name of active module
        module_name = _sessions[request.id]
        # module of active session treats command as request argument too
        request.args.insert(0, request.command)
        # enter module and get flag if session must be closed
        session_exit = _modules[module_name].run(request)
        if session_exit:
            del _sessions[request.id]
        return
    try:
        session_exit = _modules[command].run(request)
    except KeyError:
        return
    # add session to track dictionary if script needs it
    if not session_exit:
        _sessions[request.id] = request.command