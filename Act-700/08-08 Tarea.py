# paqueteria
from copy import copy

# import list of primes as primes
# FILE_primes = open('primes.py','r')
# exec(FILE_primes.read())
# FILE_primes.close()

# Esta funcion devuelve el indice del primer primo mayor a *primes[start_i]* que divide a *N*   
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

# Esta funcion devuelve una lista con los indices de los primos que dividen a *N*, el indice de divisor
# aparece en la lista tantas veces como la mayor potencia del primo que divide a *N*
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

# Esta funcion toma una lista y devuelve otra lista con elementos unicos de la forma *[i,n]* donde i es un
# elemento presente en *L* y *n* es el numero de veces que se repite dicho elemento en *L*
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

# Esta funcion calcula el periodo maximo de un multiplicative congruential (pseudorandom) generator de modulo m 
def periodo_maximo(m):
    primes_list_powers = compactification(factorization(m))
    power_primes_factors = []
    other_factors =[]
    for [i,n] in primes_list_powers:
        if i==0:
            if n==2:
                power_primes_factors.append([0,1])
            else:
                power_primes_factors.append([0,n-2])
        else:
            if n>1:
                power_primes_factors.append([i,n-1])
            other_factors.append(primes[i]-1)
    for m in other_factors:
        power_primes_factors+=compactification(factorization(m))
    periodo_maximo_factors = sorted(power_primes_factors)
    periodo_maximo_factorization = []
    periodo_maximo_primes = []
    for k in range(len(periodo_maximo_factors)):
        [i,_] = periodo_maximo_factors[k]
        if i not in periodo_maximo_primes:
            periodo_maximo_primes.append(i)
    for i in periodo_maximo_primes:
        max = 1
        for k in range(len(periodo_maximo_factors)):
            [j,n] = periodo_maximo_factors[k]
            if i==j and max<n:
                max = n
        periodo_maximo_factorization.append([i,max])
    periodo_maximo = 1
    for k in range(len(periodo_maximo_factorization)):
        periodo_maximo*=primes[periodo_maximo_factorization[k][0]]**periodo_maximo_factorization[k][1]
    return periodo_maximo

# Esta funcion calcula todos los divisores de periodo_maximo(m)
def multiplier_orders(m):
    factors_primes = compactification(factorization(periodo_maximo(m)))
    [i,n] = factors_primes.pop(0)
    divisors_primes = [[[i,m]] for m in range(n+1)]
    new_divisors_primes = []
    while len(factors_primes)!=0:
        [i,n] = factors_primes.pop(0)
        for m in range(n+1):
            for divisor in divisors_primes:
                new_divisors_primes.append(divisor+[[i,m]])
        divisors_primes =  copy(new_divisors_primes)
        new_divisors_primes = []
    divisors = []
    for divisor_primes in divisors_primes:
        divisor = 1
        for k in range(len(divisor_primes)):
            divisor*=primes[divisor_primes[k][0]]**divisor_primes[k][1]
        divisors.append(divisor)
    return sorted(divisors)

# Esta funcion calcula la representacion binaria de N como una lista en la que el digito menos significativo es
# el primer elemento en la lista
def int_to_binary(N):
    if N<0:
        return []
    if N==0:
        return [False]
    if N==1:
        return [True]
    least_dig = True if N%2==1 else False
    quotient = N//2
    return [least_dig]+int_to_binary(quotient)

# Esta funcion devuelve el entero cuya representacion decimal esta contenida en *l*, inversa de *int_to_binary*
def binary_to_int(l):
    N = 0
    for k in range(len(l)):
        N+=l[k]*2**k
    return N

# Esta funcion calcula el periodo del multiplicative congruential (pseudorandom) generator de modulo m y
# multiplicador b. Si el multiplicador es un divisor de cero devuelve -1
def multiplier_order(b,m):
    if b%m==1:
        return 1
    all_divisors = multiplier_orders(m)
    residuals_for_powers_of_2 = {k:b**(2**k)%m for k in range(1)}
    for divisor in all_divisors:
        binary_rep_divisor = int_to_binary(divisor)
        while max(residuals_for_powers_of_2)<len(binary_rep_divisor)-1:
            i = max(residuals_for_powers_of_2)
            residuals_for_powers_of_2[i+1] = (residuals_for_powers_of_2[i]**2)%m
        residual_divisor_power = b**(1 if binary_rep_divisor[0] else 0)
        for k in range(1,len(binary_rep_divisor)):
            if binary_rep_divisor[k]:
                residual_divisor_power = (residual_divisor_power*residuals_for_powers_of_2[k])%m
        if residual_divisor_power==1:
            return divisor
    return -1
