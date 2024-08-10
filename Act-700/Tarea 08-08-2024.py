# import list of primes as primes
FILE_primes = open('primes.py','r')
exec(FILE_primes.read())

def find_next_prime(N,start_i):
    if N<=1 or type(N)!=int:
        return -1
    i = start_i
    p = primes[i]
    r = N%p
    while r!=0:
        i+=1
        p = primes[i]
        r = N%p
    return i

def factorization(N):
    n = N
    i = 0
    factorization = []
    while n>1:
        i = find_next_prime(n,i)
        factorization.append(i)
        p = primes[i]
        n = n//p
    return factorization

def compactification(L):
    if len(L) ==0:
        return []
    i = 0
    j = len(L)
    compact_list = []
    L.append(-1)
    while i<j:
        e = L[i]
        compact_list.append([e,L.count(e)])
        i+=1
        while e == L[i] and i<j:
            i+=1
    return compact_list

def periodo_maximo(N):
    primes_list_powers = compactification(factorization(N))
    power_primes_factors = []
    other_factors =[]
    for [i,n] in primes_list_powers:
        if i==0:
            if n==2:
                power_primes_factors.append([0,1])
            else:
                power_primes_factors.append([0,n-2])
        else:
            if n==1:
                power_primes_factors.append([i,1])
            else:
                power_primes_factors.append([i,n-1])
                other_factors.append(primes[i]-1)
    print(power_primes_factors)
    print(other_factors)