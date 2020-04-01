from importlib import import_module
from os.path import exists
from .request import Request
from . import error_handler
import re
import json
import ast
import os
import sys

class RequestRouter:
    def __init__(self):
        self.modules = dict()
        self.sessions = dict()
        # path to 'modules' directory
        self.modules_path = os.path.join(os.path.dirname(__file__), 'modules')
        sys.path.append(self.modules_path)
        # Load enabled modules
        with open(self.modules_path + r'\.modules', 'r') as file:
            names = json.load(file)
            self.modules = {name: import_module(f'.{name}', 'archbucket.core.modules') for name in names.keys() if names[name] == 'enabled'}
            for module in self.modules.values():
                module.run = error_handler.func_error_handler(module.run)

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
