from importlib import import_module

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