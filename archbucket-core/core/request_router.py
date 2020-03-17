from importlib import import_module
from os.path import exists
from inspect import signature
import re
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
        with open('core/modules/.modules', 'r') as file:
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

    def validate(self, module_name) -> (bool, str):
        path = f'core/modules/{module_name}'
        # 1st: check for existence
        if not exists(path + '.py'):
            return (False, f"Module '{module_name}' cannot be find in 'core/modules.")
        with open(path, 'r') as file:
            source_code = file.read()
        # 2nd: check for syntax errors
        try:
            compile(source_code)
        except SyntaxError:
            return (False, 'Syntax error.')
        module = import_module(path)
        # 3rd: check if module has required callable attribute 'run'
        if not hasattr(module, 'run') and not callable(module.run):
            return (False, f"Module '{module_name}' has no callable attribute with name 'run'.")
        # 4th: check signature of 'run'
        if not str(signature(module.run)) == '(request: core.request_router.Request) -> bool':
            return (False, "Signature of 'run' function does not match to following: (request: core.request_router.Request) -> bool.")
        # 5th: check return value of 'run'
        pattern = r'def run(\.|\n)*return (False|Return))'
        if not re.search(pattern, source_code):
            return (False, "'run' function does not return True nor False.")
        # successful validation
        with open('core/modules/.modules', 'r+') as file:
            modules_list = json.load(file)
            modules_list.append(module_name)
            json.dump(modules_list, file)
        return (True, f"Module '{module_name}' has been successfully validated. Restart bot to begin using it.")