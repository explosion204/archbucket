from importlib import import_module
from os.path import exists
from inspect import signature
import re
import json
import ast

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
            self.modules = {name: import_module(f"core.modules.{name}") for name in names.keys() if names[name] == 'enabled'}

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

    def validate(self, module_name, source_code) -> (bool, str):
        try:
             ast.parse(source_code)
        except SyntaxError:
            return (False, 'Syntax error.')
        pattern = r'def run\((.|\n)*\)(.|\n)*return (False|True)'
        if not re.search(pattern, source_code):
             return (False, "Module has no callable attribute 'run' which returns True or False.")
        # successful validation
        # with open('core/modules/.modules', 'r+') as file:
        #     modules_list = json.load(file)
        #     modules_list.append(module_name)
        #     json.dump(modules_list, file)
        return (True, f"Module '{module_name}' has been successfully imported.")