from typing import Any as _Any
from . import _package_warning
from . import _generator_Error
from . import _warn_int
from . import _validate_int_by_key
from . import _validate_list_ints
from . import _validate_list_ints_by_key
from . import random_sample as _random_sample

class _random_generator:
    """parent class for random generators
    
    Pseudorandom generators are organized in a two level hierarchy, specified by attributs _main_type and _sub_type
    """
    _main_type:str
    _sub_type:str
    
    def __str__(self)->str:
        return f'{self._main_type} {self._sub_type} pseudorandom generator. all attributes are private.'

    def __repr__(self)->str:
        return 'blocked'
    
    def rand(self):
        pass
    
    def sample(self,size:int=1)->_random_sample|None:
        """generation of size pseudo-random numbers

        """
        sample:_random_sample
        _warn_int(size,'size of sample must be a positive integer',threshold=1)
        sample = _random_sample()
        for _ in range(size):
            sample.append(self.rand())
        return sample

class _congruential_generator(_random_generator):
    """parent class for congruential random generators

    First level hierarchy for all congruential type generators.
    """
    _main_type = 'congruential'

class multiplicative_congruential_generator(_congruential_generator):
    """Multiplicative congruential  pseudorandom generator.

    Pseudorandom generator based on the multiplicative congruential method.
    Initialization must be made with keywords for all parameters.

    Keyword Args:
        mod (int): Module for residual reduction
        mult (int): Multiplier
        seed (int): initial value
    """
    
    _sub_type = 'multiplicative'

    def __new__(cls,**kwargs:dict[str,int]):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='mult',message='mult should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:dict[str,int])->None:
        """all attributes are private"""
        self._mod:int = kwargs['mod']
        self._mult:int = kwargs['mult']%self._mod
        self._state:int = kwargs['seed']%self._mod

    def rand(self)->float:
        """generation of one pseudo-random number"""
        self._state = self._mult*self._state % self._mod
        if self._state==0:
            raise _generator_Error()
        return self._state/self._mod

class linear_congruential_generator(_congruential_generator):
    """Linear congruential pseudorandom generator.
    
    Pseudorandom generator based on the linear congruential method.
    Initialization must be made with keywords for all parameters.

    Keyword Args:
        mod (int): Module for residual reduction
        mult (int): Multiplier
        seed (int): initial value
        cte (int): aditive constant
    """
    
    _sub_type = 'linear'
    
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='mult',message='mult should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='cte',message='')
        if kwargs['cte']!=0:
            return super().__new__(cls)
        else:
            warn('since cte=0 you will get a multiplicative congruential generator instead of a linear congruential generator',category=_package_warning)
            return multiplicative_congruential_generator(mod=kwargs['mod'],mult=kwargs['mult'],seed=kwargs['seed'])
    
    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mod:int = kwargs['mod']
        self._mult:int = kwargs['mult']%self._mod
        self._cte:int = kwargs['cte']%self._mod
        self._state:int = kwargs['seed']%self._mod
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        x:int = 0
        while x==0:
            x = (self._mult*self._state + self._cte)%self._mod
        return x/self._mod

class quadratic_congrential_generator(_congruential_generator):
    """Quadratic congruential pseudorandom generators.
    
    Pseudorandom generator based on the quadrátic congruential method.
    Initialization must be made with keywords for all parameters.
    
    Keyword Args:
        mod (int): Module for residual reduction
        seed (int): initial value
    """
    
    _sub_type = 'quadratic'
    
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mod:int = int(kwargs['mod'])
        self._state:int = int(kwargs['seed']%self._mod)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        x = self._state**2%self._mod
        if x==0:
            raise _generator_Error()
        self._state = x
        return x/self._mod

class polynomial_congruential_generator(_congruential_generator):
    """Polynomial congruential pseudorandom generator.
    
    Pseudorandom generator based on the method to generate pseudorandom numbers.
    Initialization must be made with keywords for all parameters.

    Keyword Args:
        mod (int): Module for residual reduction
        mults (int): Multipliers
        seeds (int): initial values, the flast element on the list
    """
    
    _sub_type = 'polynomial'
    
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='seed',message='seed should be an integer')
        _validate_list_ints_by_key(kwargs,key='coefs',exclude_all_zeros=True)
        if len(kwargs['coefs'])==1:
            raise ValueError('coefs shuld be at least of size 2')
        if len(kwargs['coefs'])==2:
            warn('coefs only have 2 integers, you will get a linear congruential generator instead of a polynomial congruential generator',category=_package_warning)
            return linear_congruential_generator(mod=kwargs['mod'],mult=kwargs['coefs'][1],cte=kwargs['coefs'][0],seed=kwargs['seed'])
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mod:int = int(kwargs['mod'])
        self._mult:list[int] = [int(b%self._mod) for b in kwargs['mult']]
        while self._mult[-1]==0:
            self._mult.pop()
        self._state:int = int(kwargs['seed']%self._mod)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        x:int = 0
        pow:int
        while x==0:
            pow = 1
            for k in range(len(self._mult)):
                x = (x+pow*self._mult[k])%self._mod
                pow = pow*self._state%self._mod
            if x==0 and self._mult[0]==0:
                raise _generator_Error()
        self._state = x
        return x/self._mod        

