from scipy.stats import norm

def mean_test(sample:list,sig:float)->bool:
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
    if abs((mean-0.5))>norm.ppf(threshold,)*(1/(n*12))**0.5:
        return False
    else:
        return True