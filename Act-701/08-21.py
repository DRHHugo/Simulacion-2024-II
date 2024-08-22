def multiplicative_congruential_PRNG(m:int,b:int,x:int,n:int):
    if m<=1:
        raise ValueError('el módulo del generador pseudoaleatorio debe ser un número entero mayor a 1')
    if n<0:
        return None
    b=b%m
    x=x%m
    sample=[]
    while len(sample)<n:
        x=b*x%m
        if x==0:
            raise ValueError('no es posible simular la cantidad deseada de números pseudoaleatorios ')
        else:
            sample.append(x/m)
    return sample

def linear_congruential_PRNG(m:int,b:int,c:int,x:int,n:int):
    if m<=1:
        raise ValueError('el módulo del generador pseudoaleatorio debe ser un número entero mayor a 1')
    if n<0:
        return None
    b=b%m
    x=x%m
    sample=[]
    while len(sample)<n:
        x=(b*x+c)%m
        if x==0:
            raise ValueError('no es posible simular la cantidad deseada de números pseudoaleatorios ')
        else:
            sample.append(x/m)
    return sample
