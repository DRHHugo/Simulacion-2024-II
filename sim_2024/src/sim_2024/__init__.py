from typing import Any as _Any
from typing import Callable as _Callable
from array import array as _array
from os import urandom as _urandom
from os import getcwd as _getcwd
from warnings import warn as _warn  
from matplotlib import font_manager as _font_manager
from matplotlib import rcParams as _rcParams
from matplotlib import pyplot as _pyplot
from matplotlib.figure import Figure as _Figure

#change font for matplotlib figures

_font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmroman12-regular.otf')
_font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmsans12-regular.otf')
_rcParams.update({
    'font.serif': 'Latin Modern Roman',
    'font.sans-serif': 'Latin Modern Sans',
    'font.size': 8
    })

#custom errors and warnings

class _package_warning(UserWarning):
    """Warning for error handling
    
    Warning raised when an error occurs with a function or class defined in this package.
    """
    pass

class _generator_Error(Exception):
    """Exception for pseudorandom generator
    
    Exception raised when a generator raise a null state, that is, the generator is incapable to produce more pseudorandom numbers.
    """
    def __init__(self):
        self.add_note('random generator raise a null state')

#validation functions

def _validate_int(x:_Any,message:str='',threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """Validation for an integer.

    x must be an integer not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Error will be raised with the associated message error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success validation
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

def _warn_int(x:_Any,message:str='',threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """Validation for an integer.
    
    x must be an integer not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Warning will be raised with the associated message error.
    Similar to _validate_int but raise a warn instead of an error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success validation
        False otherwise
    """
    try:
        _validate_int(x,message,threshold,exceptions)
    except:
        _warn(message,category=_package_warning)
        return False
    else:
        return True

def _validate_int_by_key(kwargs:dict[str,_Any],key:str,message:str='',threshold:None|int=None,exceptions:None|int|list[int]=None)->bool:
    """Validation for an integer on a dictionary.

    This functions will raise an Error if kwargs[key] doesn't exists.
    If kwargs[key] exists, evaluate _validate_int(kwargs[key],message,threshold,exceptions).

    Args:
        kwargs : kwargs passed by another function
        key: name of parameter to validate
        message : message to be displayed when kwargs[key] isn't valid
        threshold : inferior threshold for kwargs[key]
        exceptions : one or more values not allowed for kwargs[key]

    Returns:
        True for success validation
    """
    if not key in kwargs:
        raise KeyError(key+' key not found during inicialization. You should use '+key+'=value(s).')
    return _validate_int(kwargs[key],message,threshold,exceptions)

def _validate_float(x:_Any,message:str='',threshold:None|float=0.0,exceptions:None|float|list[float]=None)->bool:
    """Validation for float.

    x must be a float not inferior to threshold and not in exceptions to be valid.
    If x is not valid an apropiate Error will be raised with the associated message error.

    Args:
        x : variable to validate
        threshold : inferior threshold for x
        exceptions : one or more values not allowed for x
        message : message to be displayed when x isn't valid

    Returns:
        True for success validation
    """
    if type(x)!=float:
        raise TypeError(message)
    if threshold!=None:
        if type(threshold)!=float:
            raise TypeError('inferior threshold must be a float')
        if x<threshold:
            raise ValueError(message)
    if exceptions!=None:
        if type(exceptions)!=float and type(exceptions)!=list:
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

def _validate_float_by_key(kwargs:dict[str,_Any],key:str,message:str='',threshold:None|float=None,exceptions:None|float|list[float]=None)->bool:
    """Validation for an float on a dictionary.

    This functions will raise an Error if kwargs[key] doesn't exists.
    If kwargs[key] exists, evaluate _validate_float(kwargs[key],message,threshold,exceptions)

    Args:
        kwargs : kwargs passed by another function
        key: name of parameter to validate
        message : message to be displayed when kwargs[key] isn't valid
        threshold : inferior threshold for kwargs[key]
        exceptions : one or more values not allowed for kwargs[key]

    Returns:
        True for success validation
    """
    if not key in kwargs:
        raise KeyError(key+' key not found during inicialization. You should use '+key+'=value(s).')
        return False
    return _validate_float(kwargs[key],message,threshold,exceptions)

def _validate_list(l:_Any,message:str='',threshold:None|int=None,exceptions:None|int|list[int]=None):
    """Validation for an array of integers.

    l must be a non empty list of integers and each one must be not inferior to threshold and not in exceptions to be valid.
    If l is not valid an apropiate Error will be raised with the associated message error.
    
    Args:
        l : array to validate
        threshold : inferior threshold for integers in l
        exceptions : one or more values not allowed for integers in l
        message : message to be displayed when l isn't valid

    Returns:
        True for success validation
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

def _validate_list_by_key(kwargs:dict[str,_Any],key:str,exclude_all_zeros:bool=True)->bool:
    """Validation for an array on a dictionary.

    This functions will raise an Error if kwargs[key] doesn't exists or if is not a list of integers.
    If exclude_all_zeros==True, it will also raise an Error if all elements on list kwargs[key] are zeros.

    Args:
        kwargs : kwargs passed from another function
        key: key associated with the list to be validated
        exclude_all_zeros : True if kwargs[key] can't be a list of zeros only

    Returns:
        True for success validation
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

def _validate_sample(sample:_Any,message:str='')->bool:
    """Validate if sample is a sample.

    This functions will raise an Error with message=message if sample is not a non-empty array of pseudorandom numbers.
    
    Args:
        sample : array to validate
    
    Returns:
        True for success validation
    """
    if type(sample)!=random_sample:
        raise TypeError(message)
    for x in sample:
        if type(x)!=float and type(x)!=int:
            raise TypeError(message)
    return True

#pseudorandom default generator and related functions

class _package_generator:
    """Class reserved for main pseudorandom generator.
    
    This class provide the default pseudorandom generator on package initialization.
    This pseudorandom generator is an implementation of L'Ecuyer* MRG32k3a specification.
    When the package is first imported the generator is initialized with a random number provided by the host system.
    After that is possible to restart the generator with the set_seed function.
    This class is not intended to be used to construct another generator, if desire use multcombi_congruential_generator class to construct an equivalent generator.
    *L'Ecuyer, P. Uniform random number generation. Ann Oper Res 53, 77-120 (1994).
    
    Args:
        seed : integer to initilizate the pseudorandom generator
    """
    
    def __str__(self)->str:
        return 'package default generator'
    
    def __call__(self,n:None|int=None)->float|list[float]|None:
        if n==None:
            return self.rand()
        if type(n)==int:
            return self.sample(n)
        else:
            _warn(message='invalid parameter')
            return None
    
    def __init__(self,seed:int)->None:
        """all attributes are private"""
        self._mod_1:int = 2**32-209
        self._mod_2:int = 2**32-22853
        self._mults_1:list[int] = [0,1403580,-810728]
        self._mults_2:list[int] = [527612,0,-1370589]
        self._state_1:list[int] = [1,1,seed%self._mod_1]
        self._state_2:list[int] = [1,1,1]
    
    def rand(self)->float:
        """generation of one pseudo-random numbers"""
        x:int = 0
        y:int = 0
        for i in range(len(self._state_1)):
            x = (x+self._state_1[i]*self._mults_1[i])%self._mod_1
            y = (y+self._state_2[i]*self._mults_2[i])%self._mod_2
        z:int = (x-y)%self._mod_1
        self._state_1.pop(0)
        self._state_2.pop(0)
        self._state_1.insert(len(self._state_1),x)
        self._state_2.insert(len(self._state_2),y)
        return z/self._mod_1
    
    def sample(self,size:int=1)->list[float]|None:
        """generation of a sample of pseudo-random numbers of length size
        
        Keyword Args:
            size (int): size of sample
        """
        _warn_int(size,'size of sample must be a posituve integer',threshold=1)
        sample = random_sample('d')
        for _ in range(size):
            sample.append(self.rand())
        return sample

    def _set_seed(self,seed)->None:
        """restart the state"""
        self._state_1 = [1,1,seed]
        self._state_2 = [1,1,1]
        return None

rand = _package_generator(int.from_bytes(_urandom(4)))

def set_seed(seed:int)->None:
    """Change state of default pseudorandom generator.

    This functions allows to set the state of the default pseudorandom generator for reproductibility porpuses.
    If seed is not an integer it raise a Warning and no change is done.

    Args:
        seed: integer used to restart the default pseudorandom generator
    """
    if _warn_int(seed,message='seed must be an integer'):
        rand._set_seed(seed)
    return None

#probability and statistics utilities

class mass_function:
    """funcion de masa"""
    def __init__(self,function:_Callable[[float],float],sup:list[float])->None:
        self._function:_Any = function
        self._support:list[float] = sup
    def __str__(self) :
        return 'Funcion de masa'
    def __repr__(self) :
        return f'mass_function with:\\n support:'+repr(self._sup)+'\\n formula:'+repr(self._support)
    def __call__(self,x):
        return self._function(x)
    #    def __add__(self,g:mass_function) :
    #        len_f:float = self.__max-self.__min+1
    #        len_g:float = g.__max-g.__min+1
    #        f_values:list[float] = [float(self.__min+k) for k in range(len_f)]
    #        g_values:list[float] = [g.__min+k for k in range(len_g)]
    #        new_weights:list[float] = [[self(f_values[i])*g(g_values[k-i]) for i in range(max(0,k+1-len_g),min(k+1,len_f))] for k in range(len_f+len_g-1)]
    #        return mass_function({float(k+self.__min+g.__min):sum(new_weights[k]) for k in range(len(new_weights))})

class density_function:
    """funcion de densidad
    
    Clase de abstracción de una función de densidad de probabilidad.

    Args:
        function (Callable): functión used to evaluate density_function between min and max args.

    Keyword Args:
        min (float): density_functión evaluate to zero below min
        max (float): density_functión evaluate to zero above max
        """
    def __new__(cls,function:_Callable[[float],float],**kwargs):
        if 'min' in kwargs:
            _validate_float(kwargs['min'],'min must be a float')
        if 'max' in kwargs:
            _validate_float(kwargs['max'],'max must be a float')
        if 'min' in kwargs and 'max' in kwargs:
            if kwargs['max']<=kwargs['min']:
                raise ValueError('max value must be greater that min value')

    def __init__(self,function:_Callable[[float],float],**kwargs):
        self._function:_Callable[[float],float]
        self._min: str|float
        self._max: str|float
        if 'min' in kwargs:
            self._min = kwargs['min']
        else:
            self._min = '-inf'
        if 'max' in kwargs:
            self._min = kwargs['max']
        else:
            self._min = '+inf'
        self._function = function
    
    def __call__(self,x:float)->float:
        if type(self._min) is float and type(self._max) is float:
            if self._min<=x and x<=self._max:
                return self._function(x)
            else:
                return 0
        elif type(self._min) is float:
            if self._min<=x:
                return self._function(x)
            else:
                return 0
        else:
            return self._function(x)

class random_sample(_array):
    """custom type to store an array of float xor int values and some functionalities related

    Sample has to porpuses. First, store a potentialy huge amount of numbers (either float or int) 

    """
    
    # def __init__(self)->None:
    #     self._array:_array
    #     self._array = _array('d')
        
    # def get_values(self)->_array:
    #     return self._array
    
    # def add_value(self,x:float)->None:
    #     self._array.append(x)
    
    def make_plot(self,*args,**kwargs)->_Figure:
        return _pyplot.figure(self,*args,**kwargs,FigureClass=HistogramFigure)

class random_path:
    def __init__(self,times:_array[float],events:_array[float])->None:
        self._times:_array[float]
        self._events:_array[float]
        self._times = times
        self._events = events
        self._horizon = max(times)
    
    def get_values(self)->tuple[_array,_array]:
        return self._times,self._events
    
    def make_plot(self,**kwargs)->None:
        return PathFigure(self._times,self._events,**kwargs)

class process_sample:
    def __init__(self,paths:list[random_path]):
        self._paths = paths
        self._maxhorizon = max([path._horizon for path in paths])
    def get_values(self)->list[tuple[_array,_array]]:
        return [path.get_values() for path in self._paths]
    def make_plot(self,**kwargs):
        paths = [path.get_values() for path in self._paths]
        return PathFigure([path[0] for path in paths],[path[1] for path in paths],**kwargs)

class HistogramFigure(_Figure):
    """custom matplotlib Figure to plot a density histogram
    
    This custom figure allows to create a histogram of a sample of float values in a pre-defined format.
    *args and *Keyword arguments are passed to figure inizialization and to histogram creation.

    Args:
        sample (random_sample): random_sample to plot
    """
    def __new__(cls,sample:random_sample,*args,**kwargs):
        _validate_sample(sample,message='sample must be a random_sample object')
        if len(args)==0:
            args=(None,(5,3),200)
        if len(args)==1:
            args+=((5,3),200)
        if len(args)==2:
            args+=(200)
        return super().__init__(*args,**dict({'frameon':False},**kwargs))
    def __init__(self,sample:random_sample,*args,**kwargs):
        _,_,bars = self.axes[0].hist(sample,**dict({'bins':bins},{'density':True},**kwargs))
        for bar in bars:
            bar.set_facecolor('xkcd:azure')
            bar.set_edgecolor('xkcd:white')
        try:
            self.canvas.toolbar_visible = False
            self.canvas.header_visible = False
            self.canvas.footer_visible = False
        finally:
            return figure

def PathFigure(times:_array|list[_array],events:_array|list[_array],**kwargs:dict[str,_Any])->_Figure:
    """function to create a plot for random process realizations"""
    _times = list[_array]
    _events = list[_array]
    if type(times)==_array:
        _times = [times]
    else:
        _times = times
    if type(events)==_array:
        _events = [events]
    else:
        _events = events
    figure:_Figure
    figure = pyplot.figure(figsize=(5,3),dpi=300,frameon=False,**kwargs)
    figure.add_axes((0,0,1,1))
    figure.axes[0].plot(_times,_events,**kwargs)
    try:
        figure.canvas.toolbar_visible = False
        figure.canvas.header_visible = False
        figure.canvas.footer_visible = False
    finally:
        return figure

#elements to export
__all__ = [
    'rand',
    'set_seed',
    'mass_function',
    'density_function',
    'HistogramFigure',
    'random_sample'
    ]