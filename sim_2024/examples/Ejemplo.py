from os import chdir
chdir('D:\\OneDrive\\Documents\\GitHub\\Simulacion-2024-II\\sim_2024\\src')
from sim_2024.generators import multiplicative_congruential_generator

random = multiplicative_congruential_generator(mod=2**32,mult=65321,seed=48158)

class Bernoulli:
    def __init__(self,p):
        self.p = p
    def simular(self,n):
        sample = []
        for _ in range(n):
            u = random.rand()
            if u<self.p:
                sample.append(1)
            else:
                sample.append(0)

        return sample
