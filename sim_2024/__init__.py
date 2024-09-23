#from exceptions import KeyError,TypeError,ValueError
from math import floor
from matplotlib import pyplot
from warnings import warn
from typing import Any

class package_warning(UserWarning):
    """package warning
    
    """
    pass

class GeneratorError(Exception):
    """exception raised when a generator raise a null state
    
    """
    def __init__(self):
        self.add_note('random generator raise a null state')

def _validate_int(x:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """validation for first paramater

    x must be an integer not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Error will be raised with the associated message error.

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

def _warn_int(x:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """equal to _validate_int but raise a warn instead of an error
    
    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success
        False otherwise
    
    """
    try:
        _validate_int(x,message,threshold,exceptions)
    except:
        warn(message,category=package_warning)
        return False
    else:
        return True

def _validate_int_by_key(kwargs:dict,key:str,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """_validate_int aplied to kwargs[key]

    This functions will raise an Error if kwargs[key] doesn't exists.
    If kwargs[key] exists, evaluate _validate_int(kwargs[key],message,threshold,exceptions)

    Args:
        kwargs : kwargs passed by another function
        key: key associated with the value to be validated
        message : message to be displayed when kwargs[key] isn't valid
        threshold : inferior threshold for kwargs[key]
        exceptions : one or more values not allowed for kwargs[key]

    Returns:
        True for success
        False otherwise
    
    """
    if not key in kwargs:
        raise KeyError(key+' key not found during inicialization. You should use '+key+'=value(s).')
        return False
    return _validate_int(kwargs[key],message,threshold,exceptions)

def _validate_list(l:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None):
    """validation for first parameter

    l must be a non empty list of integers and each one must be not inferior to threshold and not in exceptions to be valid.
    If l is not valid an apropiate Error will be raised with the associated message error.
    
    Args:
        l : variable to validate
        threshold : inferior threshold for integers in l
        exceptions : one or more values not allowed for integers in l
        message : message to be displayed when l isn't valid

    Returns:
        True for success
        False otherwise
    """

    if type(l)!=list:
        raise TypeError(message)
        return False
    if len(l)==0:
        raise ValueError(message)
        return False
    fails = [0 for i in range(len(l))]
    if type(exceptions)==int:
        exceptions=[exceptions]
    for i in range(len(l)):
        if b<threshold:
            num_fails+=1
        elif b
    return True

def _validate_list_by_key(kwargs:dict,key:str,exclude_all_zeros:bool=True)->bool:
    """validate list on kwargs

    This functions will raise an Error if kwargs[key] doesn't exists or if is not a list of integers.
    If exclude_all_zeros==True, it will also raise an Error if all elements on list kwargs[key] are zeros.

    Args:
        kwargs : kwargs passed from another function
        key: key associated with the list to be validated
        exclude_all_zeros : True if kwargs[key] can't be a list of zeros only

    Returns:
        True if kwargs[key] is a valid list of integers
        False otherwise
    
    """

    if not key in kwargs.keys():
        raise KeyError(key+' not found during inicialization. You should use '+key+'=list[value(s)]')
    if type(kwargs[key])!=list:
        raise TypeError(key+' should be a non empty list of integers')
    for x in kwargs[key]:
        _validate_int(x,key+' should be a non empty list of integers')
    if exclude_all_zeros:
        num_of_zeros = 0
        for x in kwargs[key]:
            if x==0:
                num_of_zeros+=1
        if num_of_zeros == len(kwargs[key]):
            raise ValueError(key+' can\'t be a list of zeros')
    return True

__all__ = [
    'floor',
    'pyplot',
    'warn',
    'Any',
    'package_warning',
    'GeneratorError',
    '_validate_int',
    '_validate_int_by_key',
    '_validate_list_by_key'
    ]