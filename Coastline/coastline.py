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


sealine=np.loadtxt("coastline_1.dat")

for i in range(len(sealine)):
    if (sealine[i,0]>125 or sealine[i,0]<119 or sealine[i,1]<21.3 or sealine[i,1]>26.1):
        #print("pass")
        continue
    sealine[i,0]=interpolation(119,125,sealine[i,0],len_lon)
    sealine[i,1]=interpolation(21.3,26.1,sealine[i,1],len_lat)

nmarkers=len(sealine)
output_in_binary = True


fvtp = open('coastline.vtp', 'w')
vtp_header(fvtp, nmarkers)

# point-based data
fvtp.write('  <PointData>\n')
a = np.zeros((nmarkers, 1), dtype=np.float32)
vts_dataarray(fvtp, a, '0', 1)
fvtp.write('  </PointData>\n')

# point coordinates

# VTK requires vector field (velocity, coordinate) has 3 components.
# Allocating a 3-vector tmp array for VTK data output.
tmp = np.zeros((nmarkers, 3), dtype=np.float32)
tmp[:,0] = sealine[:,0]
tmp[:,1] = sealine[:,1]
tmp[:,2] = -5
fvtp.write('  <Points>\n')
vts_dataarray(fvtp, tmp, '', 3)
fvtp.write('  </Points>\n')

vtp_footer(fvtp)
fvtp.close()



fig1=plt.figure(figsize=(11,10),dpi=1000)
ax1=fig1.add_subplot(1,1,1)
ax1.set_aspect(1)
ax1.plot(sealine[:,0],sealine[:,1],marker='o',ms=1,lw=0)
#ax1.set_xlim(119,125)
#ax1.set_ylim(21.3,26.1)