from typing import Any as _Any
from typing import Callable as _Callable
from sys import modules as _modules
from os import getcwd as _getcwd
from matplotlib import font_manager as _font_manager
from matplotlib import pyplot as _pyplot
from matplotlib.figure import Figure as _Figure
from matplotlib import rcParams as _rcParams
from . import _validate_sample
from . import _validate_float

#change font for matplotlib figures
try:
    _font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmsans12-regular.otf')
    _font_manager.fontManager.addfont(_getcwd()+'\\sim_2024\\lmroman12-regular.otf')
    _rcParams.update({
    'font.serif': 'Latin Modern Roman',
    'font.sans-serif': 'Latin Modern Sans',
    'font.size': 8
    })
except:
    pass

try:
    'sim_2024' in _modules.keys()
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

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
        min (float): density_functión evaluate to zero below min, min=-inf is used when min=-infinity
        max (float): density_functión evaluate to zero above max, max=+inf is used when max=+infinity
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

def HistogramFigure(sample:list[float],function:None|mass_function|density_function=None,bins:int|list[float]=10,label:str='',**kwargs:dict):
    """function to create a density histogram with or without a density function"""
    _validate_sample(sample,message='later')
    figure:_Figure
    if label=='':
        figure = _pyplot.figure(figsize=(5,3),dpi=200,frameon=False)
    else:
        figure = _pyplot.figure(num=label,figsize=(5,3),dpi=200,frameon=False)
    _,listbins,bars = _pyplot.hist(sample,bins=bins,density=True)
    for bar in bars:
            bar.set_facecolor('xkcd:azure')
            bar.set_edgecolor('xkcd:white')
    if label!='':
        figure.axes[0].set_title(label)
    if type(function)==density_function:
        min_x:float = listbins[0]
        max_x:float = listbins[-1]
        xrange:list[float] = [min_x+0.01*k for k in range(int((max_x-min_x)/0.01))]
        yrange:list[float] = [function(x) for x in xrange]
        _pyplot.plot(xrange,yrange,color='xkcd:indigo')
    try:
        figure.canvas.toolbar_visible = False
        figure.canvas.header_visible = False
        figure.canvas.footer_visible = False
    finally:
        return figure

__all__ = [
    'mass_function',
    'density_function',
    'HistogramFigure',
    ]