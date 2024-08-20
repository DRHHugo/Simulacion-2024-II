def PRMCG(m:int,b:int,x:int,n:int):
    b=b%m
    x=x/m
    if n<0:
        return None
    if n==0:
        rerurn []|
    sample = []
    while len(sample)<n:
        sample.append(x:=b*x%m)
    return sample

def evaluate_pol(coef,x:int)
    

def PRMCG(m:int,b:int,c:int,x:int,n:int):
    b=b%m
    x=x/m
    c=c%m
