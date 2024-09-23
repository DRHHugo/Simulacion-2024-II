from __init__ import *

class _random_generator:
    """parent class for random generators
    

    Pseudorandom generators are organized in a two level hierarchy, specified by attributs _main_type and _sub_type
    
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
        """generation of size pseudo-random numbers

        """

        _validate_int(size,'size must be a positive integer, no random numbers generated',threshold=1)
        return [self.rand() for _ in range(size)]

class _congruential_generator(_random_generator):
    """parent class for congruential random generators

    First level hierarchy for all congruential type generators.
    
    """

    _main_type = 'congruential'

class multiplicative_congruential_generator(_congruential_generator):
    """congruential multiplicative pseudorandom generators

    Pseudorandom generator based on the multiplicative congruential method

    """

    _sub_type = 'multiplicative'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here

        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='mult',message='mult should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private
        
        """

        self._mod:int = int(kwargs['mod'])
        self._mult:int = int(kwargs['mult']%self._mod)
        self._state:int = int(kwargs['seed']%self._mod)

    def rand(self)->float:
        """generation of one pseudo-random number

        """

        self._state = self._mult*self._state % self._mod
        if self._state==0:
            raise GeneratorError()
        return self._state/self._mod

class linear_congruential_generator(_congruential_generator):
    """congruential linear pseudorandom generators
    
    """

    _sub_type = 'linear'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here
        
        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='mult',message='mult should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        _validate_int_by_key(kwargs,key='cte',message='')
        if kwargs['cte']!=0:
            return super().__new__(cls)
        else:
            warn('since cte=0 you will get a multiplicative congruential generator instead of a linear congruential generator',category=package_warning)
            return multiplicative_congruential_generator(mod=kwargs['mod'],mult=kwargs['mult'],seed=kwargs['seed'])

    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private
        
        """

        self._mod:int = kwargs['mod']
        self._mult:int = kwargs['mult']%self._mod
        self._cte:int = kwargs['cte']%self._mod
        self._state:int = kwargs['seed']%self._mod

    def rand(self)->float:
        """generation of one pseudo-random number
        
        """

        x:int = 0
        while x==0:
            x = (self._mult*self._state + self._cte)%self._mod
        return x/self._mod

class quadratic_congrential_generator(_congruential_generator):
    """congruential quadratic pseudorandom generators
    
    """

    _sub_type = 'quadratic'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here
        
        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='seed',message='seed should be non zero integer',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private

        """

        self._mod:int = int(kwargs['mod'])
        self._state:int = int(kwargs['seed']%self._mod)

    def rand(self)->float:
        """generation of one pseudo-random number

        """

        x = self._state**2%self._mod
        if x==0:
            raise GeneratorError()
        self._state = x
        return x/self._mod

