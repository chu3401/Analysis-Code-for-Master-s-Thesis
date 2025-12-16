# -*- coding: utf-8 -*-


"""
Created on Thu Mar 13 09:38:55 2025

@author: C
"""

import pygmt
import numpy as np
import pandas as pd
import os
import matplotlib.font_manager as font_manager

region_map = [120.25, 122, 21.75, 24.25]

# Create a new pygmt.Figure instance
fig = pygmt.Figure()

# ----------------------------------------------------------------------------
# Bottom: Map of elevation in study area

# Set up basic map using a Mercator projection with a width of 12 centimeters
fig.basemap(region=region_map, projection="M12c", frame="af")

# Download grid for Earth relief with a resolution of 10 arc-minutes and gridline
# registration [Default]
grid_map = pygmt.datasets.load_earth_relief(resolution="15s", region=region_map)
shade = pygmt.grdgradient(grid_map,azimuth=45)

# Plot the downloaded grid with color-coding based on the elevation
fig.grdimage(grid=grid_map, cmap="geo", shading=shade)

# Add a colorbar for the elevation
fig.colorbar(
    # Place the colorbar inside the plot (lowercase "j") in the Bottom Right (BR)
    # corner with an offset ("+o") of 0.7 centimeters and 0.3 centimeters in x or y
    # directions, respectively; move the x label above the horizontal colorbar ("+ml")
    position="jBR+o1c/0.3c+v+w5c/0.3c+ml",
    # Add a box around the colobar with a fill ("+g") in "white" color and a
    # transparency ("@") of 30 % and with a 0.8-points thick, black, outline ("+p")
    box="+gwhite@30+p0.8p,black",
    # Add x and y labels ("+l")
    frame=["x+lElevation", "y+lm"],
)

Fault_folder="D:\script\Faults"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red,dashed",style="f0.5c/0.1c+l+t",fill='red')
    elif '33' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red",style="f0.5c/0.1c+r+t+o0.15",fill='red')
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red",style="f0.5c/0.1c+l+t+o0.15",fill='red')
        
Fault_folder="D:\script\Faults\RyukyuTrench"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red")
    if 'RF_RykyuTrench.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+t+i",fill='red') 
    elif 'NF01.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+i",fill='red')
    elif 'NF_infered03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.3c/0.1c+r+o0.1+i",fill='red')
    elif 'NF_infered04.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.3c/0.1c+r+i",fill='red')
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'NF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.2c+l+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+l+s45+o0.35c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+r+s45+o0.35c+i",fill='red')
    
Fault_folder="D:\script\Faults\PSP"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red")    
    if 'RF03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+o0.25c+i",fill='red') 
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+t+o0.25c+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+l+s45+o0.25c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+r+s45+o0.25c+i",fill='red')
    
    
Fault_folder="D:\script\Faults\WestTaiwan"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.9p,red")
    if 'ManilaTrench.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+t+i",fill='red') 
    elif 'DeformationFront_infered.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+t+i",fill='red')
    elif 'RF01.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF02.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF_infered02.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF_infered03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF_infered04.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF_infered06.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF05.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF11.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF13.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+t+i",fill='red')
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+t+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+l+s45+o0.25c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.2c+r+s45+o0.25c+i",fill='red')
    elif 'NF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+i",fill='red')

fig.show()
'''
import matplotlib.pyplot as plt
vpt_levels=np.linspace(-20,20,21)
vpt_ticks=np.linspace(-20,20,5)
fig1=plt.figure(figsize=(10,5),dpi=500)
ax1=fig1.add_subplot(1,1,1)
ax1.set_aspect(1)
fig1_vpt=ax1.contourf(profile_dis.T,profile_dep.T,profile_vpt,levels=vpt_levels,cmap='coolwarm_r',alpha=1,extend='both')
ax1.set_ylim(50,0)
ax1.set_xlabel("Distance (km)",fontdict={"name": "Times New Roman"},fontsize=12)
ax1.set_xticks(ticks=np.linspace(0,200,9))
ax1.set_xticklabels(np.linspace(0,200,9),fontdict={"name": "Times New Roman"},fontsize=10)
ax1.set_ylabel("Depth (km)",fontdict={"name": "Times New Roman"},fontsize=12)
ax1.set_yticks(ticks=np.linspace(50,0,6))
ax1.set_yticklabels(np.linspace(50,0,6),fontdict={"name": "Times New Roman"},fontsize=10)


vpt_label="Vp perturbation (%)"
cbar_vpt=fig1.colorbar(fig1_vpt,ticks=vpt_ticks,label=vpt_label,orientation='vertical',pad=0.03,shrink=0.4)

#cbar_vpt.ax.set_aspect(0.001)
ax = cbar_vpt.ax
text = ax.yaxis.label
font16 = font_manager.FontProperties(family='times new roman',size=12)
text.set_font_properties(font16)
font10 = font_manager.FontProperties(family='times new roman',size=10)
cbar_vpt.ax.set_yticklabels(vpt_ticks, fontproperties=font10)

'''





