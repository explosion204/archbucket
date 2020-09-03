class DefaultRequestRouter(object):
    def __init__(self, modules_list):
        self.modules = modules_list

    def route(self, request: Request):
        command = request.command
        self.modules['command']().run(request)