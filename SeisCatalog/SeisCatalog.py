# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:36:50 2025

@author: C
"""
from __future__ import print_function
import sys, os
import zlib, base64, glob
import matplotlib.pyplot as plt
import numpy as np

def interpolation(min_,max_,i,length):
    ii=length*((i-min_)/(max_-min_))
    return ii
def vtp_header(f, npoints):
    f.write(
'''<?xml version="1.0"?>
<VTKFile type="PolyData" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">
<PolyData>
<FieldData>
</FieldData>
<Piece NumberOfPoints="{0}">
'''.format(npoints))
    return


def vtp_footer(f):
    f.write(
'''</Piece>
</PolyData>
</VTKFile>
''')
    return


def vts_dataarray(f, data, data_name=None, data_comps=None):
    if data.dtype in (int, np.int32, np.int_):
        dtype = 'Int32'
    elif data.dtype in (float, np.single, np.double, np.float,
                        np.float32, np.float64):
        dtype = 'Float32'
    else:
        raise Error('Unknown data type: ' + name)

    name = ''
    if data_name:
        name = 'Name="{0}"'.format(data_name)

    ncomp = ''
    if data_comps:
        ncomp = 'NumberOfComponents="{0}"'.format(data_comps)

    if output_in_binary:
        fmt = 'binary'
    else:
        fmt = 'ascii'
    header = '<DataArray type="{0}" {1} {2} format="{3}">\n'.format(
        dtype, name, ncomp, fmt)
    f.write(header)

    if output_in_binary:
        header = np.zeros(4, dtype=np.int32)
        header[0] = 1
        a = data.tostring()
        header[1] = len(a)
        header[2] = len(a)
        b = zlib.compress(a)
        header[3] = len(b)
        f.write(base64.standard_b64encode(header).decode('ascii'))
        f.write(base64.standard_b64encode(b).decode('ascii'))
    else:
        data.tofile(f, sep=' ')
    f.write('\n</DataArray>\n')
    return
len_lon=621.53
len_lat=533.71


f1=open("GDMScatalog2003_2010.txt",'r')
data1=f1.readlines()
del data1[0]
f2=open("GDMScatalog2011_2013.txt",'r')
data2=f2.readlines()
del data2[0]
f3=open("GDMScatalog2014_2016.txt",'r')
data3=f3.readlines()
del data3[0]
f4=open("GDMScatalog2017_2020.txt",'r')
data4=f4.readlines()
del data4[0]
f5=open("GDMScatalog2021_2025.txt",'r')
data5=f5.readlines()
del data5[0]
f6=open("GDMScatalogLat20_22.5.txt",'r')
data6=f6.readlines()
del data6[0]
f7=open("GDMScatalog2003_2010_Lon120.txt",'r')
data7=f7.readlines()
del data7[0]
f8=open("GDMScatalog2011_2016_Lon120.txt",'r')
data8=f8.readlines()
del data8[0]
f9=open("GDMScatalog2017_2021_Lon120.txt",'r')
data9=f9.readlines()
del data9[0]
f0=open("GDMScatalog2022_2025_Lon120.txt",'r')
data0=f0.readlines()
del data0[0]

data=data1+data2+data3+data4+data5+data6+data7+data8+data9+data0
#big1=0
fff=open('SeisCatalog2003_2025_1up.dat','w')
for i in range(len(data)):
    data[i]=data[i].split()
    if (float(data[i][5])>=1):
        fff.write(str(data[i][3])+' '+str(data[i][2])+' '+str(data[i][4])+'\n')
    #data[i][3]=float(data[i][3])
    #if (data[i][3]>big1):
    #    big1=data[i][3]
fff.close()


catalog=np.zeros((len(data),5), dtype=np.float32)
for i in range(len(data)):
    data[i]=data[i].split()
    catalog[i,0]=interpolation(119,125,float(data[i][3]),len_lon) #lon
    catalog[i,1]=interpolation(21.3,26.1,float(data[i][2]),len_lat) #lat
    catalog[i,2]=data[i][4] #depth
    catalog[i,3]=data[i][5] #mag
    
    data[i][0]=data[i][0].split('-')
    catalog[i,4]=data[i][0][0] #year



nmarkers=len(catalog)
output_in_binary = True


fvtp = open('SeisCatalog_01.vtp', 'w')
vtp_header(fvtp, nmarkers)

# point-based data
fvtp.write('  <PointData>\n')
vts_dataarray(fvtp, catalog[:,2], 'Depth', 1)
vts_dataarray(fvtp, catalog[:,3], 'Mag.', 1)
vts_dataarray(fvtp, catalog[:,4], 'Year', 1)
fvtp.write('  </PointData>\n')

# point coordinates

# VTK requires vector field (velocity, coordinate) has 3 components.
# Allocating a 3-vector tmp array for VTK data output.
tmp = np.zeros((nmarkers, 3), dtype=np.float32)
tmp[:,0] = catalog[:,0]
tmp[:,1] = catalog[:,1]
tmp[:,2] = catalog[:,2]
fvtp.write('  <Points>\n')
vts_dataarray(fvtp, tmp, '', 3)
fvtp.write('  </Points>\n')

vtp_footer(fvtp)
fvtp.close()


'''
fig1=plt.figure(figsize=(11,10),dpi=1000)
ax1=fig1.add_subplot(1,1,1)
ax1.set_aspect(1)
ax1.plot(sealine[:,0],sealine[:,1],marker='o',ms=1,lw=0)
#ax1.set_xlim(119,125)
#ax1.set_ylim(21.3,26.1)
'''