class Request:
    def __init__(self, api_name: str, id: int, request_type: str, command: str, args: list):
        self.api_name = api_name
        self.id = id
        self.request_type = request_type
        self.command = command
        self.args = args
        self.response = str()