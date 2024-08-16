def PRMCG(m:int,b:int,x:int,n:int):
    return [x:=b*x%m for _ in range(n)]