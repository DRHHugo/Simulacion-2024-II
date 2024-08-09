k=1
r=2**k%2023
while r!=1:
#    print("2**",k,"mod 2023=",r)
    k+=1
    r=2**k%2023
print("2**",k,"mod 2023=",r)