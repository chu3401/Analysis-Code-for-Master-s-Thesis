# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 16:11:18 2025

@author: C
"""

import numpy as np
from matplotlib import pyplot as plt

p410=np.loadtxt("p410.dat")
p660=np.loadtxt("p660.dat")

fig1=plt.figure(figsize=(5,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
t410=[p410[0,0],p410[1,0]]
d410=[p410[0,1],p410[1,1]]
t660=[p660[0,0],p660[1,0]]
d660=[p660[0,1],p660[1,1]]

tt410=np.array([])
dd410=np.array([])
for i in range(2500):
    tt410=np.append(tt410,i)
    d=0.102*i+216.82
    dd410=np.append(dd410,d*-1)

tt660=np.array([])
dd660=np.array([])
for i in range(2500):
    tt660=np.append(tt660,i)
    d=-0.0666*i+788.49
    dd660=np.append(dd660,d*-1)

tt=np.array([])
dd=np.array([])
den=np.array([])
for i in range(700,1700,2):
    for j in range(-800,1,2):
        tmpr=i+abs(j*0.35)
        j=j*1000
        tt=np.append(tt,tmpr)
        dd=np.append(dd,j/1000)
        di=-101.58*tmpr-216828
        dii=66.55*tmpr-788494
        if (dii<j<di):
            den=np.append(den,1.1)
        elif (dii>j):
            den=np.append(den,1.2)
        else:
            den=np.append(den,1.0)
            
        

ax1.plot(t410,d410[:])
ax1.plot(tt410,dd410[:],lw=2,c='k')
ax1.plot(t660,d660[:])
ax1.plot(tt660,dd660[:],lw=2,c='k')
ax1.plot([1000,2500],[-410,-410],lw=2,c='r')
ax1.plot([1000,2500],[-660,-660],lw=2,c='r')
cax=ax1.scatter(tt,dd,c=den,cmap='jet')
#ax1.plot(p660)
ax1.set_ylim(-800,00)
ax1.set_ylabel("Depth (km)")
ax1.set_xlim(1000,2300)
ax1.set_xlabel("Temperature (K)")
fig1.colorbar(cax,ax=ax1)
ax1.grid()

#print( 3450*(1-2e-5*1350) )