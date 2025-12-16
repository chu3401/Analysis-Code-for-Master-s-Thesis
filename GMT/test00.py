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

region_map = [119.5, 122.5, 20, 25.5]
grid_map = pygmt.datasets.load_earth_relief(resolution="15s", region=region_map)
# Create a new pygmt.Figure instance
fig = pygmt.Figure()

# ----------------------------------------------------------------------------
# Bottom: Map of elevation in study area

# Set up basic map using a Mercator projection with a width of 12 centimeters

fig.basemap(region=region_map, projection="M12c", frame="af")
shade = pygmt.grdgradient(grid_map,azimuth=45)
fig.grdimage(grid=grid_map, cmap="geo", shading=shade)
# Add a colorbar for the elevation
fig.colorbar(
    # Place the colorbar inside the plot (lowercase "j") in the Bottom Right (BR)
    # corner with an offset ("+o") of 0.7 centimeters and 0.3 centimeters in x or y
    # directions, respectively; move the x label above the horizontal colorbar ("+ml")
    position="jBR+o6.5c/22.85c+h+w5c/0.3c+ml", #20,22.85 21,18.55??
    # Add a box around the colobar with a fill ("+g") in "white" color and a
    # transparency ("@") of 30 % and with a 0.8-points thick, black, outline ("+p")
    box="+gwhite@30+p0.8p,black",
    # Add x and y labels ("+l")
    frame=["x+lElevation", "y+lm"],
)

# Choose a survey line

liney_st=np.array([22.4,23.2,23.8,24])
linex_st=np.full(len(liney_st),120)
linex_ed=np.full(len(liney_st),122.1)
liney=np.vstack((liney_st,liney_st)).T
linex=np.vstack((linex_st,linex_ed)).T
#22
crx=np.array([])
cry=np.array([])
crp=np.array([])
for i in range(len(linex)):
    
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
    # Extract the elevation at the generated points from the downloaded grid and add it as
    # new column "elevation" to the pandas.DataFrame
    track_df = pygmt.grdtrack(grid=grid_map, points=track_df, newcolname="elevation")
    # Plot topo maximum
    topo_max_x=max(track_df.elevation)
    max_p=np.where(track_df.elevation==topo_max_x)
    if (len(max_p[0])==0):
        continue
    max_p=max_p[0][0]
    print(track_df.r[max_p],track_df.s[max_p])
    crx=np.append(crx,track_df.r[max_p])
    cry=np.append(cry,track_df.s[max_p])
    crp=np.append(crp,max_p)
    
    fig.plot(
        x=track_df.r[int(max_p-75):int(max_p+75)],  # Longitude in degrees East
        y=track_df.s[int(max_p-75):int(max_p+75)],  # Latitude in degrees North
        # Draw a 2-points thick, red, dashed line for the survey line
        pen="2p,red,dashed",
    )
    # Add labels "A" and "B" for the start and end points of the survey line
    fig.text(
        x=[track_df.r[int(max_p-75)],track_df.r[int(max_p+75)]], 
        y=[track_df.s[int(max_p-75)],track_df.s[int(max_p+75)]],
        text=[chr(ord('A') + i), chr(ord('A') + i)+"'"],
        offset="0c/0.2c",  # Move text 0.2 centimeters up (y direction)
        font="15p",  # Use a font size of 15 points
    )
    
    
