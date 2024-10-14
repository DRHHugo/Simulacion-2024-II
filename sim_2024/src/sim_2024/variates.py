from typing import Any as _Any
from . import _validate_float_by_key
from . import _validate_int_by_key
from .utilities import mass_function as _mass_function
from importlib.util import find_spec as _find_spec
from sys import modules

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
    """representation of a random variate of Bernoulli type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Bernoulli'

    def __new__(cls,**kwargs:_Any):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:_Any):
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self.mass_function:_mass_function = _mass_function({0.0:1-self._p,1.0:self._p})
    def rand(self)->float:
        global rand
        u = rand.rand()
        if u<self._p:
            return 1.0
        else:
            return 0.0

class Binomial(_discrete_variate):
    """representation of a random variate of binonimal type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
        n (int): Number of trials
    """
    _sub_type = 'Binomial'

    def __new__(cls,**kwargs:_Any):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        _validate_int_by_key(kwargs,'n','number of trials must be a positive integer',threshold=1)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:_Any):
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self._n:float = kwargs['n']

__all__ = [
    'Bernoulli',
    'Binomial'
]