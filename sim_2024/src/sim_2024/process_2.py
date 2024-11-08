from array import array as _array
from sys import modules
from .variates import _NormalStd
from . import process_path as _process_path
from . import process_sample as _process_sample   

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
    def rand(self,**kwargs)->_process_path:
        pass
    def sample(self,size:int=1,**kwargs)->list[_process_path]|None:
        """generation of size pseudo-random sample of variate"""
        horizon = kwargs['horizon'] if 'horizon' in kwargs else 1.0
        dt = kwargs['granularity'] if 'granularity' in kwargs else 0.01
        return _process_sample('continum',[self.rand(horizon=horizon,granularity=dt) for _ in range(size)])

class WienerProcess(_random_process):
    """Standar Wiener process """
    def __init__(self):
        self._stdvariate = _NormalStd()
    def rand(self,**kwargs)->_process_path:
        dt = kwargs['granularity'] if 'granularity' in kwargs else 0.01
        stdev_dt = dt**0.5
        horizon = kwargs['horizon'] if 'horizon' in kwargs else 1.0
        times:_array
        X:_array
        times = _array('d')
        X = _array('d')
        times.append(0.0)
        X.append(0.0)
        while times[-1]+dt<horizon:
            X.append(X[-1]+stdev_dt*self._stdvariate.rand())
            times.append(times[-1]+dt)
        X.append(X[-1]+(horizon-times[-1])*self._stdvariate.rand())
        times.append(horizon)
        return _process_path(times=times,events=X)
