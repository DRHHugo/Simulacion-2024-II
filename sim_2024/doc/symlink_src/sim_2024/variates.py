from typing import Any,Callable
from sys import modules
from math import log
from math import exp
from math import gamma
from math import pi
from . import _validate_float_by_key
from . import _validate_int_by_key
from . import _validate_int
from . import _validate_list
from .utilities import mass_function
from .utilities import density_function

try:
    rand = modules['sim_2024'].rand
except KeyError:
    raise ImportError('Module sim_2024 not loaded. Load sim_2024 and try again')

class _random_variate:
    """parent class for random variates
    
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
        """generation of size pseudo-random sample of variate"""
        return [self.rand() for _ in range(size)]

class _discrete_variate(_random_variate):
    """parent class for discrete random variates"""
    _main_type = 'discrete'

class _continuos_variate(_random_variate):
    """parent class for continuos random variates
    
    """
    _main_type = 'continuos'

class Bernoulli(_discrete_variate):
    """Representation of a random variate of Bernoulli type.

    Keyword Args:
        p (float): Sucess probability
    """
    
    _sub_type = 'Bernoulli'
    
    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    
    def __init__(self,**kwargs:Any):
        """all attributes are private"""
        self._p:float = kwargs['p']
        self.mass_function:mass_function = mass_function(function=lambda x:(self._p if x==1 else 1-self._p),sup=[0,1])
    
    def rand(self)->float:
        global rand
        u = rand.rand()
        if u<self._p:
            return 1.0
        else:
            return 0.0

class Binomial(_discrete_variate):
    """representation of a random variate of binonimal type
    
    Keyword Args:
        p (float): Sucess probability
        n (int): Number of trials
    """
    _sub_type = 'Binomial'
    def __new__(cls,**kwargs:Any):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'n','number of trials must be a positive integer',threshold=1)
        _validate_float_by_key(kwargs,'p','probability p must be a float between 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:Any):
        """all attributes are private"""
        self._p:float = kwargs['p']
        self._n:int = kwargs['n']
    def rand(self)->float:
        global rand
        x:float = 0.0
        for _ in range(self._n):
            u = rand.rand()
            if u<self._p:
                x+=1.0
        return x   

class Geometric(_discrete_variate):
    """Representation of a random variate of Bernoulli type
    
    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Geometric'
    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs)->None:
        """all attributes are private"""
        self._p:float = kwargs['p']
    def rand(self)->float:
        #global rand
        u = rand()
        x =  0.0
        while u>self._p:
            u = rand()
            x+= 1
        return x

