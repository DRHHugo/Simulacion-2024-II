from scipy.stats import norm
from scipy.stats import chi2
from typing import Iterator
from __init__ import *

def mean_est(sample:list[float])->float:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n:int = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    summ:float = sum(sample)
    mean:float = summ/n
    return mean

def mean_test(sample:list[float],sig:float=0.95)->float:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n:int = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        raise TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        raise ValueError('significance must be in the range (0,1)')
    mean:float = mean_est(sample)
    threshold:float = 1-(1-sig)/2
    if abs((mean-0.5))>norm.ppf(threshold)*(1/(n*12))**0.5:
        return False
    else:
        return True

def var_est(sample:list[float])->float:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    sumss:float = 0.0
    for u in sample:
        sumss+= (u-0.5)**2
    var:float = sumss/n
    return var

def var_test(sample:list[float],sig:float=0.95)->bool:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        raise TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        raise ValueError('significance must be in the range (0,1)')
    var:float = var_est(sample)
    threshold = sig
    if abs((var-1/12))>norm.ppf(threshold,)*(1/(n*180))**0.5:
        return False
    else:
        return True

def chisq_est(sample:list[float],k:int)->float:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    if type(k)!=int:
        raise TypeError('k must be an integer')
    if k<1:
        raise ValueError('k must be at least two')
    freq:list[int] = [0 for _ in range(k)]
    for u in sample:
        freq[int(k*u)]+=1
    sumss:float = 0.0
    for f in freq:
        sumss+=(f-n/k)**2
    chisq_0:float = (k/n)*sumss
    return chisq_0

def chisq_test(sample:list[float],k:int,sig:float=0.95)->bool:
    if type(sample)!=list:
        raise TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        raise ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        raise TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        raise ValueError('significance must be in the range (0,1)')
    chisq_0 = chisq_est(sample,k)
    threshold = sig
    if chisq_0>chi2.ppf(threshold,k-1):
        return False
    else:
        return True

def series_est(sample:list[float],l:int,d:int)->float:
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
    sumss = 0
    f_teo = m/(l**d)
    for f in freq:
        sumss+= (f-f_teo)**2
    chisq_0 = (l**d)*sumss/m
    return chisq_0

def series_test(sample:list[float],l:int,d:int,sig:float=0.95)->bool:
    chisq_0 = series_est(sample,l,d)
    threshold = sig
    if chisq_0>chi2.ppf(threshold,l**d-1):
        return False
    else:
        return True

__all__ = [
    'mean_est',
    'mean_test',
    'var_est',
    'var_test',
    'chisq_test',
    'series_est',
    'series_test'
    ]