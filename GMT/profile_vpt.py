# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:33:05 2025

@author: C
"""

import pygmt
import numpy as np
import pandas as pd
import os
import matplotlib.font_manager as font_manager
import xarray as xr

liney_st=np.array([22.4,23.2,23.8,24])
linex_st=np.full(len(liney_st),120)
linex_ed=np.full(len(liney_st),122.1)
liney=np.vstack((liney_st,liney_st)).T
linex=np.vstack((linex_st,linex_ed)).T


fig = pygmt.Figure()
region_map = [119.5, 122.5, 20, 25.5]
# Set up basic map using a Mercator projection with a width of 12 centimeters
#fig.basemap(region=region_map, projection="M12c", frame="af")

# Download grid for Earth relief with a resolution of 10 arc-minutes and gridline
# registration [Default]
grid_map = pygmt.datasets.load_earth_relief(resolution="15s", region=region_map)
# Right: Vp perturbation
#vik=pygmt.makecpt(series=[-20,20,2], cmap="vik",reverse=True,output="vik00.cpt")
vik=pygmt.makecpt(cmap="vik44.cpt",reverse=True)

from scipy.interpolate import RegularGridInterpolator
v_model=np.loadtxt('Huang2014.xyz')
gridx = v_model[:, 0].reshape(76, 61, 27)
gridy = v_model[:, 1].reshape(76, 61, 27)
gridz = v_model[:, 2].reshape(76, 61, 27)
gridvp = v_model[:, 3].reshape(76, 61, 27)
gridvpt = v_model[:, 4].reshape(76, 61, 27)
profile_z=np.linspace(0,50,51)

xx = gridx[:, 0, 0]
yy = gridy[0, :, 0]
zz = gridz[0, 0, :]
interp_vp=RegularGridInterpolator((xx,yy,zz),gridvp)
interp_vpt=RegularGridInterpolator((xx,yy,zz),gridvpt)


for i in range(len(linex)):#
    track_df = pygmt.project(
        center=[linex[i,0], liney[i,0]],  # Start point of survey line (longitude, latitude)
        endpoint=[linex[i,1], liney[i,1]],  # End point of survey line (longitude, latitude)
        generate=1,  # Output data in steps of 1 km
        unit=True,
    )
    track_dis=track_df["p"].max()

    track_lon=np.linspace(min(track_df.r),max(track_df.r),len(track_df.r))
    track_lat=np.linspace(min(track_df.s),max(track_df.s),len(track_df.s))
    track_dist=np.linspace(min(track_df.p),max(track_df.p),len(track_df.p))
    xxx, zzz = np.meshgrid(track_lon, profile_z)
    yyy, zzz = np.meshgrid(track_lat, profile_z)

    profile_vp=interp_vp((xxx,yyy,zzz))
    profile_vpt=interp_vpt((xxx,yyy,zzz))
    
    profile_dis, profile_dep = np.meshgrid(track_dist,profile_z)
    profile_grd = pygmt.xyz2grd(x=profile_dis.flatten(),y=profile_dep.flatten(),\
                            z=profile_vp.flatten(),\
                                spacing=(track_dist[1]-track_dist[0],profile_z[1]-profile_z[0]),\
                                region=[np.min(profile_dis),np.max(profile_dis),np.min(profile_dep),np.max(profile_dep)])
    profile_grd = profile_grd.fillna(0)
    print(type(profile_grd))
    print(np.min(profile_dis),np.max(profile_dis),np.min(profile_dep),np.max(profile_dep))
    print(track_dist[1]-track_dist[0],profile_z[1]-profile_z[0])
    
    fig.basemap(
        region=[0, track_dis, 0, 50],  # x_min, x_max, y_min, y_max
        # Cartesian projection with a width of 12 centimeters and a height of 3 centimeters
        projection="x0.075c/-0.075c",
        # Add annotations ("a") and ticks ("f") as well as labels ("+l") at the west or
        # left and south or bottom sides ("WSrt")
        frame=["WSrt", "xa50f50+lDistance (km)", "ya10+lDepth (km)"])

    fig.grdview(grid=profile_grd,cmap=vik,surftype='i')
    #print(linex[i,0], liney[i,0],linex[i,1], liney[i,1])
    profile_seis = pygmt.project(data='SeisCatalog2003_2025_2up.dat',
        center=[linex[i,0], liney[i,0]],  # Start point of survey line (longitude, latitude)
        endpoint=[linex[i,1], liney[i,1]],  # End point of survey line (longitude, latitude)
        unit=True,
        width=[-10,10],
        convention="pz",
    )
    
    fig.plot(profile_seis,style="c0.01c", pen="black",fill='black')
    
    # ----------------------------------------------------------------------------
    # Top: Elevation along survey line
    fig.shift_origin(yshift="h")
    fig.basemap(
        region=[0, track_dis, -2999, 4000],  # x_min, x_max, y_min, y_max
        # Cartesian projection with a width of 12 centimeters and a height of 3 centimeters
        projection="x0.075c/0.0002c",
        # Add annotations ("a") and ticks ("f") as well as labels ("+l") at the west or
        # left and south or bottom sides ("WSrt")
        frame=["Wrt", "x", "ya3000+lElevation (m)"],
    )

    # Add labels "A" and "B" for the start and end points of the survey line
    fig.text(
        x=[0, track_dis],
        y=[5000, 5000],
        text=[chr(ord('A') + i), chr(ord('A') + i)+"'"],
        no_clip=True,  # Do not clip text that fall outside the plot bounds
        font="10p",  # Use a font size of 10 points
    )
    # Extract the elevation at the generated points from the downloaded grid and add it as
    # new column "elevation" to the pandas.DataFrame
    track_df = pygmt.grdtrack(grid=grid_map, points=track_df, newcolname="elevation")
    
    # Plot water masses
    fig.plot(
        x=[0, track_dis],
        y=[0, 0],
        fill="lightblue",  # Fill the polygon in "lightblue"
        # Draw a 0.25-points thick, black, solid outline
        pen="0.25p,black,solid",
        close="+y-8000",  # Force closed polygon
    )
    
    # Plot elevation along the survey line
    fig.plot(
        x=track_df.p,
        y=track_df.elevation,
        fill="gray",  # Fill the polygon in "gray"
        # Draw a 1-point thick, black, solid outline
        pen="1p,black,solid",
        close="+y-8000",  # Force closed polygon
    )
    fig.colorbar(
        # Place the colorbar inside the plot (lowercase "j") in the Bottom Right (BR)
        # corner with an offset ("+o") of 0.7 centimeters and 0.3 centimeters in x or y
        # directions, respectively; move the x label above the horizontal colorbar ("+ml")
        position="jBR+o-0.8c/-3.7c+v+w5c/0.3c+ml",
        # Add a box around the colobar with a fill ("+g") in "white" color and a
        # transparency ("@") of 30 % and with a 0.8-points thick, black, outline ("+p")
        #box="+gwhite@30+p0.8p,black",
        # Add x and y labels ("+l")
        frame=["x+lvelocity perturbation (%)", "y"],
    )
    
    fig.shift_origin(yshift="h+2.5c")
    
    #save file
    profile_seis.to_csv("profile_seis"+chr(ord('A') + i)+".csv")
    profile_grd.to_netcdf("profile_grd"+chr(ord('A') + i)+".nc")









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