from typing import Any,Callable
from matplotlib import pyplot
from matplotlib import font_manager
from matplotlib import rc as matplotlib_rc
from matplotlib import rcParams as matplotlib_rcParams
from matplotlib import use as matplotlib_use
from os import urandom

#select backend and change font for matplotlib figures
matplotlib_use('notebook')
custom_font = font_manager.FontProperties(fname='C:\\Windows\\Fonts\\lmsans12-regular.otf')
font_manager.fontManager.addfont('C:\\Windows\\Fonts\\lmsans12-regular.otf')
matplotlib_rc('font', family='sans-serif') 
matplotlib_rcParams.update({
    'font.sans-serif': custom_font.get_name(),
    'font.size': 8
    })

def _validate_sample(sample:Any,message:str)->bool:
    if type(sample)!=list:
        raise TypeError(message)
    for x in sample:
        if type(x)!=float and type(x)!=int:
            raise TypeError(message)
    return True

class package_warning(UserWarning):
    """package warning
    
    """
    pass

class GeneratorError(Exception):
    """exception raised when a generator raise a null state
    
    """
    def __init__(self):
        self.add_note('random generator raise a null state')

class mass_function:
    """funcion de masa"""
    def __init__(self,f:dict[int,float])->None:
        self.__dict = dict(sorted(f.items()))
        keys = list(self.__dict.keys())
        self.__min = keys[0]
        self.__max = keys[-1]
    def __add__( self , g ) :
        len_f = self.__max-self.__min+1
        len_g = g.__max-g.__min+1
        f_values = [self.__min+k for k in range(len_f)]
        g_values = [g.__min+k for k in range(len_g)]
        new_weights = [[self(f_values[i])*g(g_values[k-i]) for i in range(max(0,k+1-len_g),min(k+1,len_f))] for k in range(len_f+len_g-1)]
        return mass_function({k+self.__min+g.__min:sum(new_weights[k]) for k in range(len(new_weights))})
    def __str__( self ) :
        return 'Funcion de masa'
    def __repr__( self ) :
        return 'mass_function from:'+repr(self.__dict)
    def __call__( self , x):
        return self.__dict.get(x,0)
    def get_dict( self ) -> dict[float:float]:
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

def HistogramFigure(sample:list[float],function:None|mass_function|density_function=None,bins:int|list[float]=10,**kwargs:Any):
    """function to create a density histogram with or without a density function 
    
    """
    _validate_sample(sample,message='later')
    figure:Figure = pyplot.figure(figsize=(5,3),dpi=200,frameon=False)
    freq,listbins,bars = pyplot.hist(sample,bins=bins,density=True)
    for bar in bars:
            bar.set_facecolor('xkcd:azure')
            bar.set_edgecolor('xkcd:white')
    if function != None:
        min_x = listbins[0]
        max_x = listbins[-1]
        xrange = [min_x+0.01*k for k in range(int((max_x-min_x)/0.01))]
        yrange = [function(x) for x in xrange]
        pyplot.plot(xrange,yrange,color='xkcd:indigo')
    return figure

class _package_generator:
    """class for package random generator
    
    """
    def __init__(self,seed:int)->None:
        self._mod_1:int = 2**32-209
        self._mod_2:int = 2**32-22853
        self._mults_1:list[int] = [0,1403580,-810728]
        self._mults_2:list[int] = [527612,0,-1370589]
        self._state_1:list[int] = [1,1,seed]
        self._state_2:list[int] = [1,1,1]
    def __str__(self)->str:
        return 'package default generator'
    def rand(self):
        """generation of one pseudo-random numbers

        """

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
        """generation of size pseudo-random numbers

        """

        if type(size)!=int:
            return []
        if size<=0:
            return []
        return [self.rand() for _ in range(size)]
    def _set_seed(self,seed):
        self._state_1:list[int] = [1,1,seed]
        self._state_2:list[int] = [1,1,1]

rand = _package_generator(int.from_bytes(urandom(4)))

def set_seed(seed:int)->None:
    global rand
    rand._set_seed(seed)
    return None

__all__ = [
    'mass_function',
    'density_function',
    'HistogramFigure',
    'rand',
    'set_seed'
    ]