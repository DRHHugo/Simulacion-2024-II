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

def _validate_poly_array(kwargs:dict,exclude_last_zero=False)->bool:
    if not 'mult' in kwargs.keys():
        raise KeyError('mult not found during inicialization. You should use cte=list[values]')
    if type(kwargs['mult'])!=list:
        raise TypeError('mult should be a non empty list of integers')
    num_of_zeros = 0
    for x in kwargs['mult']:
        if type(x)!=int:
            listt = kwargs['mult']
            raise TypeError(f'mult[{listt.index(x)}] should be a integer')
        if x==0:
            num_of_zeros+=1
    if num_of_zeros == len(kwargs['mult']):
        raise ValueError('mult can\'t be full of zeros')
    if kwargs['mult'][0]==0 and exclude_last_zero:
        raise ValueError('seed and mult[0] can\'t be both zeros')
    return True

def _validate_mult_array(kwargs:dict)->bool:
    pass

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
    """class for congruential multiplicative pseudorandom generators"""
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
    def sample(self,size:int=1)->list[float]|None:
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
    """class for congruential linear pseudorandom generators"""
    _sub_type = 'linear'
    def __new__(cls,**kwargs):
        _validate_mod(kwargs)
        _validate_mult(kwargs)
        if _validate_cte(kwargs):
            return super().__new__(cls)
        else:
            warn('since cte=0 you will get a multiplicative congruential generator instead of a linear congruential generator',category=package_type_warning)
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
    def sample(self,size:int=1)->list[float]|None:
        if size<0:
            return None
        if size==0:
            return []
        sample:list[float] = []
        while len(sample)<size:
            self._state = (self._mult*self._state + self._cte)%self._mod
            if self._state!=0:
                sample.append(self._state/self._mod)
        return sample

class quadratic_congrential_generator(_congruential_generator):
    """class for congruential quadratic pseudorandom generators"""
    _sub_type = 'quadratic'
    def __new__(cls,**kwargs):
        _validate_mod(kwargs)
        _validate_seed(kwargs,exclude_zero=True)
        return super().__new__(cls)
    def __init__(self,**kwargs):
        self._mod = kwargs['mod']
        self._state = kwargs['seed']%self._mod
    @property
    def rand(self)->float:
        self._state = self._state**2%self._mod
        return self._state/self._mod
    def sample(self,size:int=1)->list[float]|None:
        if size<0:
            return None
        if size==0:
            return []
        sample:list[float] = []
        while len(sample)<size and self._state!=0:
            self._state = self._state**2%self._mod
            if self._state!=0:
                sample.append(self._state/self._mod)
        return sample

class polynomial_confruential_generator(_congruential_generator):
    """class for congruential polynomial pseudorandom generators"""
    _sub_type = 'polynomial'
    def __new__(cls,**kwargs):
        _validate_mod(kwargs)
        _validate_seed(kwargs)
        _validate_poly_array(kwargs,exclude_last_zero=True if kwargs['seed']==0 else False)
        if len(kwargs['mult'])==1:
            raise ValueError('mult shuld be at least of size 2')
        if len(kwargs['mult'])==2:
            warn('since mult only have 2 integers you will get a linear congruential generator instead of a polynomial congruential generator',category=package_type_warning)
            return linear_congruential_generator(mod=kwargs['mod'],mult=kwargs['mult'][1],cte=kwargs['mult'][0],seed=kwargs['seed'])
        return super().__new__(cls)
    def __init__(self,**kwargs):
        self._mod = kwargs['mod']
        self._mult = [b%self._mod for b in kwargs['mult']]
        while self._mult[-1]==0:
            self._mult.pop()
        self._state = kwargs['seed']%self._mod
    @property
    def rand(self)->float:
        x = 0
        pow = 1
        while x==0:
            pow = 1
            for k in range(len(self._mult)):
                x = (x+pow*self._mult[k])%self._mod
                pow = pow*self._state%self._mod
            if x==0 and self._mult[0]==0:
                raise package_generator_error(f'generator raise a dead end.')
        self._state = x
        return self._state/self._mod        
    def sample(self,size:int=1)->list[float]:
        return [self.rand for _ in range(size)]

class multiple_congruential_generator(_congruential_generator):
    """"""
    _sub_type = ''
    def __new__(cls,**kwargs):
        pass
    def __init__(self,**kwargs):
        pass
    @property
    def rand(self):
        pass
    def sample(self,size:int=1)->list[float]:
        pass

class combined_congruential_generator(_congruential_generator):
    """"""
    _sub_type = ''
    def __new__(cls,**kwargs):
        pass
    def __init__(self,**kwargs):
        pass
    @property
    def rand(self):
        pass
    def sample(self,size:int=1)->list[float]:
        pass

class multcombi_congruential_generator(_congruential_generator):
    """"""
    _sub_type = ''
    def __new__(cls,**kwargs):
        pass
    def __init__(self,**kwargs):
        pass
    @property
    def rand(self):
        pass
    def sample(self,size:int=1)->list[float]:
        pass
