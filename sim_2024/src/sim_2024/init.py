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
from matplotlib.patches import Circle as _Circle
from matplotlib import colormaps as _colormaps
#change font for matplotlib figures

_font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmroman12-regular.otf')
_font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmsans12-regular.otf')
_rcParams.update({
    'font.serif': 'Latin Modern Roman',
    'font.sans-serif': 'Latin Modern Sans',
    'font.size': 8,
    'savefig.bbox': 'tight'
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

#probability and statistics utilities

class mass_function:
    """funcion de masa
    
    
    """
    
    def __new__(cls,sup_val:dict[float,float]=None,**kwargs):
        if sup_val==None:
            if 'support' in kwargs and 'values' in kwargs:
                if type(kwargs['support'])==list and type(kwargs['values'])==list:
                    if len(kwargs['support'])>0 and len(kwargs['values'])>0 and len(kwargs['support'])==len(kwargs['values']):
                        if sum(kwargs['values'])==1.0:
                            return super().__new__(cls)
                        else:
                            raise ValueError('values sum not equals 1')
                    else:
                        raise ValueError('support and values must be non empty lists of the same size')
                else:
                        raise TypeError('support and values must be non empty lists of the same size')
            elif 'support' in kwargs:
                if type(kwargs['support'])==list:
                    if len(kwargs['support'])>0:
                        return super().__new__(cls)
                    else:
                        raise ValueError('support must be a non empty list')
                else:
                    raise TypeError('support must be a non empty list')
            else:
                raise KeyError('support not provided')
        elif type(sup_val)==dict:
            _validate_list(list(sup_val.keys()),message='dict keys must be all float numbers')
            _validate_list(list(sup_val.values()),message='dict values must be all float numbers')
            if sum(sup_val.values())==1.0:
                return super().__new__(cls)
            else:
                raise ValueError('dict values sum not equals 1')
        else:
            raise TypeError('first parameter must be a dictionary with float keys and values')
    
    def __init__(self,sup_val:dict[float,float]=None,**kwargs)->None:
        self._sup: list[float]
        self._val: list[float]
        if sup_val==None:
            if 'support' in kwargs and 'values' in kwargs:
                self._sup = kwargs['support']
                self._val = kwargs['values']
            else:
                self._sup = kwargs['support']
                self._val = [1/len(self._sup) for _ in range(len(self._sup))]
        else:
            self._sup = list(sup_val.keys())
            self._val = list(sup_val.values())
            
    def __str__(self) :
        return 'Funcion de masa'
    def __repr__(self) :
        return self.__str__()
    def __call__(self,x):
        try:
            return self._val[self._sup.index(x)]
        except:
            return 0.0

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
        return super().__new__(cls)

    def __init__(self,function:_Callable[[float],float],**kwargs):
        self._function:_Callable[[float],float]
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
    """custom type to store an array of float xor int values and some functionalities related

    Sample has to porpuses. First, store a potentialy huge amount of numbers (either float or int) 

    """
    def __new__(cls,*args):
        return super().__new__(cls,'d')
    def __init__(self,*args)->None:
        if len(args)==1:
            _validate_int(args[0],'single argument must be a positive integer',threshold=1)
            global rand
            for _ in range(args[0]):
                self.append(rand())
        elif len(args)==2:
            _validate_int(args[1],'second argument must be a positive integer',threshold=1)
            for _ in range(args[1]):
                self.append(args[0]())
        elif len(args)!=0:
            _warn('some arguments has bean ignored',type=_package_warning)
    def make_plot(self,*args,**kwargs)->_Figure:
        return _pyplot.figure(*args,**dict({'FigureClass':HistogramFigure,'sample':self},**kwargs))    
    @property
    def mean(self)->float:
        return sum(self)/len(self)

class process_path:
    def __new__(cls,times:_array[float]|list[float],events:_array[float]|list[float]):
        if type(times)==_array and type(events)==_array:
            if len(times)>0 and len(events)>0 and len(times)==len(events):
                return super().__new__(cls)
            else:
                raise ValueError('first and second parameters must be arrays of the same length')
        elif type(times)==list and type(events)==list:
            _validate_list(times,'all elemnts of first parameter must be floats')
            _validate_list(events,'all elemnts of second parameter must be floats')
            if len(times)>0 and len(events)>0 and len(times)==len(events):
                return super().__new__(cls)
            else:
                raise ValueError('first and second parameters must be lists of the same length')
        else:
            raise TypeError('first and second parameters must both be arrays or lists of the same length')
    
    def __init__(self,times:_array[float]|list[float],events:_array[float]|list[float])->None:
        self._times:_array[float]
        self._events:_array[float]
        self._horizon:float
        if type(times)==_array:
            self._times = times
            self._events = events
        else:
            self._times = _array('d',times)
            self._events = _array('d',events)
        self._horizon = max(times)
    
    def __len__(self):
        return len(self._times)
    
    def __getitem__(self, i):
        if i<0 or i>=len(self):
            _warn('indes out of range',category=_package_warning)
        else:
            return (self._times[i],self._events[i])
    
    def __call__(self,time:float)->float:
        if time in self._times:
            return self._events[self._times.index(time)]
        else:
            raise ValueError('time not in path')

    def get_values(self)->list[tuple]:
        i:int
        return [(self._times[i],self._events[i]) for i in range(len(self._times))]
    
    def make_plot(self,*args,**kwargs)->None:
        color:str
        if not 'color' in kwargs:
            kwargs['color'] = 'xkcd:cobalt'
        if not 'linewidth' in kwargs:
            kwargs['linewidth'] = 0.75
        return _pyplot.figure(*args,**dict({'FigureClass':PathFigure,'sample':self},**kwargs))

class process_sample:
    def __init__(self,paths:list[process_path]):
        self._paths = paths
        self._maxhorizon = max([path._horizon for path in paths])
    def __len__(self)->int:
        return len(self._paths)
    def __getitem__(self,i:int)->process_path:
        if i<0 or i>len(self):
            _warn('index out of range',category=_package_warning)
        else:
            return self._paths[i]
    def get_values(self)->list[tuple[_array,_array]]:
        return [path.get_values() for path in self._paths]
    def get_path(self,index:int)->process_path:
        if index<0 or index>=len(self._paths):
            _warn('index out of range',category=_package_warning)
        else:
            return self._paths[index]
    def make_plot(self,*args,**kwargs)->None:
        return _pyplot.figure(*args,**dict({'FigureClass':PathFigure,'sample':self},**kwargs))
    @property
    def mean(self)->process_path:
        times:_array
        mean_values:_array
        mean_values = _array('d')
        times = self._paths[0]._times
        for i in range(1,len(self)):
            for t in self._paths[i]._times:
                if not t in times:
                    times.append(t)
        times = _array('d',sorted(times))
        for t in times:
            try:
                l = [self._paths[i](t) for i in range(len(self))]
            except:
                raise IndexError('paths in sample are uncompatible')
            else:
                mean_values.append(sum(l)/len(l))
                del l
        return process_path(times,mean_values)

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
            if type(kwargs['bins']==int) or type(kwargs['bins']==list):
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
            for x in function._sup:
                if xmin<=x<=xmax:
                    xrange.append(x)
                    yrange.append(function(x))
            self.axes[0].scatter(xrange,yrange,s=radius*72,marker=marker,color='xkcd:wine')

class PathFigure(_Figure):
    """custom matplotlib Figure to plot a set of random paths
    
    This custom figure allows to create a figure of a set of random paths in a pre defined format.
    *args and *Keyword arguments are passed to figure inizialization and to plot creation.

    Args:
        sample_paths (process_sample): set of paths to plot
    """
    def __init__(self,sample:process_sample|process_path,**kwargs):
        if type(sample)!=process_sample and type(sample)!=process_path:
            raise TypeError('path(s) must be of type process_sample or process_path')
        sample_paths:process_sample
        if type(sample)==process_sample:
            sample_paths = sample
        else:
            sample_paths = process_sample([sample])
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
        if color in _colormaps:
            for j in range(len(sample_paths)):
                self.axes[0].plot([sample_paths[j][i][0] for i in range(len(sample_paths[0]))],[sample_paths[j][i][1] for i in range(len(sample_paths[0]))],color=_colormaps[color]((j+1)/len(sample_paths)),linewidth=linewidth)
        else:
            for j in range(len(sample_paths)):
                self.axes[0].plot([sample_paths[j][i][0] for i in range(len(sample_paths[0]))],[sample_paths[j][i][1] for i in range(len(sample_paths[0]))],color=color,linewidth=linewidth)
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

# def PathFigure(times:_array|list[_array],events:_array|list[_array],**kwargs:dict[str,_Any])->_Figure:
#     """function to create a plot for random process realizations"""
#     _times:list[_array]
#     _events:list[_array]
#     if type(times)==_array:
#         _times = [times]
#     else:
#         _times = times
#     if type(events)==_array:
#         _events = [events]
#     else:
#         _events = events
#     figure:_Figure
#     figure = _pyplot.figure(figsize=(5,3),dpi=300,frameon=False,**kwargs)
#     figure.add_axes((0,0,1,1))
#     figure.axes[0].plot(_times,_events,**kwargs)
#     try:
#         figure.canvas.toolbar_visible = False
#         figure.canvas.header_visible = False
#         figure.canvas.footer_visible = False
#     finally:
#         return figure

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
    
    def __call__(self,size:None|int=None)->float|random_sample:
        if size==None:
            return self.rand()
        _warn_int(size,'size of sample must be a positive integer',threshold=1)
        if size==1:
            return self.rand()
        return self.sample(size)

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
    
    def sample(self,size:int=1)->random_sample|None:
        """generation of a sample of pseudo-random numbers of length size
        
        Keyword Args:
            size (int): size of sample
        """
        _warn_int(size,'size of sample must be a posituve integer',threshold=1)
        sample = random_sample(self.rand,size)
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

#elements to export
__all__ = [
    'rand',
    'set_seed',
    'mass_function',
    'density_function',
    'random_sample',
    'random_path',
    'HistogramFigure',
    ]