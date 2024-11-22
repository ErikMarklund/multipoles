#!/usr/bin/env python

from multipoles import MultipoleExpansion
from math import *
import numpy as np
import random
from sys import argv

def spherical_to_cartesian(r, theta, phi):
    x = r * sin(theta)*cos(phi)
    y = r * sin(theta)*sin(phi)
    z = r * cos(theta)
    return x,y,z


def potential_direct(xyz, qd):
    P = 0
    for point in qd['charges']:
        q = point['q']
        pxyz = point['xyz']
        r = sqrt((xyz[0]-pxyz[0])**2 + (xyz[1]-pxyz[1])**2 + (xyz[2]-pxyz[2])**2)

        P += q/r

    vareps = 8.8541878188e-12 # C2 kg-1 m-3 s2
    
    #P *= 1/(4*pi*vareps)

    return P


def random_unitsphere_point():
    phi = 2 * pi * random.random()
    theta = asin(random.uniform(-1,1))
    return (theta, phi)


if __name__=='__main__':
    random.seed()
    
    # Place minat-maxat point charges inside a sphere of radius 1, calculate the potential
    # at random points at r=5 using both the multipole expansion and by direct summation.
    # Repeat N times to get statistics for the error.

    # Number of runs
    N = 100

    # minimum number of atoms
    minat = 2

    # maximum number of atoms
    maxat = 8

    # Use moments up to and including l=5
    l_max = 5

    # Usage:  python test_accuracy.py [N] [minat] [maxat] [l_max].
    # To use a default value, provide '-' as an argument for that position:
    #     python test_accuracy.py - 2 4 4
    # The above example uses the default number of runs, but sets the minimum
    # and maximum number of atoms to 2 and 4, and l_max to 4.
    
    narg = len(argv)-1

    # Override defaults if arguments are provided
    if narg >= 1:
        N_ = argv[1]
        if N_ != '-':
            N = int(N_)
    if narg >= 2:
        minat_ = argv[2]
        if minat_ != '-':
            minat = int(minat_)
    if narg >= 3:
        maxat_ = argv[3]
        if maxat_ != '-':
            maxat = int(maxat_)
    if narg >= 4:
        l_max_ = argv[4]
        if l_max_ != '-':
            l_max = int(l_max_)
            
    print(f'{N=}, {minat=}, {maxat=}, {l_max=}')
    
    Pdirect = []
    Pmpole  = []
    
    for run in range(N):

        # Make a charge distributuion

        qdist = {
            'discrete' : True,
            'charges'  : []
            }
        
        n = random.randint(minat,maxat)
        for i in range(n):
            # Generate uniformly distributed points in the sphere
            r = (random.random())**(1/3) # Avoid bias towards the center.
            theta, phi = random_unitsphere_point()

            xyz = spherical_to_cartesian(r, theta, phi)

            q = random.randint(0,1) * 2 - 1

            qdist['charges'].append({'q': q, 'xyz': xyz})

        rref = 5
        thetaref, phiref = random_unitsphere_point()
        xyzref = spherical_to_cartesian(rref, thetaref, phiref)
        
        Pdirect.append(potential_direct(xyzref, qdist))

        Phi = MultipoleExpansion(qdist, l_max)
        
        Pmpole.append(Phi(*xyzref))

    Pd = np.array(Pdirect)
    Pm = np.array(Pmpole)

    Perr = Pm-Pd
    Perr_rel = Perr/Pd

    Pse = Perr**2
    Pse_rel = Perr_rel**2

    print(f'mse     = {np.mean(Pse)}')
    print(f'mse_rel = {np.mean(Pse_rel)}')
        


    
