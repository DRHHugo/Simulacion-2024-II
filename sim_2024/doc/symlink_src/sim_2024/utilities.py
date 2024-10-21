from typing import Any,Callable
from warnings import warn
from sys import modules
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib import font_manager
from matplotlib import rc
from matplotlib import rcParams
from . import _validate_sample
from . import _package_warning

#change font for matplotlib figures
try:
    font_manager.fontManager.addfont('C:\\Windows\\Fonts\\lmsans12-regular.otf')
    rc('font', family='sans-serif') 
    custom_font = font_manager.FontProperties(fname='C:\\Windows\\Fonts\\lmsans12-regular.otf')
    rcParams.update({
    'font.sans-serif': custom_font.get_name(),
    'font.size': 8
    })
except:
    pass

try:
    'sim_2024' in modules.keys()
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

class mass_function:
    """funcion de masa"""
    def __init__(self,function:Callable[[float],float],sup:list[float])->None:
        self._function:Any = function
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
    """funcion de densidad"""
    def __init__(self,function:Callable[[float],float],min:float|None=None,max:float|None=None):
        self._min:float|str = float(min) if isinstance(min,int) or isinstance(min,float) else "-inf"
        self._max:float|str = float(max) if isinstance(max,int) or isinstance(max,float) else "+inf"
        self._function:Callable[[float],float] = function
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

def HistogramFigure(sample:list[float],function:None|mass_function|density_function=None,bins:int|list[float]=10,label:str='',**kwargs:dict[str,Any]):
    """function to create a density histogram with or without a density function"""
    _validate_sample(sample,message='later')
    figure:Figure
    if label=='':
        figure = pyplot.figure(figsize=(5,3),dpi=200,frameon=False)
    else:
        figure = pyplot.figure(num=label,figsize=(5,3),dpi=200,frameon=False)
    _,listbins,bars = pyplot.hist(sample,bins=bins,density=True)
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
        pyplot.plot(xrange,yrange,color='xkcd:indigo')
    try:
        figure.canvas.header_visible = False
        figure.canvas.footer_visible = False
        figure.canvas.toolbar_visible = False
    finally:
        return figure

__all__ = [
    'mass_function',
    'density_function',
    'HistogramFigure',
    ]