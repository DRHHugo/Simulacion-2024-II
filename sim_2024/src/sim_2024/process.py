from array import array as _array
from sys import modules
from .variates import _NormalStd
from .variates import Exponential as _Exponential
from . import process_path as _process_path
from . import process_sample as _process_sample   

try:
    rand = modules['sim_2024'].rand
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

class _random_process:
    """parent class for stochastic process"""
    _main_type:str
    _type_paths:str
    _auto_valuation:bool
    def __str__(self)->str:
        return f'{self._main_type} stochastic process. All attributes are private.'
    def __repr__(self)->str:
        return 'blocked'
    def rand(self,**kwargs)->_process_path:
        """generation of one pseudo-random sample of process"""
        pass
    def sample(self,size:int=1,**kwargs)->list[_process_path]|None:
        """generation of size pseudo-random sample of process"""
        horizon = kwargs['horizon'] if 'horizon' in kwargs else 1.0
        dt = kwargs['granularity'] if 'granularity' in kwargs else 0.01
        return _process_sample([self.rand(horizon=horizon,granularity=dt) for _ in range(size)])

class WienerProcess(_random_process):
    """Standar Wiener process """
    _main_type = 'Wiener standar'
    _type_paths = 'continum'
    _auto_valuation = False
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
        return _process_path(times,X,self._type_paths,self._auto_valuation)

class PoissonProcess(_random_process):
    """Homogeneous Poisson process """
    _main_type = 'Homogeneous Poisson'
    _type_paths = 'jump'
    _auto_valuation = True
    def __new__(cls,**kwargs):
        if 'rate' in kwargs:
            if type(kwargs['rate'])==float:
                if kwargs['rate']>0:
                    return super().__new__(cls)
                else:
                    raise ValueError('rate must be a positive float')
            else:
                raise TypeError('rate must be a positive float')
        else:
            raise KeyError('key argument rate not found during initialization')
    def __init__(self,**kwargs):
        self._exponential = _Exponential(rate=kwargs['rate'])
    def rand(self,**kwargs)->_process_path:
        times:_array
        X:_array
        t:float
        arrivals:int
        horizon = kwargs['horizon'] if 'horizon' in kwargs else 1.0
        times = _array('d')
        X = _array('d')
        times.append(0.0)
        X.append(0.0)
        t = self._exponential.rand()
        arrivals = 1
        while t<horizon:
            times.append(t)
            X.append(arrivals)
            t+=self._exponential.rand()
            arrivals+=1
        return _process_path(times,X,self._type_paths,self._auto_valuation)