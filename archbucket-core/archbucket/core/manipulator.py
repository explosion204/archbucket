import ast
import json
import os
import re

from constants import API_PATH, DISABLED, ENABLED, MODULES_PATH

def import_module(module_name, source_code) -> (bool, str):
    try:
        ast.parse(source_code)
    except SyntaxError:
        return (False, 'Syntax error.')

    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)
        modules_dict[module_name] = DISABLED

    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)

    with open(MODULES_PATH + f'/{module_name}.py', 'w') as file:
        file.write(source_code)

    return (True, f"Module '{module_name}' imported. Restart bot to apply changes.")

def remove_module(module_name):
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)

    if module_name in modules_dict.keys():
        os.remove(MODULES_PATH + f'/{module_name}.py')
        modules_dict.pop(module_name)
    else:
        return (False, f"Cannot find module with name '{module_name}'.")

    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)

    return (True, f"Module '{module_name}' removed. Restart bot to apply changes.")

def import_api(api_name, class_name, source_code) -> (bool, str):
    try:
        ast.parse(source_code)
    except SyntaxError:
        return (False, 'Syntax error.')

    with open(API_PATH + '/.api', 'r') as file:
        apis_dict = json.load(file)

    apis_dict[f'{api_name}'] = [class_name, DISABLED]
    
    with open(API_PATH + '/.api', 'w') as file:
        json.dump(apis_dict, file)

    with open(API_PATH + f'/{api_name}.py', 'w') as file:
        file.write(source_code)

    return (True, f"API '{api_name}' imported. Restart bot to apply changes.")

def remove_api(api_name):
    with open(API_PATH + '/.api', 'r') as file:
        api_dict = json.load(file)

    if api_name in api_dict.keys():
        os.remove(API_PATH + f'/{api_name}.py')
        api_dict.pop(api_name)
    else:
        return (False, f"Cannot find API with name '{api_name}'.")

    with open(API_PATH + '/.api', 'w') as file:
        json.dump(api_dict, file)

    return (True, f"API '{api_name}' removed. Restart bot to apply changes.")

def set_module_status(module_name, status):
    with open(MODULES_PATH + '/.modules', 'r') as file:
        modules_dict = json.load(file)

    if module_name in modules_dict.keys():
        modules_dict[module_name] = ENABLED if status == True else DISABLED
    else:
        return (False, f"Cannot find module with name '{module_name}'.")

    with open(MODULES_PATH + '/.modules', 'w') as file:
        json.dump(modules_dict, file)

    if status == True:
        return (True, f"Module '{module_name}' enabled. Restart bot to apply changes.")
    else:
        return (True, f"Module '{module_name}' disabled. Restart bot to apply changes.")

def set_api_status(api_name, status):
    with open(API_PATH + '/.api', 'r') as file:
        api_dict = json.load(file)

    if api_name in api_dict.keys():
        api_dict[api_name][1] = ENABLED if status == True else DISABLED
    else:
        return (False, f"Cannot find API with name '{api_name}'.")

    with open(API_PATH + '/.api', 'w') as file:
        json.dump(api_dict, file)

    if status == True:
        return (True, f"API '{api_name}' enabled. Restart bot to apply changes.")
    else:
        return (True, f"API '{api_name}' disabled. Restart bot to apply changes.")