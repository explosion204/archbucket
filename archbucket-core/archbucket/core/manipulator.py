import json
import ast
import re
import os

MODULES_PATH = os.path.join(os.path.dirname(__file__), 'modules')
API_PATH = os.path.join(os.path.dirname(__file__), 'api')

def import_module(module_name, source_code) -> (bool, str):
    try:
        ast.parse(source_code)
    except SyntaxError:
        return (False, 'Syntax error.')
    pattern = r'def run\((.|\n)*\)(.|\n)*return (False|True)'
    if not re.search(pattern, source_code):
        return (False, "Module has no callable attribute 'run' which returns True or False.")
    # successful validation
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)
        modules_dict[module_name] = 'disabled'
    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)
    with open(MODULES_PATH + f'/{module_name}.py', 'w') as file:
        file.write(source_code)
    return (True, f"Module '{module_name}' successfully imported. Restart bot to apply changes.")

def remove_module(module_name):
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)
        if module_name in modules_dict.keys():
            os.remove(MODULES_PATH + f'/{module_name}.py')
            del modules_dict[module_name]
        else:
            return (False, f"Cannot find module '{module_name}'.")
    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)
    return (True, f"Module '{module_name}' successfully removed. Restart bot to apply changes.")

def enable_module(module_name):
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)
        if module_name in modules_dict.keys():
            modules_dict[module_name] = 'enabled'
        else:
            return (False, f"Cannot find module '{module_name}'.")
    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)
    return (True, f"Module '{module_name}' successfully enabled. Restart bot to apply changes.")

def disable_module(module_name):
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)
        if module_name in modules_dict.keys():
            modules_dict[module_name] = 'disabled'
        else:
            return (False, f"Cannot find module '{module_name}'.")
    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)
    return (True, f"Module '{module_name}' successfully disabled. Restart bot to apply changes.")

def import_api(api_name, class_name, source_code) -> (bool, str):
    try:
        ast.parse(source_code)
    except SyntaxError:
        return (False, 'Syntax error.')
    if not re.search(r'\tdef __init__\(self\):', source_code):
        return (False, "API class must have '__init__' member function which takes one argument (including 'self')")
    if not re.search(r'\tdef start\(self, [^\s\n]+\):', source_code):
        return (False, "API class must have 'start' member function which takes two arguments (including 'self')")
    if not re.search(r'\tdef stop\(self\):', source_code):
        return (False, "API class must have 'stop' member function which takes one argument (including 'self')")
    if not re.search(r'\tdef send_response\(self, [^\s\n]+\):', source_code):
        return (False, "API class must have 'send_response' member function whick takes two arguments (including 'self')")
    with open(API_PATH + '/.api', 'r') as file:
        apis_dict = json.load(file)
        apis_dict[f'{api_name}'] = [class_name, 'disabled']
    with open(API_PATH + '/.api', 'w') as file:
        json.dump(apis_dict, file)
    with open(API_PATH + f'/{api_name}.py', 'w') as file:
        file.write(source_code)
    return (True, f"API class '{api_name}' successfully imported. Restart bot to apply changes.")

def remove_api(api_name):
    with open(API_PATH + '/.api', 'r') as file:
        api_dict = json.load(file)
        if api_name in api_dict.keys():
            del api_dict[api_name]
        else:
            return (False, f"Cannot find API with name '{api_name}'")
    with open(API_PATH + '/.api', 'w') as file:
        json.dump(api_dict, file)
    return (True, f"API {api_name} successfully removed. Restart bot to apply changes.")

def enable_api(api_name):
    with open(API_PATH + '/.api', 'r') as file:
        api_dict = json.load(file)
        if api_name in api_dict.keys():
            api_dict[api_name][1] = 'enabled'
        else:
            return (False, f"Cannot find API with name '{api_name}'")
    with open(API_PATH + '/.api', 'w') as file:
        json.dump(api_dict, file)
    return (True, f"API '{api_name}' successfully enabled. Restart bot to apply changes.")

def disable_api(api_name):
    with open(API_PATH + '/.api', 'r') as file:
        api_dict = json.load(file)
        if api_name in api_dict.keys():
            api_dict[api_name][1] = 'disabled'
        else:
            return (False, f"Cannot find API with name '{api_name}'")
    with open(API_PATH + '/.api', 'w') as file:
        json.dump(api_dict, file)
    return (True, f"API '{api_name}' successfully disabled. Restart bot to apply changes.")