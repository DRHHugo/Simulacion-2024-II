# from os import getcwd,chdir
# direc_list = getcwd().split('\\')
# direc_list.pop()
# chdir('\\'.join(direc_list))
# print(getcwd())

from __init__ import *

def _validate_mod(kwargs:dict)->bool:
    """
    validation of module

    Args:
        kwargs : kwargs passed from another function
    
    Returns:
        True if kwargs['mod'] is an integer bigger that 1
        False otherwise
    """
    if not 'mod' in kwargs.keys():
        raise KeyError('mod not found during inicialization. You should use mod=value.')
        return False
    return _validate_int(kwargs['mod'],'mod should be an integer bigger than 1',threshold=2)

def _validate_mult(kwargs:dict)->bool:
    """
    validation of multiplier
    
    Args:
        kwargs : kwargs passed from another function
    
    Returns:
        True if kwargs['mod'] is a non-zero integer
        False otherwise
    """
    if not 'mult' in kwargs.keys():
        raise KeyError('mult not found during inicialization. You should use mult=value.')
    return _validate_int(kwargs['mult'],'mult should be non zero integer',None,0)

def _validate_seed(kwargs:dict,exceptions:None|int|list[int]=None)->bool:
    """
    validation of seed
    
    Args:
        kwargs : kwargs passed from another function
        exceptions: integer or list of integers not allowed for seed
    
    Returns:
        True if kwargs['seed'] is a valid integer
        False otherwise
    """
    if not 'seed' in kwargs.keys():
        raise KeyError('seed not found during inicialization. You should use seed=value.')
    return _validate_int(kwargs['seed'],'seed is set to a non valid value',None,exceptions)

def _validate_cte(kwargs:dict)->bool:
    """
    validation of constant

    Args:
        kwargs : kwargs passed from another function
    
    Returns:
        True if kwargs['cte'] is a non zero integer
        False otherwise
    """
    if not 'cte' in kwargs.keys():
        raise KeyError('cte not found during inicialization. You should use cte=value.')
    return _validate_int(kwargs['cte'],'cte should be an integer')

def _validate_list(kwargs:dict,exclude_all_zeros:bool=True)->bool:
    """
    validate a list of integers

    Args:
        kwargs : kwargs passed from another function
        exclude_all_zeros : True if kwargs['mult'] can\'t be a list of zeros only
    
    Returns:
        True if kwargs['mult'] is a valid list of integers
        False otherwise
    """
    if not 'mult' in kwargs.keys():
        raise KeyError('mult not found during inicialization. You should use mult=list[values]')
    if type(kwargs['mult'])!=list:
        raise TypeError('mult should be a non empty list of integers')
    for x in kwargs['mult']:
        _validate_int(x,'mult should be a non empty list of integers')
    if exclude_all_zeros:
        num_of_zeros = 0
        for x in kwargs['mult']:
            if x==0:
                num_of_zeros+=1
        if num_of_zeros == len(kwargs['mult']):
            raise ValueError('mult can\'t be a list of zeros')
    return True

class _random_generator:
    """
    parent class for random generators

    """
    _main_type:str
    _sub_type:str
    def __str__(self):
        return f'{self._main_type} {self._sub_type} pseudorandom generator. All attributes are private.'
    def __repr__(self):
        return self.__str__()

class _congruential_generator(_random_generator):
    """
    parent class for congruential random generators

    subclasses must contain the global Attribute: _sub_type
    """
    _main_type = 'congruential'

class multiplicative_congruential_generator(_congruential_generator):
    """
    class for congruential multiplicative pseudorandom generators
    """
    _sub_type = 'multiplicative'
    def __new__(cls,**kwargs):
        """
        validation of parameters occurs here
        """
        _validate_mod(kwargs)
        _validate_mult(kwargs)
        _validate_seed(kwargs,exceptions=0)
        return super().__new__(cls)
    def __init__(self,**kwargs):
        """
        All Attributes are private
        """
        self._mod:int = int(kwargs['mod'])
        self._mult:int = int(kwargs['mult']%self._mod)
        self._state:int = int(kwargs['seed']%self._mod)
    def rand(self)->float:
        """
        generation of one pseudo-random number
        """
        self._state = self._mult*self._state % self._mod
        return self._state/self._mod
    def sample(self,size:int=1)->list[float]|None:
        """
        generation of size pseudo-random numbers
        """
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
    """
    class for congruential linear pseudorandom generators
    """
    _sub_type = 'linear'
    def __new__(cls,**kwargs):
        """
        validation of parameters occurs here
        """
        _validate_mod(kwargs)
        _validate_mult(kwargs)
        if _validate_cte(kwargs):
            return super().__new__(cls)
        else:
            warn('since cte=0 you will get a multiplicative congruential generator instead of a linear congruential generator',category=package_type_warning)
            return multiplicative_congruential_generator(mod=kwargs['mod'],mult=kwargs['mult'],seed=kwargs['seed'])
    def __init__(self,**kwargs):
        """
        All Attributes are private
        """
        self._mod:int = kwargs['mod']
        self._mult:int = kwargs['mult']%self._mod
        self._cte:int = kwargs['cte']%self._mod
        self._state:int = kwargs['seed']%self._mod
    def rand(self)->float:
        """
        generation of one pseudo-random number
        """
        self._state = (self._mult*self._state + self._cte)%self._mod
        return self._state/self._mod
    def sample(self,size:int=1)->list[float]|None:
        """
        generation of size pseudo-random numbers
        """
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
    """
    class for congruential quadratic pseudorandom generators
    """
    _sub_type = 'quadratic'
    def __new__(cls,**kwargs):
        """
        validation of parameters occurs here
        """
        _validate_mod(kwargs)
        _validate_seed(kwargs,exceptions=0)
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
        _validate_list(kwargs,exclude_all_zeros=True)
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
    def rand(self)->float:
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

__all__=[
    'multiplicative_congruential_generator',
    'linear_congruential_generator',
    'quadratic_congrential_generator',
    'multiple_congruential_generator']