class NegativeBinomial(_discrete_variate):
    """representation of a random variate of Bernoulli type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Negative binomial'
    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs)->None:
        """all attributes are private"""
        self._p:float = kwargs['p']
        self._s:float = kwargs['s']
    def rand(self)->float:
        #global rand
        s = 1.0 if rand()<self._p else 0
        x = 0.0 if s==1 else 1
        while s<self._s:
            s+= 1.0 if rand()<self._p else 0
            x+= 0.0 if s==1 else 1
        return x

class DiscreteUniform(_discrete_variate):
    """Discrete uniform distribution.

    Keyword Args:
        size(int): if provided, the class will represenr Discrete distribution on inetegers 1,2,...,size.
        sup(list[float]): if provided, the class will represent Discrete distribution on the set {members of list}.
    """
    _sub_type = 'uniform'
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        size:bool = True if 'size' in kwargs else False
        sup:bool = True if 'sup' in kwargs else False
        if not (size^sup):
            raise KeyError('initialization must include one and just one:size or sup')
        if 'size' in kwargs:
            _validate_int(kwargs['size'],'size must be an integer greater that 1',2)
        if 'sup' in kwargs:
            _validate_list(kwargs['sup'],'sup must be a list of int or float numbers')
            if len(kwargs['sup'])<2:
                raise ValueError('sup must be a list of size at leats 2')
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._type:str = 'size' if ('size' in kwargs) else 'sup'
        self._size:int
        self._sup:list[int|float]|None
        if self._type=='size':
            self._size = kwargs['size']
            self._sup = None
        else:
            self._sup = kwargs['sup']
            self._size = len(self._sup)
    
    def rand(self)->float:
        """generation of one random number"""
        u:float = rand()
        index:float = 1.0
        while u>index/self._size:
            index+=1.0
        if self._sup==None:
            return index
        else:
            return self._sup[int(index)-1]

class Poisson(_discrete_variate):
    """Poisson distribution.

    Keyword Args:
        rate (float): the rate associated with the underlaing exponential distribitud arrival process.
    """
    _sub_type = 'Poisson'
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'rate',threshold=0.0,exceptions=0.0)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict) -> None:
        """all attributes are private"""
        self._rate:float = kwargs['rate']
        self._expvariate:Exponential = Exponential(rate=kwargs['rate'])
    
    def rand(self)->float:
        """generation of one random number"""
        x:float = 0.0
        t:float = self._expvariate.rand()
        while t<=1:
            x+=1.0
            t+=self._expvariate.rand()
        return x

class ContinuousUniform(_continuos_variate):
    """Continuous uniform distribution.

    Keyword Args:
        sup(tuple): support of distribution.
    """

    #def __new__(cls,**kwargs:dict):
    #    """validation of parameters occurs here"""
    def __init__(self,**kwargs:dict)->None:
        self._sup = kwargs['sup']
    def rand(self)->float:
        u:float = rand.rand()
        return self._sup[0]+u*(self._sup[1]-self._sup[0])

class Exponential(_continuos_variate):
    """Exponential distribution.

    Keyword Args:
        rate(float): rate parameter 
    """
    
    def __new__(cls,**kwargs:dict):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'rate','rate must be a positive number',threshold=0.0,exceptions=0.0)
        return super().__new__(cls)

    def __init__(self,**kwargs:dict)->None:
        self._rate:float = kwargs['rate']
        #self._density:density_function = density_function(lambda x: self._rate*exp(-self._rate*x),min=0,max=None)

    def rand(self)->float:
        """generation of one random number"""
        u = rand.rand()
        return -log(u)/self._rate

class _NormalStd(_continuos_variate):
    def __init__(self):
        pass
    def _rand(self):
        s=2
        while s>1:
            u = rand()
            v = rand()
            x = 2*u -1
            y = 2*v -1
            s = x**2+y**2
        return (x*((-2*log(s)/s)**0.5),y*((-2*log(s)/s)**0.5))
    def rand(self):
        _rand()[0]
    def sample(self,size:int=1)->list[float]|None:
        pairs = [self._rand() for _ in range(size//2+size%2)]
        _sample = []
        for k in range(size//2):
            _sample.append(pairs[k][0])
            _sample.append(pairs[k][1])
        if len(_sample)<size:
            _sample.append(pairs[-1][0])
        return _sample

class Normal(_continuos_variate):
    """Normal distribution

    Keyword Args:
        mean (float): mean parameter
        var (float): variance parameter
        stdev (float): standar deviation parameter
    """
    
    _sub_type = 'Normal'
    
    def __init__(self,**kwargs)->None:
        self._mean:float
        self._var:float
        self._stdev:float
        self._stdvariate:_NormalStd
        self._mean = kwargs['mean']
        if 'var' in kwargs:
            self._var = kwargs['var']
            self._stdev = self._var**0.5
        if 'stdev'in kwargs:
            self._stdev = kwargs['stdev']
            self._var = self._stdev**2
        self._stdvariate = _NormalStd()
    
    def rand(self):
        return self._mean+self._stdev*self._stdvariate.rand()
    
    def sample(self,size:int=1)->list[float]|None:
        _sample = self._stdvariate.sample(size)
        return [self._mean+self._stdev*z for z in _sample]

class BoundedNormal(_continuos_variate):
    """Normal bounded distribution

    """
    
    _sub_type = 'bounded normal'
    
    def __init__(self)->None:
        self._stdvariate:_NormalStd
        self._stdvariate = _NormalStd()
    
    def rand(self)->float:
        x:float
        x = self._stdvariate.rand()
        while abs(x)>1:
            x = self._stdvariate.rand()
        return x

class RectifiedNormal(_continuos_variate):
    """Rectified normal distribution

    """
    
    _sub_type = 'rectified normal'
    
    def __init__(self)->None:
        self._stdvariate:_NormalStd
        self._stdvariate = _NormalStd()
    
    def rand(self)->float:
        x:float
        x = self._stdvariate.rand()
        if x<0.0:
            return 0.0
        else:
            return x

class Chisq(_continuos_variate):
    def __init__(self,**kwargs)->None:
        self._deg:int
        self._stdvarite:_NormalStd
        self._deg = kwargs['deg']
        self._stdvarite = _NormalStd()
    def rand(self)->float:
        sample = self._stdvarite.sample(self._deg)
        samplesq = [s**2 for s in sample]
        return sum(samplesq)

class Student(_continuos_variate):
    def __init__(self,**kwargs)->None:
        self._deg:int
        self._stdvarite:_NormalStd
        self._deg = kwargs['deg']
        self._stdvariate = _NormalStd()
    def rand(self)->float:
        sample = self._stdvariate.sample(self._deg+1)
        z = sample.pop(0)
        samplesq = [s**2 for s in sample]
        return z/sum(samplesq)

class _mayorant_Gamma_density:
    def __init__(self,shape:float)->None:
        self.shape:float
        self.a:float
        self.b:float
        self.shape = shape
        self.a = abs(2*shape-1)**0.5
        self.b = 4*(shape**shape)*exp(shape)/(self.a*gamma(shape))
    
    def __call__(self,x:float)->float:
        if self.shape<1:
            if 1<x:
                return exp(-x)/self.shape
            else:
                return x**(self.shape-1)/self.shape
        else:
            return (self.b*x**(self.a-1))/((self.shape**self.a+x**self.a)**2)

class Gamma(_continuos_variate):
    """Gamma distribution
    
    """
    
    _sub_type = 'gamma distribution'
    
    def __init__(self,**kwargs)->None:
        self._shape:float
        self._rate:float
        self._scale:float
        self._mayorant:_mayorant_Gamma_density
        self._shape = kwargs['shape']
        self._rate = kwargs['rate']
        self._scale = 1/self._rate
        self._mayorant = _mayorant_Gamma_density(self._shape)
    
    def rand(self)->float:
        x:float
        u:float
        y:float
        if self._shape == 1:
            return Exponential(rate=1.0).rand()
        u=rand()
        if self._shape<1:
            y = ((exp(0)+self._shape)*u/exp(0)) if u<exp(0)/(exp(0)+self._shape) else -log((exp(0)+self._shape)*(1-u)/(exp(0)*self._shape))
        else:
            y = (u*self._shape**self._mayorant.a/(1-u))**(1/self._mayorant.a)
        u=rand()
        while u*self._mayorant(y)>y**(self._shape-1)*exp(-y)/gamma(self._shape):
            u=rand()
            if self._shape<1:
                y = ((exp(0)+self._shape)*u/exp(0)) if u<exp(0)/(exp(0)+self._shape) else -log((exp(0)+self._shape)*(1-u)/(exp(0)*self._shape))
            else:
                y = (u*self._shape**self._mayorant.a/(1-u))**(1/self._mayorant.a)
            u=rand()
        return self._rate*y        

class Beta(_continuos_variate):
    """Beta distribution
    
    """
    
    _sub_type = 'beta distribution'

    def __init__(self,**kwargs:dict)->None:
        self._alpha:float
        self._beta:float
        self._gamma_1:Gamma
        self._gamma_2:Gamma
        self._alpha = kwargs['shape'][0]
        self._beta = kwargs['shape'][1]
        self._gamma_1 = Gamma(shape=self._alpha,rate=1)
        self._gamma_2 = Gamma(shape=self._beta,rate=1)
    def rand(self)->float:
        x:float
        y:float
        x = self._gamma_1.rand()
        y = self._gamma_2.rand()
        return x/(x+y)

class Tringular(_continuos_variate):
    """Triangular distribution
    """
    def __init__(self,**kwargs)->None:
        self._a:float
        self._b:float
        self._c:float
        self._a = kwargs['a']
        self._b = kwargs['b']
        self._c = kwargs['c']
    def rand(self)->float:
        u:float
        u = rand()
        if u<(self._b-self._a)/(self._c-self._a):
            return self._a + (u*(self._c-self._a)*(self._b-self._a))**0.5
        else:
            return self._b - ((1-u)*(self._c-self._a)*(self._b-self._a))**0.5

class ExampleDis(_continuos_variate):
    def rand(self)->float:
        y:float
        u:float
        u = rand()
        y = 2*u-1
        u = rand()
        while 4*u>3/(y**2+y+1):
            u = rand()
            y = 2*u-1
            u = rand()
        return y

__all__ = [
    'Bernoulli',
    'Binomial',
    'Geometric',
    'NegativeBinomial',
    'DiscreteUniform',
    'Poisson',
    'Exponential',
    'Normal',
    'Chisq',
    'Student',
    'BoundedNormal',
    'RectifiedNormal',
    'Gamma',
    'ExampleDis'
]