#from exceptions import KeyError,TypeError,ValueError
from math import floor
from matplotlib import pyplot
from warnings import warn
from inspect import currentframe

class package_type_warning(UserWarning):
    """package type warning"""
    pass

class package_generator_error(Exception):
    """exception raised for a null generator"""
    pass

__all__ = ['floor', 'pyplot','warn','package_type_warning','package_generator_error',]