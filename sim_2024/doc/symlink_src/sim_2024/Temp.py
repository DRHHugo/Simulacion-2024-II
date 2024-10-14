from random import random as rand
from random import seed

class Geometric():
    """representation of a random variate of Bernoulli type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Bernoulli'

    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs):
        """All Attributes are private"""
        self._p:float = kwargs['p']
    def rand(self)->float:
        #global rand
        u = rand()
        x =  0.0
        while u>self._p:
            u = rand()
            x+= 1
        return x

class NegativeBinomial():
    """representation of a random variate of Bernoulli type
    
    Representation of random variate include ...

    Keyword Args:
        p (float): Sucess probability
    """
    _sub_type = 'Bernoulli'

    def __new__(cls,**kwargs):
        """validation of parameters occurs here"""
        #_validate_float_by_key(kwargs,'p','probability p must be a float betwenn 0 and 1',threshold=0.0)
        if kwargs['p']>1:
            raise ValueError('probability p must be a float betwenn 0 and 1')
        return super().__new__(cls)
    def __init__(self,**kwargs):
        """All Attributes are private"""
        self._p:float = kwargs['p']
        self._s:float = kwargs['s']
    def rand(self)->float:
        #global rand
        s = 1 if rand()<self._p else 0
        x = 0 if s==1 else 1
        while s<self._s:
            s+= 1 if rand()<self._p else 0
            x+= 0 if s==1 else 1
        return x

