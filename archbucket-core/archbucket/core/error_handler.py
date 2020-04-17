from . import manipulator
from . import server
from functools import wraps
import sys
import os
import inspect
import logging

from archbucket.core.constants import LOGFILES_PATH

logger = logging.getLogger(__name__)

if not os.path.exists(LOGFILES_PATH):
    os.makedirs(LOGFILES_PATH)

# clean up log file
if os.path.exists(LOGFILES_PATH + '/file.log'):
    file = open(LOGFILES_PATH + '/file.log', 'w')
    file.close()

f_handler = logging.FileHandler(LOGFILES_PATH + '/file.log')
f_handler.setLevel(logging.ERROR)

f_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
f_handler.setFormatter(f_format)

logger.addHandler(f_handler)

def func_error_handler(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            filename = os.path.splitext(os.path.basename(inspect.getfile(function)))[0]

            if filename == '__init__' and exc_type is NameError:
                # error can occure in import_module() function because of wrong imports or not imported types
                logger.error(f"NameError occured before module '{args[0][1:]}' had been completely imported. Check if module does all required imports and do not reference unknown types.") 
            else:
                logger.error(f"{exc_type.__name__} occured. Module: '{filename}'. Function: '{function.__name__}'")            
            
            return True
            
    return wrapper

def class_error_handler(cls):
    for name, member in inspect.getmembers(cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
        setattr(cls, name, func_error_handler(member))

    return cls