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


trx_750myr=np.load("trx_750myr.npy")
trt_750myr=np.load("trt_750myr.npy")

trx_500myr=np.load("trx_500myr.npy")
trt_500myr=np.load("trt_500myr.npy")

trx_250myr=np.load("trx_250myr.npy")
trt_250myr=np.load("trt_250myr.npy")

trx_050myr=np.load("trx_050myr.npy")
trt_050myr=np.load("trt_050myr.npy")

xx1=np.array([])
tt1=np.array([])
for i in range(0,len(trx_050myr)-1,3):
    xx1=np.append(xx1,(trx_050myr[i]-trx_050myr[i+1])/(trt_050myr[i]-trt_050myr[i+1]))
    tt1=np.append(tt1,abs(trt_050myr[i]+trt_050myr[i+1])/2)
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
    
fig1=plt.figure(figsize=(8,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(c.smooth_1d_array(xx4, n),tt4,label='750 Myr')
ax1.plot(c.smooth_1d_array(xx3, n),tt3,label='500 Myr')
ax1.plot(c.smooth_1d_array(xx2, n),tt2,label='250 Myr')
ax1.plot(c.smooth_1d_array(xx1, n),tt1,label='50 Myr')
ax1.grid()
ax1.legend(prop={'family': "Times New Roman",'size': 15},loc=4)

ax1.set_ylabel("Time (Myr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_ylim(1,19)#-80,40 #-150,10 2plot #-165,60 2plot #-170,10 3plot
ax1.set_yticks(ticks=np.arange(1,20.1,3))
ax1.set_yticklabels(np.arange(1,20.1,3),fontdict={"name": "Times New Roman"},fontsize=14)

ax1.set_xlabel("Velocity (mm/yr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_xlim(-20,80)
ax1.set_xticks(ticks=np.arange(-20,81,10))
ax1.set_xticklabels(np.arange(-20,81,10),fontdict={"name": "Times New Roman"},fontsize=14)
'''
fig1=plt.figure(figsize=(8,8),dpi=200)
ax1=fig1.add_subplot(1,1,1)
ax1.plot(trx_750myr,trt_750myr,label='750 Myr')
ax1.plot(trx_500myr,trt_500myr,label='500 Myr')
ax1.plot(trx_250myr,trt_250myr,label='250 Myr')
ax1.plot(trx_050myr,trt_050myr,label='50 Myr')
ax1.grid()
ax1.legend(prop={'family': "Times New Roman",'size': 15},loc=4)

ax1.set_ylabel("Time (Myr)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_ylim(1,19)#-80,40 #-150,10 2plot #-165,60 2plot #-170,10 3plot
ax1.set_yticks(ticks=np.arange(1,20.1,3))
ax1.set_yticklabels(np.arange(1,20.1,3),fontdict={"name": "Times New Roman"},fontsize=14)

ax1.set_xlabel("Distance (km)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_xlim(400,1200)
ax1.set_xticks(ticks=np.arange(400,1201,200))
ax1.set_xticklabels(np.arange(400,1201,200),fontdict={"name": "Times New Roman"},fontsize=14)
'''