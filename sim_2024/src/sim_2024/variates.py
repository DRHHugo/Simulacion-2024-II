from typing import Any as _Any
from sys import modules as _modules
from math import log as _log
from math import exp as _exp
from math import gamma as _gamma
from . import _validate_float_by_key
from . import _validate_int_by_key
from . import _validate_int
from . import _validate_list
from . import _warn_int
from . import random_sample as _random_sample
from . import mass_function as _mass_function
from . import density_function as _density_function

try:
    _rand = _modules['sim_2024'].rand
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
    def sample(self,size:int=1)->_random_sample|None:
        """simulation of a sample of the random variate
        
        Args:
            size (int): Size of the desire sample
        """
        sample = _random_sample()
        for _ in range(size):
            sample.append(self.rand())
        return sample

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
    
    def __new__(cls,**kwargs:dict[str,float]):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1.:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict[str,float]):
        """all attributes are private"""
        self._p:float
        self._p = kwargs['p']
        self.mass_function:mass_function = _mass_function(function=lambda x:(self._p if x==1 else 1-self._p),sup=[0,1])
    
    def rand(self)->float:
        """simulate one value of the random variate"""
        global _rand
        u = _rand()
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
    def __new__(cls,**kwargs:dict[str,int|float]):
        """validation of parameters occurs here"""
        _validate_int_by_key(kwargs,'n','number of trials must be a positive integer',threshold=1)
        _validate_float_by_key(kwargs,'p','probability p must be a float between 0 and 1',threshold=0.0)
        if kwargs['p']>1.:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs:dict[str,int|float]):
        """all attributes are private"""
        self._p:float
        self._n:int
        self._p = float(kwargs['p'])
        self._n = int(kwargs['n'])
    def rand(self)->float:
        global _rand
        x:float
        x = 0.0
        for _ in range(self._n):
            u = _rand()
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
        global _rand
        u = _rand()
        x =  0.0
        while u>self._p:
            u = _rand()
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
        global _rand
        s = 1.0 if _rand()<self._p else 0
        x = 0.0 if s==1 else 1
        while s<self._s:
            s+= 1.0 if _rand()<self._p else 0
            x+= 0.0 if s==1 else 1
        return x

