def multiple_PRNG(m,b,x,n):
    if len(b)!=len(x):
        raise ValueError('dimensiones no complatibles')
    state=x
    sample=[]
    while len(sample)!=n:
        s=0
        for k in range(len(b)):
            s=(s+b[k]*x[k])%m
        if s!=0:
            sample.append(s/m)
        state.pop()
        state.insert(0,s)
    return sample