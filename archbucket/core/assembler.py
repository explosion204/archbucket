from os import listdir
from os.path import isfile, isdir, join
from importlib.util import spec_from_file_location, module_from_spec
import inspect
from multiprocessing import Queue
import re
import sys

from archbucket.components import AbstractAPI, AbstractScript
from .bot import Bot


def assemble(path):
    path_to_api = join(path, 'api')
    path_to_scripts = join(path, 'scripts')
    path_to_config = join(path, 'config.py')
    include_pattern = re.compile('^[\w_]+\.[\w_]+$')
    api_dict, scripts_dict = dict(), dict()

    # existence check up
    if not isdir(path_to_api):
        # (success flag, message, object)
        return (False, 'Cannot find directory "api".')

    if not isdir(path_to_scripts):
        return (False, 'Cannot find directory "scripts".')

    if not isfile(path_to_config):
        return (False, 'Cannot find file "config.py".')

    # reading config preferences
    spec = spec_from_file_location('config.py', path_to_config)
    config = module_from_spec(spec)
    spec.loader.exec_module(config)

    # config: pipelines count
    try:
        pipelines_count = config.PIPELINES_COUNT
    except AttributeError:
        return (False, 'config.py: Cannot find attribute "PIPELINES COUNT".')

    # config: api list
    try:
        included_api = config.INCLUDED_API
    except AttributeError:
        return (False, 'config.py: Cannot find attribute "INCLUDED_API".')

    for api_location in included_api:
        if re.match(include_pattern, api_location):
            api_file, api_class = api_location.split('.')
        else:
            return (False, 'config.py: API inclusion record must be like "filename.classname".')

        spec = spec_from_file_location(api_file, join(path_to_api, api_file + '.py'))
        api_module = module_from_spec(spec)
        spec.loader.exec_module(api_module)

        for cls_name, cls_object in inspect.getmembers(api_module, inspect.isclass):
            if issubclass(cls_object, AbstractAPI):
                name = cls_object.Meta.name if cls_object.Meta.name else cls_name
                api_dict[name] = cls_object

    # config: scripts list
    try:
        included_scripts = config.INCLUDED_SCRIPTS
    except AttributeError:
        return (False, 'config.py: Cannot find attribute "INCLUDED_SCRIPTS".')

    for script_location in included_scripts:
        if re.match(include_pattern, script_location):
            script_file, script_class = script_location.split('.')
        else:
            return (False, 'config.py: Script inclusion record must be like "filename.classname".')

        spec = spec_from_file_location(script_file, join(path_to_scripts, script_file + '.py'))
        script_module = module_from_spec(spec)
        spec.loader.exec_module(script_module)

        for cls_name, cls_object in inspect.getmembers(script_module, inspect.isclass):
            if issubclass(cls_object, AbstractScript):
                name = cls_object.Meta.name if cls_object.Meta.name else cls_name
                scripts_dict[name] = cls_object

    return (True, Bot(api_dict, scripts_dict, pipelines_count))
