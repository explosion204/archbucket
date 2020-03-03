class Request:
    def __init__(self, id: int, request_type: str, command: str, args: list):
        self.id = id
        self.request_type = request_type
        self.command = command
        self.args = args
        self.response = str()

def process_text(request: Request):
    # test 
    if request.command == 'echo' and len(request.args) != 0:
        request.response = request.args[0]
    else: 
        request.response = 'error!'

def call(request: Request):
    if request.request_type == 'text':
        process_text(request)