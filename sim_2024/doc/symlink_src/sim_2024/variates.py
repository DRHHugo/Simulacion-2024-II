from typing import Any
from sys import modules
from math import log
from . import _validate_float_by_key
from . import _validate_int_by_key
from . import _validate_int
from . import _validate_list
from .utilities import mass_function

try:
    rand = modules['sim_2024'].rand
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

class _random_variate:
    """parent class for random variates
    
    """
    _main_type:str
    _sub_type:str
    def __str__(self)->str:
        return f'{self._main_type} {self._sub_type} pseudorandom generator. All attributes are private.'
    def __repr__(self)->str:
        return 'blocked'
    def rand(self):
        pass
    def sample(self,size:int=1)->list[float]|None:
        """generation of size pseudo-random sample of variate"""
        return [self.rand() for _ in range(size)]

class _discrete_variate(_random_variate):
    """parent class for discrete random variates"""
    _main_type = 'discrete'

class _continuos_variate(_random_variate):
    """parent class for continuos random variates
    
    """
    _main_type = 'continuos'

class Bernoulli(_discrete_variate):
    """Representation of a random variate of Bernoulli type
    
    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Bernoulli'
    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:Any):
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self.mass_function:mass_function = mass_function(function=lambda x:(self._p if x==1 else 1-self._p),sup=[0,1])
    def rand(self)->float:
        global rand
        u = rand.rand()
        if u<self._p:
            return 1.0
        else:
            return 0.0

class Binomial(_discrete_variate):
    """representation of a random variate of binonimal type
    
    Keyword Args:
        p (float): Sucess probability
        n (int): Number of trials
    """
    _sub_type = 'Binomial'
    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        _validate_int_by_key(kwargs,'n','number of trials must be a positive integer',threshold=1)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:Any):
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self._n:float = kwargs['n']
    def rand(self)->float:
        pass

class Geometric(_discrete_variate):
    """Representation of a random variate of Bernoulli type
    
    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Geometric'
    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs)->None:
        """All Attributes are private"""
        self._p:float = kwargs['p']
    def rand(self)->float:
        #global rand
        u = rand()
        x =  0.0
        while u>self._p:
            u = rand()
            x+= 1
        return x

class NegativeBinomial(_discrete_variate):
    """representation of a random variate of Bernoulli type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Negative binomial'
    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs)->None:
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self._s:float = kwargs['s']
    def rand(self)->float:
        #global rand
        s = 1 if rand()<self._p else 0
        x = 0 if s==1 else 1
        while s<self._s:
            s+= 1 if rand()<self._p else 0
            x+= 0 if s==1 else 1
        return x

class DiscreteUniform(_discrete_variate):
    """Discrete uniform distribution

    """
    def __new__(cls,**kwargs:dict[Any,Any]):
        """validation of parameters occurs here"""
        size:bool = True if 'size' in kwargs else False
        sup:bool = True if 'sup' in kwargs else False
        if not (size^sup):
            raise KeyError('initialization must include one and just one:size or sup')
        if 'size' in kwargs:
            _validate_int(kwargs['size'],'size must be an integer greater that 1',2)
        if 'sup' in kwargs:
            _validate_list(kwargs['sup'],'sup must be a list of int or float numbers')
            if len(kwargs['sup'])<2:
                raise ValueError('sup must be a list of size at leats 2')
        return super().__new__(cls)
    def __init__(self,**kwargs:dict[Any,Any]) -> None:
        self._type:str = 'size' if ('size' in kwargs) else 'sup'
        self._size:int
        self._sup:list[int]|None
        if self._type=='size':
            self._size = kwargs['size']
            self._sup = None
        else:
            self._sup = kwargs['sup']
            self._size = len(self._sup)
    def rand(self)->float:
        u:float = rand()
        index:float = 1.0
        while u>index/self._size:
            index+=1.0
        if self._sup==None:
            return index
        else:
            return self._sup[int(index)-1]

class Exponential(_continuos_variate):
    def __init__(self,**kwargs:dict):
        self._rate:float = kwargs['rate']
    def rand(self)->float:
        u = rand()
        return -log(u)/self._rate

class _NormalStd(_continuos_variate):
    def __init__(self):
        pass
    def _rand(self):
        s=2
        while s>1:
            u = rand()
            v = rand()
            x = 2*u -1
            y = 2*v -1
            s = x**2+y**2
        return (x*((-2*log(s)/s)**0.5),y*((-2*log(s)/s)**0.5))
    def rand(self):
        _rand()[0]
    def sample(self,size:int=1)->list[float]|None:
        pairs = [self._rand() for _ in range(size//2+size%2)]
        _sample = []
        for k in range(size//2):
            _sample.append(pairs[k][0])
            _sample.append(pairs[k][1])
        if len(_sample)<size:
            _sample.append(pairs[-1][0])
        return _sample

class Normal(_continuos_variate):
    def __init__(self,**kwargs):
        self._mean:float = kwargs['mean']
        if 'var' in kwargs:
            self._var:float = kwargs['var']
            self._stdev:float = self._var**0.5
        if 'stdev'in kwargs:
            self._stdev:float = kwargs['stdev']
            self._var = self._stdev**2
        self._stdvariate = _NormalStd()
    def rand(self):
        return self._mean+self._stdev*self._stdvariate().rand()
    def sample(self,size:int=1)->list[float]|None:
        _sample = self._stdev.sample(size)
        return [self._mean+self._stdev*z for z in sample]

class Chisq(_continuos_variate):
    def __init__(self,**kwargs):
        self._deg = kwargs['deg']
    def rand(self):
        X = NormalStd()
        sample = X.sample(self._deg)
        samplesq = [s**2 for s in sample]
        return sum(samplesq)
        
__all__ = [
    'Bernoulli',
    'Binomial',
    'Geometric',
    'NegativeBinomial',
    'DiscreteUniform',
    'Exponential',
    'Normal',
    'Chisq'
]