# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 11:57:47 2025

@author: C

for pyflac
"""

import sys
import os
import math
sys.path.append("D:/util")
import flac
import flac_interpolate
import c_flac_tool as c
import numpy as np
import flacmarker2vtk
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import xarray as xr
import matplotlib.font_manager as font_manager
import pandas as pd

cpt_data = [
    (-20, (3, 67.75, 128.88)),
    (-18, (7.6249, 88.25, 142.25)),
    (-16, (30.75, 111.75, 157.38)),
    (-14, (66.375, 137.25, 175.12)),
    (-12, (105.63, 163.75, 192.88)),
    (-10, (146.5, 189.25, 209.62)),
    (-8,  (187.13, 213.38, 226.38)),
    (-6,  (224.25, 230.12, 232.88)),
    (-4,  (255, 255, 255)),  # white
    (0,   (255, 255, 255)),  # white
    (4,   (255, 255, 255)),
    (6,   (238, 221.12, 211.25)),
    (8,   (230.38, 196.75, 176.75)),
    (10,  (219.62, 171.25, 142.87)),
    (12,  (209.88, 147.75, 111.63)),
    (14,  (200.12, 124.25, 81.25)),
    (16,  (190, 101.75, 52.125)),
    (18,  (174.25, 75.25, 23.25)),
    (20,  (147.63, 46.75, 6)),  
]
rgb_list = [np.array(rgb) / 255.0 for val, rgb in cpt_data]
vik44 = ListedColormap(rgb_list, name="vik44")
vik44=vik44.reversed()

i=0
#read file
profile=xr.open_dataset("profile_grd"+chr(ord('A') + i)+".nc")
p_vpt=profile['z']
p_x=profile['x']
p_y=profile['y']
track_df=pd.read_csv("track_df"+chr(ord('A') + i)+".csv")
p_seis=pd.read_csv("profile_seis"+chr(ord('A') + i)+".csv")

#plot
fig1=plt.figure(figsize=(15,10),dpi=700)
ax1=fig1.add_subplot(1,1,1)
ax1.set_aspect(1)
#plot topo
ax1.fill([0,max(track_df.p),max(track_df.p),0],[-4000/350,-4000/350,0,0],c='lightblue') #sea
topo_x=np.array(track_df.p)
topo_y=np.array((track_df.elevation/-350)-4000/350)
topo_x=np.append(topo_x,0)
topo_y=np.append(topo_y,0)
for ii in range(len(topo_x)):
    if (topo_y[ii]>0):
        topo_y[ii]=0
ax1.plot(topo_x,topo_y,c='k')
ax1.fill(topo_x,topo_y,color='lightgray') #topo
#plot vpt
vpt_levels=np.arange(-20,20.1,1)
vpt_ticks=np.arange(-20,20.1,5)
vpt_label="velocity perturbation (%)"
fig1_vpt=ax1.contourf(p_x,p_y,p_vpt,vpt_levels,cmap=vik44,vmin=-20,vmax=20,extend='both')
#colorbar
cbar_vpt=fig1.colorbar(fig1_vpt,orientation='vertical',label=vpt_label,location='right',shrink=0.4,pad=1e-2)
ax = cbar_vpt.ax
text = ax.yaxis.label
font16 = font_manager.FontProperties(family='times new roman',size=12)
text.set_font_properties(font16)
font10 = font_manager.FontProperties(family='times new roman',size=10)
cbar_vpt.ax.set_yticklabels(vpt_ticks,fontproperties=font10)
#plot seis
ax1.plot(p_seis['0'],p_seis['1'],lw=0,marker='o',ms=0.2,c='k')


#fig axis
ax1.set_ylabel("Depth (km)              ",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.text(-18,1,"Elevation (m)",rotation='vertical',fontdict={"name": "Times New Roman"},fontsize=15)
ax1.set_ylim(50,-20)
topo_yticks=(np.array([-2000,0,2000])/-350)-4000/350
ax1.set_yticks(ticks=np.append(np.arange(50,-1,-10),topo_yticks))
ax1.set_yticklabels(np.append(np.arange(50,-1,-10),[-2000,0,2000]),fontdict={"name": "Times New Roman"},fontsize=14)
ax1.set_xlabel("Distance (km)",fontdict={"name": "Times New Roman"},fontsize=20)
ax1.set_xlim(min(track_df.p),max(track_df.p))
ax1.set_xticks(ticks=np.arange(min(track_df.p),max(track_df.p),50))
ax1.set_xticklabels(np.arange(min(track_df.p),max(track_df.p),50),fontdict={"name": "Times New Roman"},fontsize=14)
'''
fig_tmpr=ax.contour(xmesh-zmin_xlist[-1],zmesh,tmpr,\
                    levels=tmpr_levels_even,cmap='OrRd',\
                             linewidths=1)
tmpr_ticks=np.arange(0,500+0.001,100)
tmpr_label="Temperature ($^{o}$C)"
cbar_tmpr=fig1.colorbar(fig_tmpr,ticks=tmpr_ticks,label=tmpr_label
'''




















