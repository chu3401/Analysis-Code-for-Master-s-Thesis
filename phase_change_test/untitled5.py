# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 09:12:54 2025

@author: C
"""
import numpy as np
from math import sqrt
from matplotlib import pyplot as plt



def get_visc(edot, T, n, A, E):
    '''edot: second invariant of strain rate
    T: temperature in Celsius
    n, A, E: viscosity parameters

    return viscosity in Pascal.s
    '''
    R = 8.31448  # gas constant
    pow = 1.0/n - 1
    pow1 = -1.0/n
    visc = 0.25 * (edot**pow) * (0.75*A)**pow1 * np.exp(E / (n * R * (T + 273))) * 1e6
    return visc

'''
edot = 1e-14  # high strain rate


tmpr=np.arange(0,1301,1)
n=1.5
A=1.25e0
E=1.76e+5

visc = get_visc(edot, tmpr, n, A, E)
for i in range(len(visc)):
    if (visc[i]>3e27):
        visc[i]=3e27
    elif (visc[i]<1e19):
        visc[i]=1e19
visc2 = get_visc(edot, tmpr, 3.05, 1.25e-1, 3.76e5)
for i in range(len(visc2)):
    if (visc2[i]>3e27):
        visc2[i]=3e27
fig1=plt.figure(figsize=(3,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(np.log10(visc),tmpr)
ax1.plot(np.log10(visc2),tmpr)
ax1.set_ylim(1200,0)
ax1.set_xlim(18,28)
ax1.grid()
'''


den=3200
tmpr=np.arange(0,1301,1)

dens=den*(1-3e-5*tmpr)

fig1=plt.figure(figsize=(3,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(dens,tmpr)
ax1.set_ylim(1300,0)















