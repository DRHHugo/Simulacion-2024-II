m=2023
b=507
k=1
r=2**k%m
while r!=1:
    k+=1
    r=b**k%m
print(k)