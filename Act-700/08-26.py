class generador_multiplicativo_congruencial:
    def __init__(self,m,b,x):
        self.mod = m
        self.mul = b
        self.seed = x

gen = generador_multiplicativo_congruencial(2023,1024,7)

print(gen.mod)