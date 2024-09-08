#from exceptions import KeyError,TypeError,ValueError
from math import floor
from matplotlib import pyplot
from warnings import warn

class package_type_warning(UserWarning):
    """package type warning"""
    pass    

__all__ = ['floor', 'pyplot','package_type_warning','warn']