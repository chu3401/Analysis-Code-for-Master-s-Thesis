# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 15:44:08 2025

@author: C
"""
from __future__ import print_function
import scipy.interpolate as interp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

import sys,os
import zlib,base64,glob

def interpolation(min_,max_,i,length):
    ii=length*((i-min_)/(max_-min_))
    return ii

v_model=np.loadtxt('Huang2014.xyz')
len_lon=621.53
len_lat=533.71
minlon=min(v_model[:,0])
minlat=min(v_model[:,1])
maxlon=max(v_model[:,0])
maxlat=max(v_model[:,1])

print("longtitude")
print(min(v_model[:,0]),max(v_model[:,0]))
print("latitude")
print(min(v_model[:,1]),max(v_model[:,1]))


for i in range(len(v_model)):
    v_model[i,0]=interpolation(minlon,maxlon,v_model[i,0],len_lon)
    v_model[i,1]=interpolation(minlat,maxlat,v_model[i,1],len_lat)
np.savetxt("Huang2014_Ca.xyz",v_model)
v_model=np.loadtxt("Huang2014_Ca.xyz",dtype=np.float32)

'''
gridx=v_model[:,0].reshape(76,61,27)
gridy=v_model[:,1].reshape(76,61,27)
gridz=v_model[:,2].reshape(76,61,27)
gridvp=v_model[:,3].reshape(76,61,27)
gridvpt=v_model[:,4].reshape(76,61,27)
gridvpdws=v_model[:,5].reshape(76,61,27)

gridx=gridx[:,0,0]
gridy=gridy[0,:,0]
gridz=gridz[0,0,:]
'''
'''
gridx=np.linspace(0,len_lon,200)
gridy=np.linspace(0,len_lat,200)
gridz=np.linspace(-5,300,200)
gridx,gridy,gridz=np.meshgrid(gridx,gridy,gridz,indexing="ij")
gridvpt=interp.griddata((v_model[:,0],v_model[:,1],v_model[:,2]),v_model[:,4],(gridx,gridy,gridz),method="linear")
gridvp=interp.griddata((v_model[:,0],v_model[:,1],v_model[:,2]),v_model[:,3],(gridx,gridy,gridz),method="linear")
gridvpdws=interp.griddata((v_model[:,0],v_model[:,1],v_model[:,2]),v_model[:,5],(gridx,gridy,gridz),method="linear")
'''

def vts_header(f, nex, ney, nez):
    f.write(
'''<?xml version="1.0"?>
<VTKFile type="StructuredGrid" version="0.1" byte_order="LittleEndian" compressor="vtkZLibDataCompressor">
<StructuredGrid WholeExtent="0 {0} 0 {1} 0 {2}">
<FieldData>
</FieldData>
<Piece Extent="0 {0} 0 {1} 0 {2}">
'''.format(nex, ney, nez))
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
        a = data.tobytes()
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
def vts_footer(f):
    f.write(
'''</Piece>
</StructuredGrid>
</VTKFile>
''')
    return
output_in_binary = True

'''
np.save('gridx',gridx)
np.save('gridy',gridy)
np.save('gridz',gridz)
np.save('gridv',gridv)
'''

'''
gridx=np.load('gridx.npy')
gridy=np.load('gridy.npy')
gridz=np.load('gridz.npy')
gridvp=np.load('gridvp.npy')
gridvpt=np.load('gridvpt.npy')
gridvpdws=np.load('gridvpdws.npy')

print(np.max(gridvpt))
print(np.min(gridvpt))
'''
gridx=v_model[:,0].reshape(76,61,27)
gridy=v_model[:,1].reshape(76,61,27)
gridz=v_model[:,2].reshape(76,61,27)
gridvp=v_model[:,3].reshape(76,61,27)
gridvpt=v_model[:,4].reshape(76,61,27)
gridvpdws=v_model[:,5].reshape(76,61,27)
gridvs=v_model[:,6].reshape(76,61,27)
gridvst=v_model[:,7].reshape(76,61,27)
gridvsdws=v_model[:,8].reshape(76,61,27)
gridvpvs=v_model[:,9].reshape(76,61,27)
gridvpvst=v_model[:,10].reshape(76,61,27)

gridx=gridx[:,0,0]
gridy=gridy[0,:,0]
gridz=gridz[0,0,:]
gridx,gridy,gridz=np.meshgrid(gridx,gridy,gridz,indexing="ij")

print(np.max(gridvpt))
print(np.min(gridvpt))


fvts=open('Huang2014.vts','w')
vts_header(fvts,len(gridx)-1,len(gridx[0])-1,len(gridx[0,0])-1)


# element-based field
fvts.write('  <PointData>\n')
vts_dataarray(fvts,gridvp.swapaxes(0,2),'P-wave velocity')
vts_dataarray(fvts,gridvpt.swapaxes(0,2),'P-wave velocity perturbation')
vts_dataarray(fvts,gridvpdws.swapaxes(0,2),'derived weighted sum of P-wave')
vts_dataarray(fvts,gridvs.swapaxes(0,2),'S-wave velocity')
vts_dataarray(fvts,gridvst.swapaxes(0,2),'S-wave velocity perturbation')
vts_dataarray(fvts,gridvsdws.swapaxes(0,2),'derived weighted sum of S-wave')
vts_dataarray(fvts,gridvpvs.swapaxes(0,2),'Vp-Vs ratio')
vts_dataarray(fvts,gridvpvst.swapaxes(0,2),'Vp-Vs ratio perturbation')
fvts.write('  </PointData>\n')

tmp = np.zeros((len(gridx),len(gridx[0]),len(gridx[0,0]),3), dtype=np.float32)
tmp[:,:,:,0] = gridx
tmp[:,:,:,1] = gridy
tmp[:,:,:,2] = gridz
fvts.write('  <Points>\n')
tmp=tmp.swapaxes(0,2)
vts_dataarray(fvts,tmp,'',3)
fvts.write('  </Points>\n')

vts_footer(fvts)
fvts.close()





