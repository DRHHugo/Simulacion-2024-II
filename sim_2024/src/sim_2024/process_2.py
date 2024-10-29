from array import array as _array
from warnings import warn as _warn
from typing import Any as _Any
from sys import modules
from . import _package_warning
from .variates import _NormalStd
from . import random_path as _random_path   

try:
    rand = modules['sim_2024'].rand
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

class _random_process:
    """parent class for stochastic process"""
    _main_type:str
    _sub_type:str
    def __str__(self)->str:
        return f'{self._main_type} {self._sub_type} stochastic process. All attributes are private.'
    def __repr__(self)->str:
        return 'blocked'
    def rand(self,stop:float=1.0)->_random_path:
        return random_path(times=[0.0],events=[0.0])
    def sample(self,stop:float=1.0,size:int=1)->list[_random_path]|None:
        """generation of size pseudo-random sample of variate"""
        return [self.rand(stop=stop) for _ in range(size)]

class WienerProcess(_random_process):
    """Standar Wiener process """
    def __init__(self):
        self._stdvariate = _NormalStd()
    def rand(self,**kwargs)->_random_path:
        _dt = kwargs['dt'] if 'dt' in kwargs else 0.01
        _stdevdt = _dt**0.5
        _horizon = kwargs['stop'] if 'stop' in kwargs else 1
        times:_array
        X:_array
        times = _array('d')
        X = _array('d')
        times.append(0.0)
        X.append(0.0)
        while _dt+times[-1]<_horizon:
            X.append(X[-1]+_stdevdt*self._stdvariate.rand())
            times.append(times[-1]+_dt)
        X.append(X[-1]+(_horizon-times[-1])*self._stdvariate.rand())
        times.append(_horizon)
        return _random_path(times=times,events=X)