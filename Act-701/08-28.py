def num_to_base_2(n:int,l:int|None=None)-> list[bool]:
    if l==None:
        if n<0:
            return []
        if n==0:
            return [False]
        if n==1:
            return [True]
        bit = False if n%2==0 else True
        rest = num_to_base_2(n//2)
        rest.insert(0,bit)
        return rest
    else:
        n=n%(2**l)
        return num_to_base_2(n)

def base_2_to_num(l:list[bool])->int|None:
    if len(l)==0:
        return None
    if len(l)==1:
        return int(l[0])
    else:
        return l[0]+2*base_2_to_num(l[1:len(l)])
