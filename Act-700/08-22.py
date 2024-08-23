def multiplicative_congruential_PRNG(modulus:int,multiplier:int,seed:int,size:int)->list[float]|None:
    if size<0 or modulus<=0:
        return None
    if size==0:
        return []
    multiplier = multiplier%modulus
    state:int = seed%modulus
    sample:list[float] = []
    while len(sample)<size and state!=0:
        state = multiplier*state%modulus
        if state!=0:
            sample.append(state/modulus)
    return sample

def linear_congruential_PRNG(modulus:int,multiplier:int,constant:int,seed:int,size:int)->list[float]|None:
    if constant==0:
        return multiplicative_congruential_PRNG(modulus,multiplier,seed,size)
    if size<0 or modulus<=0:
        return None
    if size==0:
        return []
    constant = constant%modulus
    multiplier = multiplier%modulus
    state:int = seed%modulus
    sample:list[float] = []
    while len(sample)<size:
        state = (multiplier*state+constant)%modulus
        if state!=0:
            sample.append(state/modulus)
    return sample

def quadratic_congruential_PRNG(modulus:int,seed:int,size:int)->list[float]|None:
    if size<0 or modulus<=0:
        return None
    if size==0:
        return []
    state:int = seed%modulus
    sample:list[float] = []
    while len(sample)<size and state!=0:
        state = state**2%modulus
        if state!=0:
            sample.append(state/modulus)
    return sample

def polynomial_congruential_PRNG(modulus:int,coefficients:list[int],seed:int,size:int)->list[float]|None:
    if size<0 or modulus<=0 or len(coefficients)==0:
        return None
    if size==0:
        return []
    state:int = seed%modulus
    sample:list[float] = []
    while len(sample)<size and (state!=0 or coefficients[0]!=0):
        powers:list[int] = [1]
        monomials:list[int] = [coefficients[0]]
        for k in range(1,len(coefficients)):
            powers.append(powers[-1]*state%modulus)
            monomials.append(coefficients[k]*powers[-1]%modulus)
        state =  sum(monomials)%modulus
        if state!=0:
            sample.append(state/modulus)
    return sample

def multiple_congruential_PRNG(modulus:int,multipliers:list[int],seeds:list[int],size:int)->list[float]|None:
    if size<0 or modulus<=0 or len(multipliers)!=len(seeds):
        return None
    if size==0:
        return []
    temp_multipliers = [multipliers[i]%modulus for i in range(len(multipliers))]
    temp_seeds = [seeds[i]%modulus for i in range(len(multipliers))]
    multipliers = temp_multipliers
    state = temp_seeds
    sample:list[float] = []
    while len(sample)<size and state!=0:
        x = 0
        for k in range(len(multipliers)):
            x = (x+state[k]*multipliers[k])%modulus
        state.pop()
        state.insert(0,x)
        if x!=0:
            sample.append(x/modulus)
    return sample

def combined_congruential_PRNG(modulus:list[int],multipliers:list[int],seeds:list[int],size:int)->list[float]|None:
    if size<0 or len(modulus)!=2 or len(multipliers)!=2 or len(seeds)!=2:
        return None
    if modulus[0]<0 or modulus[1]<0:
        return None
    if size==0:
        return []
    multiplier_1 = multipliers[0]%modulus[0]
    multiplier_2 = multipliers[1]%modulus[1]
    state = [seeds[0]%modulus[0],seeds[1]%modulus[1]]
    sample:list[float] = []
    while len(sample)<size and state[0]!=0 and state[1]!=0:
        state=[multiplier_1*state[0]%modulus[0],multiplier_2*state[1]%modulus[1]]
        z = (state[0]-state[1])%modulus[0]
        if z!=0:
            sample.append(z/modulus[0])
    return sample

def multiple_combined_PRNG(modulus:list[int],multipliers:list[list[int]],seeds:list[list[int]],size:int)->list[float]|None:
    if size<0 or len(modulus)!=2 or len(multipliers)!=2 or len(seeds)!=2:
        return None
    if modulus[0]<0 or modulus[1]<0:
        return None
    if len(multipliers[0])!=len(seeds[0]) or len(multipliers[1])!=len(seeds[1]):
        return None
    if size==0:
        return []
    temp_multipliers = [[multipliers[0][i]%modulus[0] for i in range(len(multipliers[0]))],[multipliers[1][i]%modulus[1] for i in range(len(multipliers[1]))]]
    temp_seeds = [[seeds[0][i]%modulus[0] for i in range(len(multipliers[0]))],[seeds[1][i]%modulus[1] for i in range(len(multipliers[1]))]]
    multipliers = temp_multipliers
    state = temp_seeds
    sample:list[float] = []
    while len(sample)<size:
        x = 0
        for k in range(len(multipliers[0])):
            x = (x+state[0][k]*multipliers[0][k])%modulus[0]
        y = 0
        for k in range(len(multipliers[1])):
            y = (y+state[1][k]*multipliers[1][k])%modulus[1]
        state[0].pop()
        state[1].pop()
        state[0].insert(0,x)
        state[1].insert(0,y)
        z = (x-y) %modulus[0]
        if z!=0:
            sample.append(z/modulus[0])
    return sample
