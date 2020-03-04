from importlib import import_module
from queue import Queue

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

def process_text(request: Request):
    imported_module = import_module(f"modules.{request.command}")
    request.response = imported_module.run(request.args)

def call(request: Request):
    if request.request_type == 'text':
        process_text(request)