class polynomial_congruential_generator(_congruential_generator):
    """congruential polynomial pseudorandom generator
    
    """

    _sub_type = 'polynomial'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here
        
        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_int_by_key(kwargs,key='seed',message='seed should be an integer')
        _validate_list_by_key(kwargs,key='coefs',exclude_all_zeros=True)
        if len(kwargs['coefs'])==1:
            raise ValueError('coefs shuld be at least of size 2')
        if len(kwargs['coefs'])==2:
            warn('coefs only have 2 integers, you will get a linear congruential generator instead of a polynomial congruential generator',category=package_warning)
            return linear_congruential_generator(mod=kwargs['mod'],mult=kwargs['coefs'][1],cte=kwargs['coefs'][0],seed=kwargs['seed'])
        return super().__new__(cls)
    
    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private

        """

        self._mod:int = int(kwargs['mod'])
        self._mult:list[int] = [int(b%self._mod) for b in kwargs['mult']]
        while self._mult[-1]==0:
            self._mult.pop()
        self._state:int = int(kwargs['seed']%self._mod)

    def rand(self)->float:
        """generation of one pseudo-random number

        """

        x:int = 0
        pow:int
        while x==0:
            pow = 1
            for k in range(len(self._mult)):
                x = (x+pow*self._mult[k])%self._mod
                pow = pow*self._state%self._mod
            if x==0 and self._mult[0]==0:
                raise GeneratorError()
        self._state = x
        return x/self._mod        

class multiple_congruential_generator(_congruential_generator):
    """multiple congruential pseudorandom generator
    
    """

    _sub_type = 'multiple'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here
        
        """

        _validate_int_by_key(kwargs,key='mod',message='mod should be an integer bigger than 1',threshold=2)
        _validate_list_by_key(kwargs,key='mults',exclude_all_zeros=True)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=True)
        if len(kwargs['seeds'])!=len(kwargs['mults']):
            raise ValueError('seeds and mults must be of the same size')
        return super().__new__(cls)

    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private

        """

        self._mod:int = int(kwargs['mod'])
        self._state:list[int] = [int(x) for x in kwargs['seeds']]
        self._mults:list[int] = [int(x) for x in kwargs['mults']]

    def rand(self)->float:
        """generation of one pseudo-random number
        
        """

        x:int = 0
        while x==0:
            for i in range(len(self._state)):
                x = (x+self._state[i]*self._mults[i])%self._mod
            self._state.pop(0)
            self._state.insert(len(self._state),x)
            try:
                _validate_list_by_key({'state':self._state},key='state',exclude_all_zeros=True)
            except:
                raise GeneratorError()
        return x/self._mod

class combined_congruential_generator(_congruential_generator):
    """combined congruential pseudorandom generator
    
    """

    _sub_type = 'combined'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here

        """
        _validate_list_by_key(kwargs,key='mods',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='mults',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        if len(kwargs['mods'])!=2:
            raise ValueError('mods must be a list of integers both at leats two')
        _validate_list(kwargs['mods'],message='mods must be a list of integers both at leats two',threshold=2)
        if len(kwargs['mults'])!=2:
            raise ValueError('mults must be a list of two non zero integers')
        _validate_list(kwargs['mults'],message='mults must be a list of two non zero integers',exceptions=0)
        if len(kwargs['seeds'])!=2:
            raise ValueError('seeds must be a list of two non zero integers')
        _validate_list(kwargs['seeds'],message='seeds must be a list of two non zero integers',exceptions=0)
        return super().__new__(cls)

    def __init__(self,**kwargs:Any)->None:
        """All Attributes are private
        
        """

        self._mods:list[int] = [int(m) for m in kwargs['mods']]
        self._state:list[int] = [int(m) for m in kwargs['seeds']]
        self._mults:list[int] = [int(m) for m in kwargs['mults']]

    def rand(self:Any):
        """generation of one pseudo-random number

        """

        x:int = self._mults[0]*self._state[0]%self._mods[0]
        y:int = self._mults[1]*self._state[1]%self._mods[1]
        z:int = (x-y)%self._mods[0]
        self._state = [x,y]
        return z/self._mods[0]

class multcombi_congruential_generator(_congruential_generator):
    """multiple combined congruential pseudorandom generator
    
    """

    _sub_type = 'multiple combined'

    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here

        """
        _validate_list_by_key(kwargs,key='mods',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        _validate_list_by_key(kwargs,key='seeds',exclude_all_zeros=False)
        if len(kwargs['mods'])!=2:
            raise ValueError('mods must be a list of integers both at leats two')
        _validate_list(kwargs['mods'],message='mods must be a list of integers both at leats two',threshold=2)
        if len(kwargs['mults'])%2!=0:
            raise ValueError('mults must be a list of odd size')
        k = len(kwargs['mults'])//2
        if not _validate_list(kwargs['mults'][0:k],message='first half of mults are all zero',exceptions)
        if len(kwargs['mults'])%2!=0:
            raise ValueError('mults must be a list of odd size')
        


    def __init__(self,**kwargs:Any)->None:
        pass

    def rand(self)->float:
        pass

__all__=[
    'multiplicative_congruential_generator',
    'linear_congruential_generator',
    'quadratic_congrential_generator',
    'multiple_congruential_generator',
    'combined_congruential_generator']