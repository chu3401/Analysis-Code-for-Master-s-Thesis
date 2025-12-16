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

region_map = [140, 155, 10, 25]

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
fig.grdimage(grid=grid_map, cmap="oleron", shading=shade)

# Add a colorbar for the elevation
fig.colorbar(
    # Place the colorbar inside the plot (lowercase "j") in the Bottom Right (BR)
    # corner with an offset ("+o") of 0.7 centimeters and 0.3 centimeters in x or y
    # directions, respectively; move the x label above the horizontal colorbar ("+ml")
    position="jBR+o0.5c/0.45c+h+w5c/0.3c+ml",
    # Add a box around the colobar with a fill ("+g") in "white" color and a
    # transparency ("@") of 30 % and with a 0.8-points thick, black, outline ("+p")
    box="+gwhite@30+p0.8p,black",
    # Add x and y labels ("+l")
    frame=["x+lElevation", "y+lm"],
)

# Choose a survey line

liney_st=np.arange(15,20.1,2.5)
linex_st=np.full(len(liney_st),141)
linex_ed=np.full(len(liney_st),154)
liney=np.vstack((liney_st,liney_st)).T
linex=np.vstack((linex_st,linex_ed)).T
#22

for i in range(len(linex)):
    fig.plot(
        x=linex[i],  # Longitude in degrees East
        y=liney[i],  # Latitude in degrees North
        # Draw a 2-points thick, red, dashed line for the survey line
        pen="2p,red,dashed"
    )
    
    # Add labels "A" and "B" for the start and end points of the survey line
    
    fig.text(
        x=linex[i], 
        y=liney[i]+0.02,
        text=[chr(ord('A') + i), chr(ord('A') + i)+"'"],
        offset="0c/0.2c",  # Move text 0.2 centimeters up (y direction)
        font="15p"  # Use a font size of 15 points
    )


# ----------------------------------------------------------------------------
# Right: Vp perturbation
fig.shift_origin(xshift="w+2.5c")

for i in range(len(linex)):#
    track_df = pygmt.project(
        center=[linex[i,0], liney[i,0]],  # Start point of survey line (longitude, latitude)
        endpoint=[linex[i,1], liney[i,1]],  # End point of survey line (longitude, latitude)
        generate=1,  # Output data in steps of 1 km
        unit=True,
    )
    track_dis=track_df["p"].max()

    # ----------------------------------------------------------------------------
    # Top: Elevation along survey line
    
    fig.basemap(
        region=[0, track_dis, -10000, 500],  # x_min, x_max, y_min, y_max
        # Cartesian projection with a width of 12 centimeters and a height of 3 centimeters
        projection="x0.01c/0.0002c",
        # Add annotations ("a") and ticks ("f") as well as labels ("+l") at the west or
        # left and south or bottom sides ("WSrt")
        frame=["WSrt", "xa100f100+lDistance (km)", "ya2500+lElevation (m)"],
    )

    # Add labels "A" and "B" for the start and end points of the survey line
    fig.text(
        x=[0, track_dis],
        y=[1200, 1200],
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
        close="+y-10000",  # Force closed polygon
    )
    
    # Plot elevation along the survey line
    fig.plot(
        x=track_df.p,
        y=track_df.elevation,
        fill="gray",  # Fill the polygon in "gray"
        # Draw a 1-point thick, black, solid outline
        pen="1p,black,solid",
        close="+y-10000",  # Force closed polygon
    )
    fig.shift_origin(yshift="h+1c")








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





