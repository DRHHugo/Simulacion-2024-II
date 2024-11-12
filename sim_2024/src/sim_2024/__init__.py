from typing import Any as _Any
from typing import Callable as _Callable
from array import array as _array
from os import urandom as _urandom
from os import path as _path
from warnings import warn as _warn  
from matplotlib import font_manager as _font_manager
from matplotlib import rcParams as _rcParams
from matplotlib import pyplot as _pyplot
from matplotlib.figure import Figure as _Figure
from matplotlib import colormaps as _colormaps

#change font for matplotlib figures
_dir_path = _path.dirname(_path.realpath(__file__))

_font_manager.fontManager.addfont(_dir_path+'\\lmroman12-regular.otf')
_font_manager.fontManager.addfont(_dir_path+'\\lmsans12-regular.otf')
_rcParams.update({
    'font.serif': 'Latin Modern Roman',
    'font.sans-serif': 'Latin Modern Sans',
    'font.size': 8,
    'savefig.bbox':'tight'
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
        sample:random_sample
        _warn_int(size,'size of sample must be a posituve integer',threshold=1)
        sample = random_sample()
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
    def __new__(cls,function:_Any,**kwargs):
        if not '__call__' in function.__dir__():
            raise AttributeError('function is not callable')
        if 'min' in kwargs:
            _validate_float(kwargs['min'],'min must be a float')
        if 'max' in kwargs:
            _validate_float(kwargs['max'],'max must be a float')
        if 'min' in kwargs and 'max' in kwargs:
            if kwargs['max']<=kwargs['min']:
                raise ValueError('max value must be greater that min value')
        return super().__new__(cls)

    def __init__(self,function:_Any,**kwargs):
        self._function:_Any
        self._min: str|float
        self._max: str|float
        if 'min' in kwargs:
            self._min = kwargs['min']
        else:
            self._min = '-inf'
        if 'max' in kwargs:
            self._max = kwargs['max']
        else:
            self._max = '+inf'
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
    """array subclass to represent a realization of a random process
    
    A realization is an indexed set of observations of a random process wich is assumed to be indexed by continum time.
    The _type attribute is set to continuos if the undarlay process is of continuos paths and to jump if is a jump process.
    This class also defines some related functions and functionalities.
    
    Args:
        initializer (iterable): if provided it must be an iterable object whose
    """
    
    def __new__(cls,initializer:_Any=None):
        if initializer==None or '__iter__' in initializer.__dir__():
            return _array.__new__(cls,'d')
        else:
            raise TypeError('initializer is not iterable')
    
    def __init__(self,initializer:_Any=None)->None:
        if not initializer==None:
            for elem in initializer:
                self.append(elem)
    
    @property
    def mean(self)->float:
        return sum(self)/len(self)
    
    def make_plot(self,*args,**kwargs)->_Figure:
        fig:HistogramFigure
        try:
            fig = _pyplot.figure(*args,**dict({'FigureClass':HistogramFigure,'sample':self},**kwargs))
        finally:
            return fig

class process_path:
    """realization of a random process

    An observation over a period of the form [0,T] of a random process is called a realization.
    Value T is called horizon and is derived at izialitation time.
    A representation of such realization consist of an array of times and another one with the observed value for each time.
    Is assumed that both arrays are of the same length and that the value at any index corresponds to time at the same index.
    A random process can have contiuos or jumps paths, either one can be represneted in this class.
    Attribute _type is set to continum for contonuos paths and to jump for jumps paths.
    For both types of paths the attribute _auto must be set to on if the value of the realization at a time not given at inizialization can be derived as the weight average between the two closets times.
    
    Args:
        times (array[float]|list[float]): times for wich the process has been observed
        X (array[float]|list[float]): values for wich the process has been observed
        type_par (str): the type of path that the process have, continum or jump.
        auto (bool): Treu if the value of the realization at a time not given at inizialization can be derived.
    """
    def __new__(cls,times:_array[float]|list[float],X:_array[float]|list[float],type_par:str='continum',auto:bool=False):
        if type(auto)!=bool:
            raise TypeError('auto must a bool value')
        if type(type_par)!=str:
            raise TypeError('type_par must be of str type')
        else:
            if type_par!='continum' and type_par!='jump':
                raise ValueError('type_par must be continum or jump')
        if type(times)==_array and type(X)==_array:
            if len(times)>=0 and len(X)>=0 and len(times)==len(X):
                return super().__new__(cls)
            else:
                raise ValueError('times and X parameters must be arrays of the same length')
        elif type(times)==list and type(X)==list:
            _validate_list(times,'all elemnts of first parameter must be floats')
            _validate_list(X,'all elemnts of second parameter must be floats')
            if len(times)>0 and len(X)>0 and len(times)==len(X):
                return super().__new__(cls)
            else:
                raise ValueError('first and second parameters must be lists of the same length')
        else:
            raise TypeError('first and second parameters must both be arrays or lists of the same length')
    def __init__(self,times:_array[float]|list[float],X:_array[float]|list[float],type_path:str,auto:bool=False)->None:
        self._times:_array[float]
        self._X:_array[float]
        self._horizon:float
        self._type_path:type_path
        self._auto:bool
        self._type_path = type 
        self._auto = auto
        if type(times)==_array:
            self._times = times
            self._X = X
        else:
            self._times = _array('d',times)
            self._X = _array('d',X)
        self._horizon = max(times)
    def __len__(self):
        return len(self._times)
    
    def __getitem__(self, i:int)->tuple:
        return (self._times[i],self._X[i])
    
    def __call__(self,time:float)->float:
        if time in self._times:
            return self._X[self._times.index(time)]
        else:
            raise ValueError('time not in path')

    def get_values(self)->list[tuple]:
        i:int
        return [(self._times[i],self._X[i]) for i in range(len(self._times))]
    
    def append(self,Xt:tuple[float])->None:
        if type(Xt)!=tuple:
            _warn('appended value must be a tuple of two float values',category=_package_warning)
        if len(Xt)!=2:
            _warn('appended value must be a tuple of two float values',category=_package_warning)
        if type(Xt[0])!=float or type(Xt[1])!=float:
            _warn('appended value must be a tuple of two float values',category=_package_warning)
        self._times.append(Xt[0])
        self._X.append(Xt[1])

    def make_plot(self,*args,**kwargs)->None:
        fig:PathFigure
        color:str
        if not 'color' in kwargs:
            kwargs['color'] = 'xkcd:cobalt'
        if not 'linewidth' in kwargs:
            kwargs['linewidth'] = 0.75
        try:
            fig=_pyplot.figure(*args,**dict({'FigureClass':PathFigure,'paths':self},**kwargs))
        finally:
            return fig

class process_sample:
    """sample of process paths
    
    List of process paths and related functions. The process can be a continuous or jumps process but is assumed to be of in continum time.
    Attribute _paths must be a list of process_path elements, each one is a realization of a process.

    Args:
        paths (list[random_paths]): list of random_paths
    """
    
    def __init__(self,paths:list[process_path]):
        self._paths:list[process_paths]
        self._maxhorizon:float
        self._paths = paths
        self._maxhorizon = max([path._horizon for path in paths])
    
    def __len__(self)->int:
        return len(self._paths)

    def __getitem__(self,i:int)->process_path:
        return self._paths[i]

    def get_values(self)->list[tuple[_array,_array]]:
        return [path.get_values() for path in self._paths]
    
    @property
    def mean(self)->process_path:
        times:_array[float]
        means:_array[float]
        means = _array('d')
        t:float
        i:int
        times = self._paths[0]._times
        for t in times:
            sample = []
            for path in self._paths:
                try:
                    i = path._times.index(t)
                except:
                    raise IndexError('times for paths in sample are different')
                finally:
                    sample.append(path._X[i])
            means.append(sum(sample)/len(sample))
        return process_path(times,means,self._paths[0]._type,self._paths[0]._auto)
    
    def make_plot(self,*args,**kwargs):
        fig:PathFigure
        try:
            fig = _pyplot.figure(*args,**dict({'FigureClass':PathFigure,'paths':self},**kwargs))
        finally:
            return fig

class HistogramFigure(_Figure):
    """custom matplotlib Figure to plot a density histogram
    
    This custom figure allows to create a histogram of a sample of float values in a pre-defined format.
    *args and *Keyword arguments are passed to figure inizialization and to histogram creation.

    Args:
        sample (random_sample): random_sample to plot
    """
    def __init__(self,sample:random_sample,**kwargs):
        _validate_sample(sample,message='sample must be a random_sample object')
        if 'figsize' in kwargs:
            if type(kwargs['figsize'])==tuple:
                figsize = kwargs.pop('figsize')
            else:
                figsize = tuple([5,3])
        else:
            figsize = tuple([5,3])
        if 'dpi' in kwargs:
            if type(kwargs['dpi'])==int:
                dpi = kwargs.pop('dpi')
            else:
                dpi = 400
        else:
            dpi = 400
        if 'bins' in kwargs:
            if type(kwargs['bins'])==int or type(kwargs['bins'])==list:
                bins = kwargs.pop('bins')
            else:
                bins = 10
        else:
            bins = 10
        super().__init__(**kwargs)
        self.set_size_inches(figsize[0],figsize[1])
        self.set_dpi(dpi)
        self.add_axes((0,0,1,1))
        _,_,bars = self.axes[0].hist(sample,bins=bins,density=True)
        for bar in bars:
            bar.set_facecolor('xkcd:azure')
            bar.set_edgecolor('xkcd:white')
        self.canvas.toolbar_visible = False
        self.canvas.header_visible = False
        self.canvas.footer_visible = False
    def add_function(self,function:mass_function|density_function,**kwargs)->None:
        xmin:float
        xmax:float
        xrange:_array
        yrange:_array
        if 'range' in kwargs:
            if type(kwargs['range'])==tuple:
                xmin = kwargs['range'][0]
                xmax = kwargs['range'][1]
            else:
                raise TypeError('range must a tuple')
        else:
            xmin = float(self.axes[0].get_xlim()[0])
            xmax = float(self.axes[0].get_xlim()[1])
        if type(function)==density_function:
            x:float
            dx:float
            xmax_minus_dx:float
            xrange = _array('d')
            yrange = _array('d')
            if 'dx' in kwargs:
                if type(kwargs['dx']==float):
                    dx = kwargs['dx']
                else:
                    _warn('dx not a float, value set to 0.01 ',category=_package_warning)
                    dx = 0.01
            else:
                dx = 0.01
            x = xmin
            xmax_minus_dx = xmax-dx
            while x<xmax_minus_dx:
                xrange.append(x)
                yrange.append(function(x))
                x+=dx
            xrange.append(xmax)
            yrange.append(function(xmax))
            self.axes[0].plot(xrange,yrange,color='xkcd:wine')
        elif type(function)==mass_function:
            x:float
            radius:float
            marker:str
            xrange = _array('d')
            yrange = _array('d')
            if 'r' in kwargs:
                if type(kwargs['r'])==float:
                    radius = kwargs['r']
                else:
                    _warn('r not a float, value set to 0.25 ',category=_package_warning)
                    radius = 0.25
            else:
                radius = 0.25
            if 'marker' in kwargs:
                marker = kwargs['marker']
            else:
                marker = 'o'
            for x in function._support:
                if xmin<=x<=xmax:
                    xrange.append(x)
                    yrange.append(function(x))
            self.axes[0].scatter(xrange,yrange,s=radius*72,marker=marker,color='xkcd:wine')

class PathFigure(_Figure):
    """custom matplotlib Figure to plot a realization from a random process
    """
    def __init__(self,paths:process_path|process_sample|list[process_path],**kwargs)->None:
        _timesS:list[_array]
        _XS:list[_array]
        _type_paths:str
        if type(paths)==process_path:
            _timesS = [paths._times]
            _XS = [paths._X]
            _type_paths = paths._type_path
        elif type(paths)==process_sample:
            _timesS = [path._times for path in paths]
            _XS = [path._X for path in paths]
            _type_paths = paths[0]._type_path
        elif type(paths)==list:
            for path in paths:
                if type(path)!=process_path:
                    raise TypeError('path(s) must be a process path, process sample or list of process paths')
            _timesS = [path._time for path in paths]
            _XS = [path._X for ppath in paths]
            _type_paths = paths[0]._type_path
        else:
            raise TypeError('path(s) must be a process path, process sample or list of process paths')
        if 'figsize' in kwargs:
            if type(kwargs['figsize'])==tuple:
                figsize = kwargs.pop('figsize')
            else:
                figsize = tuple([5,3])
        else:
            figsize = tuple([5,3])
        if 'dpi' in kwargs:
            if type(kwargs['dpi'])==int:
                dpi = kwargs.pop('dpi')
            else:
                dpi = 400
        else:
            dpi = 400
        if 'color' in kwargs:
            if type(kwargs['color'])==str:
                color = kwargs.pop('color')
            else:
                color = 'winter'
        else:
            color = 'winter'
        if 'linewidth' in kwargs:
            if type(kwargs['linewidth'])==float:
                linewidth = kwargs.pop('linewidth')
            else:
                linewidth=0.5
        else:
            linewidth=0.5
        super().__init__(**kwargs)
        self.set_size_inches(figsize[0],figsize[1])
        self.set_dpi(dpi)
        self.add_axes((0,0,1,1))
        if _type_paths=='continum':
            if color in _colormaps:
                for i in range(len(_XS)):
                    self.axes[0].plot(_timesS[i],_XS[i],color=_colormaps[color]((i+1)/len(paths)),linewidth=linewidth)
            else:
                for i in range(len(_XS)):
                    self.axes[0].plot(_timesS[i],_XS[i],color=color,linewidth=linewidth)
        elif _type_paths=='jump':
            if color in _colormaps:
                for i in range(len(_XS)):
                    self.axes[0].plot(_timesS[i],_XS[i],color=_colormaps[color]((i+1)/len(paths)),linewidth=linewidth)
            else:
                for i in range(len(_XS)):
                    self.axes[0].plot(_timesS[i],_XS[i],color=color,linewidth=linewidth)    
        else:
            raise TypeError('unknown type of path(s)')
        self.canvas.toolbar_visible = False
        self.canvas.header_visible = False
        self.canvas.footer_visible = False

    def add_path(self,path:process_path,**kwargs):
        if type(path)!=process_path:
            raise TypeError('path must be of type process_sample or process_path')
        if 'color' in kwargs:
            if type(kwargs['color'])==str:
                color = kwargs.pop('color')
            else:
                color = 'red'
        else:
            color = 'red'
        if 'linewidth' in kwargs:
            if type(kwargs['linewidth'])==float:
                linewidth = kwargs.pop('linewidth')
            else:
                linewidth=0.75
        else:
            linewidth=0.75
        self.axes[0].plot([path[i][0] for i in range(len(path))],[path[i][1] for i in range(len(path))],color=color,linewidth=linewidth)

#elements to export

__all__ = [
    'rand',
    'set_seed',
    'mass_function',
    'density_function',
    'HistogramFigure',
    'random_sample'
    ]