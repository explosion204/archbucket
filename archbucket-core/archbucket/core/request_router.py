import importlib
import json
import os
import sys

from . import error_handler
from .request import Request
from archbucket.core.constants import MODULES_PATH

class RequestRouter:
    def __init__(self):
        self.modules = dict()
        self.sessions = dict()

        # path to 'modules' directory
        sys.path.append(MODULES_PATH)

        # Load enabled modules
        with open(MODULES_PATH + r'\.modules', 'r') as file:
            names = json.load(file)

        importlib.import_module = error_handler.func_error_handler(importlib.import_module)
        self.modules = {name: importlib.import_module(f'.{name}', 'archbucket.core.modules') for name in names.keys() if names[name] == 'enabled'}
        for module in self.modules.values():
            module = importlib.reload(module)
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
                self.sessions.pop(request.id)

        try:
            session_exit = self.modules[command].run(request)
        except KeyError:
            return None
            
        # add session to track dictionary if script needs it
        if not session_exit:
            self.sessions[request.id] = request.command
