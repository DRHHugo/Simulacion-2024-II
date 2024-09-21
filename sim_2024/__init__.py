#from exceptions import KeyError,TypeError,ValueError
from math import floor
from matplotlib import pyplot
from warnings import warn
from inspect import currentframe
from typing import Any

class package_type_warning(UserWarning):
    """package type warning"""
    pass

class package_generator_error(Exception):
    """exception raised for a null generator"""
    pass

def _validate_int(x:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """
    validation for int arguments

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success
        False otherwise
    """
    if type(x)!=int:
        raise TypeError(message)
        return False
    if threshold!=None:
        if type(threshold)!=int:
            raise TypeError('inferior threshold must be an integer')
            return False
        if x<threshold:
            raise ValueError(message)
            return False
    if exceptions!=None:
        if type(exceptions)!=int and type(exceptions)!=list:
            raise TypeError('exceptions must be an integer or a list of integers')
            return False
        if type(exceptions)==int:
            if x==exceptions:
                raise ValueError(message)
                return False
        if type(exceptions)==list:
            for exc in exceptions:
                if type(exc)!=int:
                    raise TypeError('exceptions must be an integer or a list of integers')
                    return False
            for exc in exceptions:
                if x==exc:
                    raise ValueError(message)
                    return False
    return True

__all__ = ['floor', 'pyplot','warn','package_type_warning','package_generator_error','_validate_int']