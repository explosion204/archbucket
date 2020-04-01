from . import manipulator
from . import server
from functools import wraps
import sys
import os
import inspect

def func_error_handler(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            filename = os.path.splitext(os.path.basename(inspect.getfile(function)))[0]
            # logging logic instead of 'print'
            print (f"{exc_type.__name__} occured. Module: '{filename}'. Function: '{function.__name__}'")
            return True
    return wrapper

def class_error_handler(cls):
    for name, member in inspect.getmembers(cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
        setattr(cls, name, func_error_handler(member))
    return cls