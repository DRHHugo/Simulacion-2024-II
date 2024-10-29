from array import array as _array
from warnings import warn as _warn
from typing import Any as _Any
from . import _package_warning
from .variates import _NormalStd
from . import random_path as _ransom_path   

class _random_process:
    """parent class for stochastic process"""
    _main_type:str
    _sub_type:str
    def __str__(self)->str:
        return f'{self._main_type} {self._sub_type} stochastic process. All attributes are private.'
    def __repr__(self)->str:
        return 'blocked'
    def rand(self,stop:float=1.0)->random_path:
        return random_path(times=[0.0],events=[0.0])
    def sample(self,stop:float=1.0,size:int=1)->list[random_path]|None:
        """generation of size pseudo-random sample of variate"""
        return [self.rand(stop=stop) for _ in range(size)]

class WienerProcess(_random_process):
    def __new__(self,**kwargs):
        super().__init__()
    def __init__(self,**kwargs)->None:
        self._var:float
        self._stdev:float
        self._stdvariate:_NormalStd
        self._horizon:float 
        self._dt:float
        self._var = kwargs['var']
        self._stdev = self._var**0.5
        self._stdvariate = _NormalStd()
        self._dt = kwargs['dt'] if 'dt' in kwargs else 0.1
        self._horizon = kwargs['stop'] if 'stop' in kwargs else 1
    def rand(self,stop:float=1.0)->_random_path:
        times:list[float]
        X:list[float]
        times = [0.0]
        X = [0.0]
        while self._dt+times[-1]<self._horizon:
            X.append(X[-1]+self._stdev*self._stdvariate.rand())
            times.append(times[-1]+self._dt)
        X.append(X[-1]+(self._horizon-times[-1])*self._stdvariate.rand())
        times.append(self._horizon)
        return _random_path({0.0:0.0})