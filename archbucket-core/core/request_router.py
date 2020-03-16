from importlib import import_module
import json

class Request:
    def __init__(self, id: int, request_type: str, command: str, args: list):
        self.id = id
        self.request_type = request_type
        self.command = command
        self.args = args
        self.response = str()

class RequestRouter:
    def __init__(self):
        self.modules = dict()
        self.sessions = dict()
        # Load names of modules
        with open('core/modules/.modules') as file:
            names = json.load(file)
            self.modules = {name: import_module(f"core.modules.{name}") for name in names}

    def route(self, request: Request):
        command = request.command
        # check if user has an active session
        if request.id in self.sessions:
            # get name of active module
            module_name = self.sessions[request.id]
            # module of active session treats command as request argument too
            request.args.insert(0, request.command)
            # enter module and get flag if session must be closed
            session_exit = self.modules[module_name].run(request)
            if session_exit:
                del self.sessions[request.id]
            return
        try:
            session_exit = self.modules[command].run(request)
        except KeyError:
            return
        # add session to track dictionary if script needs it
        if not session_exit:
            self.sessions[request.id] = request.command