# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 16:53:27 2025

@author: C
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import sys
sys.path.append("D:/util")
import c_flac_tool as c


trx_750myr=np.load("trx_30vel.npy")
trt_750myr=np.load("trt_30vel.npy")

trx_500myr=np.load("trx_70vel.npy")
trt_500myr=np.load("trt_70vel.npy")

trx_250myr=np.load("trx_30myr.npy")
trt_250myr=np.load("trt_30myr.npy")


xx2=np.array([])
tt2=np.array([])
for i in range(0,len(trx_250myr)-1,3):
    xx2=np.append(xx2,(trx_250myr[i]-trx_250myr[i+1])/(trt_250myr[i]-trt_250myr[i+1]))
    tt2=np.append(tt2,abs(trt_250myr[i]+trt_250myr[i+1])/2)
xx3=np.array([])
tt3=np.array([])
for i in range(0,len(trx_500myr)-1,3):
    xx3=np.append(xx3,(trx_500myr[i]-trx_500myr[i+1])/(trt_500myr[i]-trt_500myr[i+1]))
    tt3=np.append(tt3,abs(trt_500myr[i]+trt_500myr[i+1])/2)
xx4=np.array([])
tt4=np.array([])
for i in range(0,len(trx_750myr)-1,3):
    xx4=np.append(xx4,(trx_750myr[i]-trx_750myr[i+1])/(trt_750myr[i]-trt_750myr[i+1]))
    tt4=np.append(tt4,abs(trt_750myr[i]+trt_750myr[i+1])/2)
    
n=3
'''  
fig1=plt.figure(figsize=(8,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(c.smooth_1d_array(xx4, n),tt4,label='30 mm/yr')
ax1.plot(c.smooth_1d_array(xx3, n),tt3,label='70 mm/yr')
ax1.plot(c.smooth_1d_array(xx2, n),tt2,label='50 mm/yr')
ax1.grid()
ax1.legend(prop={'family': "Times New Roman",'size': 15},loc=4)

ax1.set_ylabel("Time (Myr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_ylim(1,19)#-80,40 #-150,10 2plot #-165,60 2plot #-170,10 3plot
ax1.set_yticks(ticks=np.arange(1,20.1,3))
ax1.set_yticklabels(np.arange(1,20.1,3),fontdict={"name": "Times New Roman"},fontsize=14)

ax1.set_xlabel("Velocity (mm/yr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_xlim(-20,20)
ax1.set_xticks(ticks=np.arange(-20,21,10))
ax1.set_xticklabels(np.arange(-20,21,10),fontdict={"name": "Times New Roman"},fontsize=14)
'''
fig1=plt.figure(figsize=(8,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(trx_750myr,trt_750myr,label='30 mm/yr',c='b')#9.205523
ax1.plot([400,600],[9.205523,9.205523],c='b',lw=2,ls='--')
ax1.plot([400,600],[13.208734,13.208734],c='b',lw=2,ls='-.')

ax1.plot(trx_250myr,trt_250myr,label='50 mm/yr',c='r')
ax1.plot([400,600],[6.304365,6.304365],c='r',lw=2,ls='--')
ax1.plot([400,600],[9.807111,9.807111],c='r',lw=2,ls='-.')#9.807111

ax1.plot(trx_500myr,trt_500myr,label='70 mm/yr',c='k')#5.413523
ax1.plot([400,600],[5.413523,5.413523],c='k',lw=2,ls='--')
ax1.plot([400,600],[8.822289,8.822289],c='k',lw=2,ls='-.')



ax1.grid()
ax1.legend(prop={'family': "Times New Roman",'size': 15},loc=4)

ax1.set_ylabel("Time (Myr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_ylim(1,19)#-80,40 #-150,10 2plot #-165,60 2plot #-170,10 3plot
ax1.set_yticks(ticks=np.arange(1,20.1,3))
ax1.set_yticklabels(np.arange(1,20.1,3),fontdict={"name": "Times New Roman"},fontsize=14)

ax1.set_xlabel("Distance (km)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_xlim(400,600)
ax1.set_xticks(ticks=np.arange(400,601,50))
ax1.set_xticklabels(np.arange(400,601,50),fontdict={"name": "Times New Roman"},fontsize=14)
