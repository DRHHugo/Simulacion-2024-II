from sim_2024 import *

def _validate_mod(kwargs:dict)->bool:
    if not 'mod' in kwargs.keys():
        raise KeyError('mod not found during inicialization. You should use mod=value.')
    if type(kwargs['mod'])!=int:
        raise TypeError('mod should be a strictly positive integer')
    if kwargs['mod']<0:
        raise ValueError('mod should be a strictly positive integer')
    return True

def _validate_mult(kwargs:dict)->bool:
    if not 'mult' in kwargs.keys():
        raise KeyError('mult not found during inicialization. You should use mult=value.')
    if type(kwargs['mult'])!=int:
        raise TypeError('mult should be non zero integer')
    if kwargs['mult']==0:
        raise ValueError('mult should be non zero integer')
    return True

def _validate_seed(kwargs:dict,exclude_zero:bool=False)->bool:
    if not 'seed' in kwargs.keys():
        raise KeyError('seed not found during inicialization. You should use seed=value.')
    if type(kwargs['seed'])!=int:
        raise TypeError('seed should be a non zero integer')
    if exclude_zero and kwargs['seed']==0:
        raise TypeError('seed should be a non zero integer')
    return True

def _validate_cte(kwargs:dict)->bool:
    if not 'cte' in kwargs.keys():
        raise KeyError('cte not found during inicialization. You should use cte=value.')
    if type(kwargs['cte'])!=int:
        raise TypeError('cte should be an integer')
    return True if kwargs['cte']!=0 else False

class _random_generator:
    """parent class for random generators"""
    def __str__(self):
        return f'{self._main_type} {self._sub_type} pseudorandom generator. All properties are private.'
    def __repr__(self):
        return self.__str__()

class _congruential_generator(_random_generator):
    """parent class for congruential random generators"""
    _main_type = 'congruential'

class multiplicative_congruential_generator(_congruential_generator):
    """class for conrguential multiplicative pseudorandom generators"""
    _sub_type = 'multiplicative'
    def __new__(cls,**kwargs):
        _validate_mod(kwargs)
        _validate_mult(kwargs)
        _validate_seed(kwargs,exclude_zero=True)
        return super().__new__(cls)
    def __init__(self,**kwargs):
        self._mod = kwargs['mod']
        self._mult = kwargs['mult']%self._mod
        self._state = kwargs['seed']%self._mod
    @property
    def rand(self)->float:
        self._state = self._mult*self._state % self._mod
        return self._state/self._mod
    def sample(self,size:int)->list[float]|None:
        if size<0:
            return None
        if size==0:
            return []
        sample:list[float] = []
        while len(sample)<size and self._state!=0:
            self._state = self._mult*self._state%self._mod
            if self._state!=0:
                sample.append(self._state/self._mod)
        return sample

class linear_congruential_generator(_congruential_generator):
    """class for linear multiplicative pseudorandom generators"""
    _sub_type = 'linear'
    def __new__(cls,**kwargs):
        _validate_mod(kwargs)
        _validate_mult(kwargs)
        if _validate_cte(kwargs):
            return super().__new__(cls)
        else:
            package_type_warning('since cte=0 you will get a multiplicative congruential generator instead of a linear congruential generator')
            return multiplicative_congruential_generator(mod=kwargs['mod'],mult=kwargs['mult'],seed=kwargs['seed'])
    def __init__(self,**kwargs):
        if type(self!='linear_congruential_generator'):
            self._mod = kwargs['mod']
            self._mult = kwargs['mult']%self._mod
            self._cte = kwargs['cte']%self._mod
            self._state = kwargs['seed']%self._mod
    @property
    def rand(self)->float:
        self._state = (self._mult*self._state + self._cte)%self._mod
        return self._state/self._mod
    def sample(self,size:int)->list[float]|None:
        if size<0:
            return None
        if size==0:
            return []
        sample:list[float] = []
        while len(sample)<size and self._state!=0:
            self._state = (self._mult*self._state + self._cte)%self._mod
            if self._state!=0:
                sample.append(self._state/self._mod)
        return sample