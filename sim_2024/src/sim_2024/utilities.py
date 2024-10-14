from typing import Any,Callable
from matplotlib import pyplot
from matplotlib.figure import Figure
from . import _validate_sample

class mass_function:
    """funcion de masa"""
    def __init__(self,f:dict[float,float])->None:
        self.__dict:dict[float,float] = dict(sorted(f.items()))
        keys:list[float] = list(self.__dict.keys())
        self.__min:float = keys[0]
        self.__max:float = keys[-1]
#    def __add__(self,g:mass_function) :
#        len_f:float = self.__max-self.__min+1
#        len_g:float = g.__max-g.__min+1
#        f_values:list[float] = [float(self.__min+k) for k in range(len_f)]
#        g_values:list[float] = [g.__min+k for k in range(len_g)]
#        new_weights:list[float] = [[self(f_values[i])*g(g_values[k-i]) for i in range(max(0,k+1-len_g),min(k+1,len_f))] for k in range(len_f+len_g-1)]
#        return mass_function({float(k+self.__min+g.__min):sum(new_weights[k]) for k in range(len(new_weights))})
    def __str__(self) :
        return 'Funcion de masa'
    def __repr__(self) :
        return 'mass_function from:'+repr(self.__dict)
    def __call__(self,x):
        return self.__dict.get(x,0)
    def get_dict(self) -> dict[float,float]:
        return self.__dict

class density_function:
    """funcion de densidad"""
    def __init__(self,function:Callable[[float],float],min:float|None=None,max:float|None=None):
        self.min:float|str = float(min) if isinstance(min,int) or isinstance(min,float) else "-inf"
        self.max:float|str = float(max) if isinstance(max,int) or isinstance(max,float) else "+inf"
        self._function:Callable[[float],float] = function
    def __call__(self,x:float)->float:
        if type(self.min) is float and type(self.max) is float:
            if self.min<=x and x<=self.max:
                return self._function(x)
            else:
                return 0
        elif type(self.min) is float:
            if self.min<=x:
                return self._function(x)
            else:
                return 0
        else:
            return self._function(x)

def HistogramFigure(sample:list[float],function:None|mass_function|density_function=None,bins:int|list[float]=10,**kwargs:dict[str,Any]):
    """function to create a density histogram with or without a density function"""
    _validate_sample(sample,message='later')
    figure:Figure = pyplot.figure(figsize=(5,3),dpi=200,frameon=False)
    freq,listbins,bars = pyplot.hist(sample,bins=bins,density=True)
    for bar in bars:
            bar.set_facecolor('xkcd:azure')
            bar.set_edgecolor('xkcd:white')
    if function!=None:
        min_x:float = listbins[0]
        max_x:float = listbins[-1]
        xrange:list[float] = [min_x+0.01*k for k in range(int((max_x-min_x)/0.01))]
        yrange:list[float] = [function(x) for x in xrange]
        pyplot.plot(xrange,yrange,color='xkcd:indigo')
    return figure

__all__ = [
    'mass_function',
    'density_function',
    'HistogramFigure',
    'set_seed'
    ]