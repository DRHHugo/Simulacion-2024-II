from scipy.stats import norm
from scipy.stats import chi2
from typing import Iterator
from __init__ import *

def _validate_sample(sample:list[float])->None:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    if len(sample)<=1:
        raise ValueError('sample must contains at least two elements')
    return None

def _validate_sig(sig:float)->None:
    if type(sig)!=float:
        raise TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        raise ValueError('significance must be in the range (0,1)')
    return None
    
def mean_est(sample:list[float])->float:
    _validate_sample(sample)
    summ:float = sum(sample)
    mean:float = summ/len(sample)
    return mean

def mean_test(sample:list[float],sig:float=0.95)->float:
    _validate_sig(sig)
    mean:float = mean_est(sample)
    threshold:float = 1-(1-sig)/2
    n:int = len(sample)
    if abs((mean-0.5))>norm.ppf(threshold)*(1/(n*12))**0.5:
        return False
    else:
        return True

def var_est(sample:list[float])->float:
    _validate_sample(sample)
    sumss:float = 0.0
    for u in sample:
        sumss+= (u-0.5)**2
    var:float = sumss/len(sample)
    return var

def var_test(sample:list[float],sig:float=0.95)->bool:
    _validate_sig(sig)
    var:float = var_est(sample)
    threshold = sig
    n:int = len(sample)
    if abs((var-1/12))>norm.ppf(threshold,)*(1/(n*180))**0.5:
        return False
    else:
        return True

def chisq_est(sample:list[float],k:int)->float:
    _validate_sample(sample)
    if type(k)!=int:
        raise TypeError('k must be an integer')
    if k<1:
        raise ValueError('k must be at least two')
    freq:list[int] = [0 for _ in range(k)]
    for u in sample:
        freq[int(k*u)]+=1
    sumss:float = 0.0
    n:int = len(sample)
    for f in freq:
        sumss+=(f-n/k)**2
    chisq:float = (k/n)*sumss
    return chisq

def chisq_test(sample:list[float],k:int,sig:float=0.95)->bool:
    _validate_sig(sig)
    chisq:float = chisq_est(sample,k)
    threshold:float = sig
    if chisq>chi2.ppf(threshold,k-1):
        return False
    else:
        return True

def series_est(sample:list[float],l:int,d:int)->float:
    _validate_sample(sample)
    if type(l)!=int:
        raise TypeError('l must be a positive integer')
    if l<=0:
        raise ValueError('l must be  positive integer')
    if type(d)!=int:
        raise TypeError('d must be a positive integer')
    if d<=0:
        raise ValueError('d must be  positive integer')
    freq:list[int] = [0 for _ in range(l**d)]
    n:int = len(sample)
    m:int = n//d
    sample_iterator:Iterator = iter(sample)
    tuples:list[list[float]] = [[next(sample_iterator) for _ in range(d)] for _ in range(m)]
    for tuple in tuples:
        k:int = 0
        for i in range(d):
            k+= floor(l*tuple[i])*(l**i)
        freq[k]+=1
    sumss:float = 0.0
    f_teo:float = m/(l**d)
    for f in freq:
        sumss+= (f-f_teo)**2
    chisq = (l**d)*sumss/m
    return chisq

def series_test(sample:list[float],l:int,d:int,sig:float=0.95)->bool:
    _validate_sig(sig)
    chisq_0 = series_est(sample,l,d)
    threshold = sig
    if chisq_0>chi2.ppf(threshold,l**d-1):
        return False
    else:
        return True

def runs_est(sample:list[float])->float:
    return 0.0


__all__ = [
    'mean_est',
    'mean_test',
    'var_est',
    'var_test',
    'chisq_test',
    'series_est',
    'series_test'
    ]