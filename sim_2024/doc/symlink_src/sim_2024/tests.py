from typing import Iterator
from copy import copy
from math import floor
from scipy.stats import norm
from scipy.stats import chi2
from . import _validate_sample

def _validate_sig(sig:float)->None:
    if type(sig)!=float:
        raise TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        raise ValueError('significance must be in the range (0,1)')
    return None
    
def mean_est(sample:list[float])->float:
    _validate_sample(sample,'')
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

def variance_est(sample:list[float])->float:
    _validate_sample(sample)
    sumss:float = 0.0
    for u in sample:
        sumss+= (u-0.5)**2
    var:float = sumss/len(sample)
    return var

def variance_test(sample:list[float],sig:float=0.95)->bool:
    _validate_sig(sig)
    var:float = variance_est(sample)
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
    chisq:float = series_est(sample,l,d)
    threshold = sig
    if chisq>chi2.ppf(threshold,l**d-1):
        return False
    else:
        return True

def runs_est(sample:list[float])->float:
    _validate_sample(sample)
    sample_copy:list[float] = copy(sample)
    sample_copy.append(0)
    runs:list[int] = [0 for _ in range(6)]
    i:int = 0
    n:int = len(sample)
    long:int = 1
    while i<n:
        if sample_copy[i]>sample_copy[i+1]:
            if long>=6:
                runs[5]+=1
            else:
                runs[long-1]+=1
            long=0
        i+=1
        long+=1
    A:list[list[float]] = [
        [4529.4,9044.9,13568,18091,22615,27892],
        [9044.9,18097,27139,36187,45234,55789],
        [13568,27139,40721,54281,67852,83685],
        [18091,36187,54281,72414,90470,111580],
        [22615,45234,67852,90470,113262,139476],
        [27892,55789,83685,111580,139476,172860]]
    b:list[float] = [n/6,5*n/24,11*n/120,19*n/720,29*n/5040,n/840]
    summ:float = 0.0
    for i in range(6):
        for j in range(6):
            summ+=A[i][j]*(runs[i]-b[i])*(runs[j]-b[j])
    chisq:float = summ/n
    return chisq

def runs_test(sample:list[float],sig:float=0.95)->bool:
    _validate_sig(sig)
    chisq:float = runs_est(sample)
    threshold:float = sig
    if chisq>chi2.ppf(threshold,6):
        return False
    else:
        return True

__all__ = [
    'mean_est',
    'mean_test',
    'variance_est',
    'variance_test',
    'chisq_est',
    'chisq_test',
    'series_est',
    'series_test',
    'runs_est',
    'runs_test'
    ]