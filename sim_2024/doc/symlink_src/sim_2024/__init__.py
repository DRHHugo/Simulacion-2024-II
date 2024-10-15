from typing import Any
from warnings import warn
#from matplotlib import font_manager
#from matplotlib import rc
#from matplotlib import rcParams
from os import urandom

#select backend and change font for matplotlib figures
#matplotlib_use('notebook')
#font_manager.fontManager.addfont('C:\\Windows\\Fonts\\lmsans12-regular.otf')
#rc('font', family='sans-serif') 
#custom_font = font_manager.FontProperties(fname='C:\\Windows\\Fonts\\lmsans12-regular.otf')
#rcParams.update({
#    'font.sans-serif': _custom_font.get_name(),
#    'font.size': 8
#    })

class _package_warning(UserWarning):
    """package warning"""
    pass

class _Generator_Error(Exception):
    """exception raised when a generator raise a null state"""
    def __init__(self):
        self.add_note('random generator raise a null state')

def _validate_int(x:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """validation for integer paramater

    x must be an integer not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Error will be raised with the associated message error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success
    """
    if type(x)!=int:
        raise TypeError(message)
    if threshold!=None:
        if type(threshold)!=int:
            raise TypeError('inferior threshold must be an integer')
        if x<threshold:
            raise ValueError(message)
    if exceptions!=None:
        if type(exceptions)!=int and type(exceptions)!=list:
            raise TypeError('exceptions must be an integer or a list of integers')
        if type(exceptions)==int:
            if x==exceptions:
                raise ValueError(message)
        if type(exceptions)==list:
            for exc in exceptions:
                if type(exc)!=int:
                    raise TypeError('exceptions must be an integer or a list of integers')
            for exc in exceptions:
                if x==exc:
                    raise ValueError(message)
    return True

def _warn_int(x:Any,message:str,threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """similar to _validate_int but raise a warn instead of an error
    
    x must be an integer not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Warning will be raised with the associated message error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success
    """
    try:
        _validate_int(x,message,threshold,exceptions)
    except:
        warn(message,category=_package_warning)
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
    """
    if not key in kwargs:
        raise KeyError(key+' key not found during inicialization. You should use '+key+'=value(s).')
    return _validate_int(kwargs[key],message,threshold,exceptions)

def _validate_float(x:Any,message:str,threshold:None|float=0.0,exceptions:None|float|list[float]=None)->bool:
    """validation for float paramater

    x must be a float not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Error will be raised with the associated message error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success
    """
    if type(x)!=float:
        raise TypeError(message)
    if threshold!=None:
        if type(threshold)!=float:
            raise TypeError('inferior threshold must be a float')
        if x<threshold:
            raise ValueError(message)
    if exceptions!=None:
        if type(exceptions)!=int and type(exceptions)!=list:
            raise TypeError('exceptions must be an integer or a list of integers')
        if type(exceptions)==int:
            if x==exceptions:
                raise ValueError(message)
        if type(exceptions)==list:
            for exc in exceptions:
                if type(exc)!=int:
                    raise TypeError('exceptions must be an integer or a list of integers')
            for exc in exceptions:
                if x==exc:
                    raise ValueError(message)
    return True

def _validate_float_by_key(kwargs:dict,key:str,message:str,threshold:None|float=None,exceptions:None|float|list[float]=None)->bool:
    """_validate_float aplied to kwargs[key]

    This functions will raise an Error if kwargs[key] doesn't exists.
    If kwargs[key] exists, evaluate _validate_float(kwargs[key],message,threshold,exceptions)

    Args:
        kwargs : kwargs passed by another function
        key: key associated with the value to be validated
        message : message to be displayed when kwargs[key] isn't valid
        threshold : inferior threshold for kwargs[key]
        exceptions : one or more values not allowed for kwargs[key]

    Returns:
        True for success
    
    """
    if not key in kwargs:
        raise KeyError(key+' key not found during inicialization. You should use '+key+'=value(s).')
        return False
    return _validate_float(kwargs[key],message,threshold,exceptions)

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
    """
    if type(l)!=list:
        raise TypeError(message)
        return False
    if len(l)==0:
        raise ValueError(message)
        return False
    fails:list[int] = [0 for i in range(len(l))]
    exceptions_list:list[int] =[]
    if type(exceptions)==int:
        exceptions_list.append(exceptions)
    for i in range(len(l)):
        if threshold!=None:
            if l[i]<threshold:
                fails[i] = 1
        if l[i] in exceptions_list:
            fails[i] = 1
    if sum(fails)==len(l):
        raise ValueError(message)
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

def _validate_sample(sample:Any,message:str)->bool:
    if type(sample)!=list:
        raise TypeError(message)
    for x in sample:
        if type(x)!=float and type(x)!=int:
            raise TypeError(message)
    return True

class _package_generator:
    """class for package random generator"""
    def __str__(self)->str:
        return 'package default generator'
    def __call__(self)->float:
        return self.rand()
    def __init__(self,seed:int)->None:
        self._mod_1:int = 2**32-209
        self._mod_2:int = 2**32-22853
        self._mults_1:list[int] = [0,1403580,-810728]
        self._mults_2:list[int] = [527612,0,-1370589]
        self._state_1:list[int] = [1,1,seed]
        self._state_2:list[int] = [1,1,1]
    def rand(self):
        """generation of one pseudo-random numbers"""
        x = 0
        y = 0
        for i in range(len(self._state_1)):
            x = (x+self._state_1[i]*self._mults_1[i])%self._mod_1
            y = (y+self._state_2[i]*self._mults_2[i])%self._mod_2
        z = (x-y)%self._mod_1
        self._state_1.pop(0)
        self._state_2.pop(0)
        self._state_1.insert(len(self._state_1),x)
        self._state_2.insert(len(self._state_2),x)
        return z/self._mod_1
    def sample(self,size:int=1)->list[float]|None:
        """generation of size pseudo-random numbers"""
        if type(size)!=int:
            return []
        if size<=0:
            return []
        return [self.rand() for _ in range(size)]
    def _set_seed(self,seed)->None:
        self._state_1 = [1,1,seed]
        self._state_2 = [1,1,1]
        return None

rand = _package_generator(int.from_bytes(urandom(4)))

def set_seed(seed:int)->None:
    rand._set_seed(seed)
    return None

__all__ = [
    'rand',
    'set_seed',
]