fig.plot(
    x=crx,
    y=cry+2e-2,
    pen="1.5p",
    style="t0.3c",
    fill='red'
)
###topo track
'''
fig.shift_origin(xshift="w+2.5c")
for i in range(len(linex)):#
    
    # ----------------------------------------------------------------------------
    # Top: Elevation along survey line
    fig.basemap(
        region=[0, track_dis, -3000, 4000],  # x_min, x_max, y_min, y_max
        # Cartesian projection with a width of 12 centimeters and a height of 3 centimeters
        projection="x0.075c/0.0002c",
        # Add annotations ("a") and ticks ("f") as well as labels ("+l") at the west or
        # left and south or bottom sides ("WSrt")
        frame=["WSrt", "x", "ya2000+lElevation (m)"],
    )

    # Add labels "A" and "B" for the start and end points of the survey line
    fig.text(
        x=[0, track_dis],
        y=[5000, 5000],
        text=[chr(ord('A') + i), chr(ord('A') + i)+"'"],
        no_clip=True,  # Do not clip text that fall outside the plot bounds
        font="10p",  # Use a font size of 10 points
    )
    
    #track
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
    
    # Plot topo maximum
    topo_max_x=max(track_df.elevation)
    max_p=np.where(track_df.elevation==topo_max_x)
    if (len(max_p[0])==0):
        continue
    max_p=max_p[0][0]
    
    fig.plot(
        x=[track_df.p[max_p],track_df.p[max_p]],
        y=[topo_max_x,0],
        pen="1.5p",
        style="f1.5+r10+t1+p",
        fill='red'
    )
    fig.plot(
        x=[track_df.p[max_p]-75,track_df.p[max_p]+75],
        y=[topo_max_x,topo_max_x],
        pen="1.5p",
        style="f1.5+r10+t1+p",
        fill='red'
    )
    fig.shift_origin(yshift="h+1.5c")
    
    #save file
    track_df.to_csv("track_df"+chr(ord('A') + i)+".csv")
    np.save("crx", crx)
    np.save("cry", cry)
    np.save("crp", crp)
'''
'''
Fault_folder="D:\script\Faults"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red,dashed",style="f0.5c/0.05c+l+t")
    elif '33' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t",fill='red')
        
Fault_folder="D:\script\Faults\RyukyuTrench"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red")
    if 'RF_RykyuTrench.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t+i",fill='red') 
    elif 'NF01.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+i",fill='red')
    elif 'NF_infered03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.3c/0.1c+r+o0.1+i",fill='red')
    elif 'NF_infered04.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.3c/0.1c+r+i",fill='red')
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'NF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+l+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+l+s45+o0.25c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+r+s45+o0.25c+i",fill='red')
    
Fault_folder="D:\script\Faults\PSP"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)  # 依據你的資料格式調整 delimiter
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red")    
    if 'RF03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red') 
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+l+s45+o0.25c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+r+s45+o0.25c+i",fill='red')
    
    
Fault_folder="D:\script\Faults\WestTaiwan"
file_list = [f for f in os.listdir(Fault_folder) if f.endswith('.dat')]
for file_name in file_list:
    file_path = os.path.join(Fault_folder, file_name)
    data = np.loadtxt(file_path)
    if 'infered' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red,dashed")
    else:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red")
    if 'ManilaTrench.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t+i",fill='red') 
    elif 'DeformationFront_infered.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t+i",fill='red')
    elif 'RF01.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF02.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF_infered02.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF_infered03.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF_infered04.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF_infered06.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF05.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF11.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF13.dat' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+l+t+i",fill='red')
    elif 'RF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.05c+r+t+i",fill='red')
    elif 'LLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+l+s45+o0.25c+i",fill='red')
    elif 'RLF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.1p,red",style="f1c/0.1c+r+s45+o0.25c+i",fill='red')
    elif 'NF' in file_name:
        fig.plot(x=data[:,0],y=data[:,1],pen="0.5p,red",style="f0.5c/0.1c+r+i",fill='red')
'''
'''
# ----------------------------------------------------------------------------
# Right: Vp perturbation
fig.shift_origin(xshift="w+2.5c")
#vik=pygmt.makecpt(series=[-20,20,2], cmap="vik",reverse=True,output="vik00.cpt")
vik=pygmt.makecpt(cmap="vik44.cpt",reverse=True)

from scipy.interpolate import RegularGridInterpolator
v_model=np.loadtxt('Huang2014.xyz')
gridx = v_model[:, 0].reshape(76, 61, 27)
gridy = v_model[:, 1].reshape(76, 61, 27)
gridz = v_model[:, 2].reshape(76, 61, 27)
gridvpt = v_model[:, 4].reshape(76, 61, 27)
profile_z=np.linspace(0,50,51)

xx = gridx[:, 0, 0]
yy = gridy[0, :, 0]
zz = gridz[0, 0, :]
interp=RegularGridInterpolator((xx,yy,zz),gridvpt)


for i in range(6,9):#
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

    profile_vpt=interp((xxx,yyy,zzz))
    
    profile_dis, profile_dep = np.meshgrid(track_dist,profile_z)
    profile_grd = pygmt.xyz2grd(x=profile_dis.flatten(),y=profile_dep.flatten(),\
                            z=profile_vpt.flatten(),\
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
        region=[0, track_dis, -3000, 4000],  # x_min, x_max, y_min, y_max
        # Cartesian projection with a width of 12 centimeters and a height of 3 centimeters
        projection="x0.075c/0.0002c",
        # Add annotations ("a") and ticks ("f") as well as labels ("+l") at the west or
        # left and south or bottom sides ("WSrt")
        frame=["Wrt", "x", "ya2000+lElevation (m)"],
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
    fig.shift_origin(yshift="h+1.7c")

fig.colorbar(
    # Place the colorbar inside the plot (lowercase "j") in the Bottom Right (BR)
    # corner with an offset ("+o") of 0.7 centimeters and 0.3 centimeters in x or y
    # directions, respectively; move the x label above the horizontal colorbar ("+ml")
    position="jBR+o17.7c/-1.8c+h+w5c/0.3c+ml",
    # Add a box around the colobar with a fill ("+g") in "white" color and a
    # transparency ("@") of 30 % and with a 0.8-points thick, black, outline ("+p")
    box="+gwhite@30+p0.8p,black",
    # Add x and y labels ("+l")
    frame=["x+l%", "y"],
)

'''





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





