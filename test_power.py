#!/usr/bin/env python

import test_accuracy as ta
import random
from multipoles import MultipoleExpansion, power
from matplotlib import pyplot as plt

def print_moments(Phi):
    moments = Phi.multipole_moments
    for k,v in moments.items():
        print(f'l={k[0]:1}, m={k[1]:2}: {v}')

def test():
    
    random.seed(1336)

    l_max = 5
    
    qd = {
        'discrete': True,
        'charges' : []
        }
    
    for i in range(10):
        q = random.randint(-1,1)
        r = random.random()**(1/3)
        
        theta, phi = ta.random_unitsphere_point()
        xyz = ta.spherical_to_cartesian(r, theta, phi)
        
        qd['charges'].append({'q':q, 'xyz':xyz})

    Phi = MultipoleExpansion(qd, l_max)

    print_moments(Phi)
    
    return power.power_spectrum(Phi)


if __name__=='__main__':
    
    ps = test()

    print(f'{ps=}')
    
    plt.bar(range(ps.size), ps)
    plt.xlabel('l')
    plt.ylabel('power density')
    plt.savefig('power_spectrum.pdf')