class DiscreteUniform(_discrete_variate):
    """Discrete uniform distribution.

    Keyword Args:
        size (int): if provided, the class will represenr Discrete distribution on inetegers 1,2,...,size.
        sup (list[float]): if provided, the class will represent Discrete distribution on the set {members of list}.
    """
    
    _sub_type = 'uniform'
    
    def __new__(cls,**kwargs:dict[str,_Any]):
        """validation of parameters occurs here"""
        size:bool
        sup:bool
        size = True if 'size' in kwargs else False
        sup = True if 'sup' in kwargs else False
        if not (size^sup):
            raise KeyError('initialization must include one and just one:size or sup')
        if 'size' in kwargs:
            _validate_int(kwargs['size'],'size must be an integer greater than 1',2)
        if 'sup' in kwargs:
            _validate_list(kwargs['sup'],'sup must be a list of int or float numbers')
            if len(kwargs['sup'])<2:
                raise ValueError('sup must be a list of size at leats 2')
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict[str,_Any]) -> None:
        """all attributes are private"""
        self._type:str
        self._size:int
        self._sup:list[float]
        self._type = 'size' if ('size' in kwargs) else 'sup'
        if self._type=='size':
            self._size = kwargs['size']
            self._sup = [float(i) for i in range(1,self._size+1)]
        else:
            self._sup = kwargs['sup']
            self._size = len(self._sup)
    
    def rand(self)->float:
        """generation of one random number"""
        global _rand
        u:float = _rand()
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
    def __new__(cls,**kwargs:dict[str,_Any]):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'rate',threshold=0.0,exceptions=0.0)
        return super().__new__(cls)
    
    def __init__(self,**kwargs:dict[str,_Any]) -> None:
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
        sup (tuple): support of distribution.
    """

    #def __new__(cls,**kwargs:dict):
    #    """validation of parameters occurs here"""
    def __init__(self,**kwargs:dict[str,tuple[float]])->None:
        self._sup = kwargs['sup']
    def rand(self)->float:
        global _rand
        u:float = _rand()
        return self._sup[0]+u*(self._sup[1]-self._sup[0])

class Exponential(_continuos_variate):
    """Exponential distribution.

    Keyword Args:
        rate (float): rate parameter 
    """
    
    def __new__(cls,**kwargs:dict[str,float]):
        """validation of parameters occurs here"""
        _validate_float_by_key(kwargs,'rate','rate must be a positive number',threshold=0.0,exceptions=0.0)
        return super().__new__(cls)

    def __init__(self,**kwargs:dict[str,float])->None:
        self._rate:float = kwargs['rate']
        #self._density:density_function = density_function(lambda x: self._rate*exp(-self._rate*x),min=0,max=None)

    def rand(self)->float:
        """generation of one random number"""
        global _rand
        u = _rand()
        return -_log(u)/self._rate

class _NormalStd(_continuos_variate):
    def __init__(self)->None:
        pass
    def _rand(self)->float:
        global _rand
        s=2
        while s>1:
            u = _rand()
            v = _rand()
            x = 2*u -1
            y = 2*v -1
            s = x**2+y**2
        return (x*((-2*_log(s)/s)**0.5),y*((-2*_log(s)/s)**0.5))
    def rand(self)->float:
        return self._rand()[0]
    def sample(self,size:int=1)->_random_sample:
        pairs = [self._rand() for _ in range(size//2+size%2)]
        _sample = _random_sample()
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
    
    def sample(self,size:int=1)->_random_sample:
        _stdsample = self._stdvariate.sample(size)
        _sample = _random_sample()
        for z in _stdsample:
            _sample.append(self._mean+self._stdev*z)
        return _sample

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
        self.b = 4*(shape**shape)*_exp(shape)/(self.a*_gamma(shape))
    def __call__(self,x:float)->float:
        if self.shape<1:
            if 1<x:
                return _exp(-x)/self.shape
            else:
                return x**(self.shape-1)/self.shape
        else:
            return (self.b*x**(self.a-1))/((self.shape**self.a+x**self.a)**2)

class Gamma(_continuos_variate):
    """Gamma distribution
    
    """
    
    _sub_type = 'gamma distribution'
    
    def __new__(cls,**kwargs:dict[str,float]):
        """validation of parameters occurs here"""
        if 'shape' not in kwargs:
            raise KeyError('parameter shape not found')
        _validate_float_by_key(kwargs,'shape','shape must be a float positive number',threshold=0.0,exceptions=0.0)
        if 'rate' not in kwargs and 'scale' not in kwargs:
            raise KeyError('parameter rate or shape must be provided')
        if 'rate' in kwargs and 'scale' in kwargs:
            raise KeyError('only one parameter rate or shape must be provided')
        if 'rate' in kwargs:
            _validate_float_by_key(kwargs,'rate','rate must be a  float positive number',threshold=0.0,exceptions=0.0)
        if 'scale' in kwargs:
            _validate_float_by_key(kwargs,'scale','scale must be a  float positive number',threshold=0.0,exceptions=0.0)
        return super().__new__(cls)

    def __init__(self,**kwargs)->None:
        self._shape:float
        self._rate:float
        self._scale:float
        self._mayorant:_mayorant_Gamma_density
        self._shape = kwargs['shape']
        if 'rate' in kwargs:
            self._rate = kwargs['rate']
            self._scale = 1/self._rate
        if 'scale' in kwargs:
            self._scale = kwargs['scale']
            self._rate = 1/self._scale
        self._mayorant = _mayorant_Gamma_density(self._shape)

    def rand(self)->float:
        global _rand
        x:float
        u:float
        y:float
        if self._shape == 1:
            return Exponential(rate=1.0).rand()
        u = _rand()
        if self._shape<1:
            y = ((_exp(0)+self._shape)*u/_exp(0)) if u<_exp(0)/(_exp(0)+self._shape) else -_log((_exp(0)+self._shape)*(1-u)/(_exp(0)*self._shape))
        else:
            y = (u*self._shape**self._mayorant.a/(1-u))**(1/self._mayorant.a)
        u = _rand()
        while u*self._mayorant(y)>y**(self._shape-1)*_exp(-y)/_gamma(self._shape):
            u = _rand()
            if self._shape<1:
                y = ((_exp(0)+self._shape)*u/_exp(0)) if u<_exp(0)/(_exp(0)+self._shape) else -_log((_exp(0)+self._shape)*(1-u)/(_exp(0)*self._shape))
            else:
                y = (u*self._shape**self._mayorant.a/(1-u))**(1/self._mayorant.a)
            u = _rand()
        return y/self._rate        

class Beta(_continuos_variate):
    """Beta distribution
    
    """
    
    _sub_type = 'beta distribution'

    def __init__(self,**kwargs:dict[str,float])->None:
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
        global _rand
        u:float
        u = _rand()
        if u<(self._b-self._a)**2/((self._c-self._a)*(self._b-self._a)):
            return self._a + (u*(self._c-self._a)*(self._b-self._a))**0.5
        else:
            return self._c - ((1-u)*(self._c-self._a)*(self._c-self._b))**0.5

class ExampleDis(_continuos_variate):
    def rand(self)->float:
        global _rand
        y:float
        u:float
        u = _rand()
        y = 2*u-1
        u = _rand()
        while 4*u>3/(y**2+y+1):
            u = _rand()
            y = 2*u-1
            u = _rand()
        return y

__all__ = [
    'Bernoulli',
    'Binomial',
    'Geometric',
    'NegativeBinomial',
    'DiscreteUniform',
    'Poisson',
    'ContinuosUniform',
    'Exponential',
    'Normal',
    'Chisq',
    'Student',
    'BoundedNormal',
    'RectifiedNormal',
    'Gamma',
    'Beta',
    'Triangular',
    'ExampleDis'
]