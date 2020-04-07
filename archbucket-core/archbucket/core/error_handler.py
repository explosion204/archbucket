from . import manipulator
from . import server
from functools import wraps
import sys
import os
import inspect
import logging

logger = logging.getLogger(__name__)
LOGFILES_PATH = os.path.join(os.path.dirname(__file__), '/logs')

if not os.path.exists(LOGFILES_PATH):
    os.makedirs(LOGFILES_PATH)

f_handler = logging.FileHandler(LOGFILES_PATH + 'file.log')
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
            logger.error(f"{exc_type.__name__} occured. Module: '{filename}'. Function: '{function.__name__}'")
            return True
            
    return wrapper

def class_error_handler(cls):
    for name, member in inspect.getmembers(cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
        setattr(cls, name, func_error_handler(member))

    return cls