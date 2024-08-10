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