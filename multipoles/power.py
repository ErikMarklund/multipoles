#!/usr/bin/env python

from multipoles import MultipoleExpansion
import numpy as np

def power_spectrum(Phi):
    l_max = Phi.l_max
    c = np.zeros(l_max+1)
    
    for l in range(l_max+1):
        cl = 0
        for m in range(-l, l+1):
            clm = Phi.multipole_moments[(l, m)]
            cl += clm.real**2 + clm.imag**2
            
        c[l] = cl

    return c

    
