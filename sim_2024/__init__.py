#from exceptions import KeyError,TypeError,ValueError
from math import floor
from matplotlib import pyplot

class package_type_warning(UserWarning):
    """package type warning"""
    def __init__(self,message):
        self.args=(message)
        

__all__ = ['floor', 'pyplot','package_type_warning']