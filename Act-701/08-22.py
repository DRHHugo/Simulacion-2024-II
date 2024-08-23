def quadratic_PRNG(m:int,x:int,n:int):
    x=x**2%m
    sample=[]
    while (x!=0) and (len(sample)<n):
        sample.append(x/m)
        x=x**2%m
    return sample