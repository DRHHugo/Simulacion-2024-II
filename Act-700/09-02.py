def num_to_base_2(n:int,k:int|None=None) -> list[bool]|None:
    if k==None:
        if n<0:
            return None
        if n==0:
            return [False]
        if n==1:
            return [True]
        bit = False if n%2==0 else True
        rest = num_to_base_2(n//2)
        rest.insert(0,bit)
        return rest
    elif k<0:
        return None
    else:
        n=n%(2**k)
        rep = num_to_base_2(n,None)
        while len(rep)<k:
            rep = rep + [False]
        return rep

def base_2_to_num(l:list[bool])->int|None:
    if len(l)==0:
        return None
    if len(l)==1:
        return int(l[0])
    else:
        return l[0]+2*base_2_to_num(l[1:len(l)])

def linear_feedback(l:list[bool]):
    return [l[1],l[2],l[3],l[0]^l[1]^l[3]]