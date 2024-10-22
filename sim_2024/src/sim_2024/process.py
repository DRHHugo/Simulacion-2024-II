from typing import Any
from warnings import warn
from . import _package_warning

class _random_process:
    """parent class for stochastic process
    
    """
    _main_type:str
    _sub_type:str
    def __str__(self)->str:
        return f'{self._main_type} {self._sub_type} stochastic process. All attributes are private.'
    def __repr__(self)->str:
        return 'blocked'
    def rand(self,stop:float=1.0):
        pass
    def sample(self,stop:float=1.0,size:int=1)->list[float]|None:
        """generation of size pseudo-random sample of variate"""
        return [self.rand() for _ in range(size)]
