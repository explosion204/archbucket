from importlib import import_module
from os.path import exists
from .request import Request
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


    def route(self, request: Request):
        command = request.command
        # check if user has an active session
        if request.id in self.sessions:
            # get name of active module
            module_name = self.sessions[request.id]
            # module of active session treats command as request argument too
            request.args.insert(0, request.command)
            # enter module and get flag if session must be closed
            try:
                session_exit = self.modules[module_name].run(request)
            except Exception as e:
                print(f'[error]: Module {module_name} removed from system.\n{str(e)}')
                session_exit = True
                self.remove_module(module_name)
            if session_exit:
                del self.sessions[request.id]
            return
        try:
            session_exit = self.modules[command].run(request)
        except KeyError:
            return
        except Exception as e:
            print(f'[error]: Module {module_name} removed from system.\n{str(e)}')
            session_exit = True
            self.remove_module(module_name)
        # add session to track dictionary if script needs it
        if not session_exit:
            self.sessions[request.id] = request.command

    def import_module(self, module_name, source_code) -> (bool, str):
        try:
             ast.parse(source_code)
        except SyntaxError:
            return (False, 'Syntax error.')
        pattern = r'def run\((.|\n)*\)(.|\n)*return (False|True)'
        if not re.search(pattern, source_code):
             return (False, "Module has no callable attribute 'run' which returns True or False.")
        # successful validation
        with open(self.modules_path + '/.modules', 'r') as file:
            modules_dict = json.load(file)
            modules_dict[module_name] = 'disabled'
        with open(self.modules_path + '/.modules', 'w') as file:
            json.dump(modules_dict, file)
        with open(self.modules_path + f'/{module_name}.py', 'w') as file:
            file.write(source_code)
        return (True, f"Module '{module_name}' successfully imported. Restart bot to apply changes.")

    def remove_module(self, module_name):
        del self.modules[module_name]
        with open(self.modules_path + '/.modules', 'r') as file:
            modules_dict = json.load(file)
            if module_name in modules_dict.keys():
                os.remove(self.modules_path + f'/{module_name}.py')
                del modules_dict[module_name]
            else:
                return (False, f"Cannot find module '{module_name}'.")
        with open(self.modules_path + '/.modules', 'w') as file:
            json.dump(modules_dict, file)
        return (True, f"Module '{module_name}'' successfully removed. Restart bot to apply changes.")

    def enable_module(self, module_name):
        with open(self.modules_path + '/.modules', 'r') as file:
            modules_dict = json.load(file)
            if module_name in modules_dict.keys():
                modules_dict[module_name] = 'enabled'
            else:
                return (False, f"Cannot find module '{module_name}'.")
        with open(self.modules_path + '/.modules', 'w') as file:
            json.dump(modules_dict, file)
        return (True, f"Module '{module_name}' successfully enabled. Restart bot to apply changes.")

    def disable_module(self, module_name):
        with open(self.modules_path + '/.modules', 'r') as file:
            modules_dict = json.load(file)
            if module_name in modules_dict.keys():
                modules_dict[module_name] = 'disabled'
            else:
                return (False, f"Cannot find module '{module_name}'.")
        with open(self.modules_path + '/.modules', 'w') as file:
            json.dump(modules_dict, file)
        return (True, f"Module '{module_name}' successfully disabled. Restart bot to apply changes.")