class multiple_congruential_generator(_congruential_generator):
    """Multiple congruential pseudorandom generator

    Pseudorandom generator based on the multiple multiplicative congruential generator. 
    
    Keyword Args:
        mod (int): Module for residual reduction
        seed (int): initial values, the last element on the list
    """
    
    _sub_type = 'multiple'

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here
        
        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_list_by_key(kwargs,key='mults',exclude_all_zeros=True)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=True)
        if len(kwargs['seeds'])!=len(kwargs['mults']):
            raise ValueError('seeds and mults must be of the same size')
        return super().__new__(cls)

    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mod:int = int(kwargs['mod'])
        self._state:list[int] = [int(x) for x in kwargs['seeds']]
        self._mults:list[int] = [int(x) for x in kwargs['mults']]

    def rand(self)->float:
        """generation of one pseudo-random number"""
        x:int = 0
        while x==0:
            for i in range(len(self._state)):
                x = (x+self._state[i]*self._mults[i])%self._mod
            self._state.pop(0)
            self._state.insert(len(self._state),x)
            try:
                _validate_list_ints(self._state,message='',exceptions=0)
            except:
                raise _generator_Error()
        return x/self._mod

class combined_congruential_generator(_congruential_generator):
    """Combined congruential pseudorandom generator.
    
    Pseudorandom generator based on the multiple multiplicative congruential generator. 
    
    Keyword Args:
        mod (int): Module for residual reduction
        seed (int): initial values, the last element on the list
    """
    
    _sub_type = 'combined'

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_list_by_key(kwargs,key='mods',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='mults',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        if len(kwargs['mods'])!=2:
            raise ValueError('mods must be a list of integers both at leats two')
        _validate_list_ints(kwargs['mods'],message='mods must be a list of integers both at leats two',threshold=2)
        if len(kwargs['mults'])!=2:
            raise ValueError('mults must be a list of two non zero integers')
        _validate_list_ints(kwargs['mults'],message='mults must be a list of two non zero integers',exceptions=0)
        if len(kwargs['seeds'])!=2:
            raise ValueError('seeds must be a list of two non zero integers')
        _validate_list_ints(kwargs['seeds'],message='seeds must be a list of two non zero integers',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mods:list[int] = [int(m) for m in kwargs['mods']]
        self._state:list[int] = [int(m) for m in kwargs['seeds']]
        self._mults:list[int] = [int(m) for m in kwargs['mults']]

    def rand(self:_Any):
        """generation of one pseudo-random number"""
        x:int = self._mults[0]*self._state[0]%self._mods[0]
        y:int = self._mults[1]*self._state[1]%self._mods[1]
        z:int = (x-y)%self._mods[0]
        self._state = [x,y]
        return z/self._mods[0]

class multcombi_congruential_generator(_congruential_generator):
    """Multiple combined congruential pseudorandom generator
    
    Pseudorandom generator based on the multiple combined congruential method.
    Initialization must be made with keywords for all parameters.

    Keyword Args:
        mods (list[int]): array of 2 positive integers, both to be used as modules
        mults (list[int]): array of 2m integers used as multipliers, the sequence is splited in two array of the same length
        seeds (list[int]): array of 2m integers used as seeds, the sequence is splited in two array of the same length
    """

    _sub_type = 'multiple combined'

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_list_by_key(kwargs,key='mods',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        if len(kwargs['mods'])!=2:
            raise ValueError('mods must be a list of integers both at leats two')
        _validate_list_ints(kwargs['mods'],message='mods must be a list of integers both at leats two',threshold=2)
        if len(kwargs['mults'])%2!=0:
            raise ValueError('mults must be a list of odd lenght')
        k = len(kwargs['mults'])//2
        _validate_list_ints(kwargs['mults'][0:k],message='first half of mults are all zero',exceptions=0)
        _validate_list_ints(kwargs['mults'][k+1:2*k],message='second half of mults are all zero',exceptions=0)
        if len(kwargs['seeds'])%2!=0:
            raise ValueError('seeds must be a list of odd lenght')
        if  len(kwargs['seeds'])//2!=k:
            raise ValueError('seeds and mods must be of the same lenght')
        _validate_list_ints(kwargs['seeds'][0:k],message='first half of seeds are all zero',exceptions=0)
        _validate_list_ints(kwargs['seeds'][k+1:2*k],message='second half of seeds are all zero',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:dict)->None:
        """all attributes are private"""
        self._mod_1:int = kwargs['mods'][0]
        self._mod_2:int = kwargs['mods'][1]
        self._mults_1:list[int] = kwargs['mults'][0:len(kwargs['mults'])//2]
        self._mults_2:list[int] = kwargs['mults'][len(kwargs['mults'])//2:len(kwargs['mults'])]
        self._state_1:list[int] = kwargs['seeds'][0:len(kwargs['mults'])//2]
        self._state_2:list[int] = kwargs['seeds'][len(kwargs['mults'])//2:len(kwargs['mults'])]
    
    def rand(self)->float:
        """generation of one pseudorandom number"""
        x = 0
        y = 0
        for i in range(len(self._state_1)):
            x = (x+self._state_1[i]*self._mults_1[i])%self._mod_1
            y = (y+self._state_2[i]*self._mults_2[i])%self._mod_2
        z = (x-y)%self._mod_1
        self._state_1.pop(0)
        self._state_2.pop(0)
        self._state_1.insert(len(self._state_1),x)
        self._state_2.insert(len(self._state_2),y)
        try:
            _validate_list_ints(self._state_1,message='',exceptions=0)
        except:
            try:
                _validate_list_ints(self._state_2,message='',exceptions=0)
            except:
                raise _generator_Error()
        return z/self._mod_1

class _linearfeedback_generator(_random_generator):
    """parent class for linear feedback random generators

    First level hierarchy for all linear feedback type generators.
    """

    _main_type = 'linear feedback'

def _int2bools(d:int)->list[bool]:
    """to convert to base 2 a non negative integer
    
    This function takes a positive integer and returns a list that contains the representation on base 2 of the given integer.
    The first element of the list corresponds to the least significative value of the integer.
    """
    if d<0:
        return []
    if d<2:
        return [d%2==1]
    sig:list[bool] = _int2bools(d//2)
    sig.insert(0,d%2==1)
    return sig

def _bools2int(l:list[bool])->int:
    """to convert a list to a positive integer
    
    This function takes a list of bools values to a positive integer.
    The constructed integer has _int2bools representation equals to the given list.
    """
    if len(l)<2:
        return 1 if l[0]==True else 0
    return _bools2int([l[0]])+2*_bools2int(l[1:len(l)])

def _ensure_size_bools(l:list[bool],size:int)->list[bool]:
    """ensure l has exactly length equals to size"""
    if len(l)>=size:
        return l[0:size]
    while len(l)<size:
        l.append(False)
    return l

def _make_submatrix(d:int)->list[list[bool]]:
    """auxiliar constructor"""
    return [[i==(j-1) for j in range(d)] for i in range(d-1)]

def _append_and_return(l:list[_Any],e:_Any)->list[_Any]:
    """appends a valur to l and return l itself"""
    l.append(e)
    return l

def _multiply_bools_by_matrix(l:list[bool],A:list[list[bool]])->list[bool]:
    """multiply a matrix and an array of bools according to operations on F2"""
    n:int = len(l)
    res:list[bool] = []
    for i in range(n):
        row_res = False
        for j in range(n):
            row_res = row_res ^ (A[i][j] and l[j])
        res.append(row_res)
    return res

def _taps2bools(s:str)->list[bool]:
    """auxiliar constructor"""
    return [False if bit=='0' else True for bit in s]

class linear_feedback_shift_register_4(_linearfeedback_generator):
    """linear fedbacl shift register for word size 4"""
    
    _taps = '1100'
    _word_size = 4
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here

        """
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private
        
        """
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo-random number
        
        """
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

class linear_feedback_shift_register_8(_linearfeedback_generator):
    """linear fedbacl shift register for word size 8"""
    
    _taps = '10111000'
    _word_size = 8
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

class linear_feedback_shift_register_12(_linearfeedback_generator):
    """linear fedbacl shift register for word size 12"""
    
    _taps = '111000001000'
    _word_size = 12
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

class linear_feedback_shift_register_16(_linearfeedback_generator):
    """linear fedback shift register for word size 16"""
    
    _taps = '1101000000001000'
    _word_size = 16
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

class linear_feedback_shift_register_20(_linearfeedback_generator):
    """linear fedbacl shift register for word size 20"""
    
    _taps = '10010000000000000000'
    _word_size = 16
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo-random number"""
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

class linear_feedback_shift_register_24(_linearfeedback_generator):
    """linear fedbacl shift register for word size 24"""
    
    _taps = '111000010000000000000000'
    _word_size = 24
    _matrix = _append_and_return(_make_submatrix(_word_size),_taps2bools(_taps))
    _divisor = 2**_word_size

    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'seed','',threshold=1)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._state:list[bool] = _ensure_size_bools(_int2bools(kwargs['seed']),self._word_size)
    
    def rand(self)->float:
        """generation of one pseudo random number"""
        self._state = _multiply_bools_by_matrix(self._state,self._matrix)
        n:int = _bools2int(self._state)
        return n/self._divisor

__all__ = [
    'multiplicative_congruential_generator',
    'linear_congruential_generator',
    'quadratic_congrential_generator',
    'polynomial_congruential_generator',
    'multiple_congruential_generator',
    'combined_congruential_generator',
    'multcombi_congruential_generator',
    'linear_feedback_shift_register_4',
    'linear_feedback_shift_register_8',
    'linear_feedback_shift_register_12',
    'linear_feedback_shift_register_16',
    'linear_feedback_shift_register_20',
    'linear_feedback_shift_register_24']