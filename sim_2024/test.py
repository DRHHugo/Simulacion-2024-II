from scipy.stats import norm
from scipy.stats import chi2
from __init__ import *

def mean_test(sample:list,sig:float=0.95)->bool:
    if type(sample)!=list:
        return TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        return ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        return TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        return ValueError('significance must be in the range (0,1)')
    sum = 0
    for u in sample:
        sum+= u
    mean = sum/n
    threshold = 1-(1-sig)/2
    if abs((mean-0.5))>norm.ppf(threshold)*(1/(n*12))**0.5:
        return False
    else:
        return True

def var_test(sample:list,sig:float=0.95)->bool:
    if type(sample)!=list:
        return TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        return ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        return TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        return ValueError('significance must be in the range (0,1)')
    sumss = 0
    for u in sample:
        sumss+= (u-0.5)**2
    var = sumss/n
    threshold = sig
    if abs((var-1/12))>norm.ppf(threshold,)*(1/(n*180))**0.5:
        return False
    else:
        return True

def chisq_test(sample:list,k:int,sig:float=0.95)->bool:
    if type(sample)!=list:
        return TypeError('sample must be a list')
    n = len(sample)
    if n<=1:
        return ValueError('sample must contains at least two elements')
    if type(sig)!=float:
        return TypeError('significance must be a float')
    if sig>=1 or sig<=0:
        return ValueError('significance must be in the range (0,1)')
    if type(k)!=int:
        return TypeError('k must be an integer')
    if k<1:
        return ValueError('k must be at least two')
    freq = [0 for _ in range(k)]
    for u in sample:
        freq[int(k*u)]+=1
    sumss = 0
    for f in freq:
        sumss+=(f-n/k)**2
    chisq_est = (k/n)*sumss
    threshold = sig
    if chisq_est>chi2.ppf(threshold,k-1):
        return False
    else:
        return True

def series_test(sample:list,m:int,k:int,sig:float=0.95)->bool: