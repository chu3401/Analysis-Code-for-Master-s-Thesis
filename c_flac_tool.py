# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 17:59:31 2024

@author: chu34
"""


import os
import flac
import numpy as np
import colorsys

class local_marker_tracing(object):
    def __init__(self):
        self.fl=flac.Flac()
        self.flac_interpolate()
        
    def read_data(self,title,path,column_index):
        temp1=np.loadtxt(path+"/"+title+".txt")
        #temp2=temp1[:,(column_index-1)]
        return temp1
        
    def findID(self,t,x1,x2,y1,y2,itype,interval):
        mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
        dx,dz,phase=self.flac_interpolate.interpolate(t, 'phase',x1-10,x2+10)
        xmesh,zmesh=self.fl.read_mesh(t)
        
        xline_x=np.array(())
        xline_z=np.array(())
        xline_p=np.array(())
        xline_ID=np.array(())
        xline=np.arange(x1,x2+1,interval)
        
        if (itype == 1): 
        # marker parallel to the surface
        # y1 decide how deep of marker
            for i in range(len(xline)):
                length0=10
                y_mark=np.interp(xline[i],xmesh[:,0],zmesh[:,0])+y1
                for m in range(len(mx)):    
                    length=((xline[i]-mx[m])**2+(y_mark-mz[m])**2)**0.5
                    if (length<length0):
                        length0=length
                        #xxx=mx[m]
                        zzz=mz[m]
                        #ppp=mphase[m]  
                m_p=np.where(mz==zzz)
                #print(mID[m_p],len(xline_ID),zzz,"length =",length0)
                xline_ID=np.append(xline_ID,mID[m_p])
        elif (itype == 2):
        # all marker in the square which you decide
        # x1,x2,y1,y2 decide the size of square
            for i in range(len(mx)):
                if (x1<mx[i]<x2 and y1>mz[i]>y2):
                    xline_ID=np.append(xline_ID,mID[i])
        elif (itype == 3):
        # choose marker in the horizon line    
        # y1 decide how deep of marker        
            for i in range(len(xline)):
                length0=10
                for m in range(len(mx)):    
                    length=((xline[i]-mx[m])**2+(y1-mz[m])**2)**0.5
                    if (length<length0):
                        length0=length
                        xxx=mx[m]
                        zzz=mz[m]
                        ppp=mphase[m]
                xline_x=np.append(xline_x,xxx)
                xline_z=np.append(xline_z,zzz)
                xline_p=np.append(xline_p,ppp)
                
                m_p=np.where(mz==zzz)
                #print(mID[m_p],len(xline_ID),zzz,"length =",length0)
                xline_ID=np.append(xline_ID,mID[m_p])
            
        return xline_ID
    
    def marker_tracing(self,t_st,t_ed,var,line_ID):
        func_name = f"read_{var}"
        tracing_array = np.array([])
        tracing_id_array = np.array([])
        x,z = self.fl_read_mesh(t_st)
        for t in range(t_st, t_ed+1):
            tracing_a = np.array([])
            tracing_id = np.array([])
            mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
            array = getattr(self.fl,func_name)
            nz=len(array[0,:])
            if (nz == len(x[0,:])):
                marr=self.flac.marker_interpolate_node(ntriag, ma1, ma2, nz, array)
            else:
                marr=self.flac.marker_interpolate_elem(ntriag, nz, array)
                
            for i in range(len(line_ID)):
                m_p=np.where(mID==line_ID[i])
                if (len(m_p[0])==0):
                    tracing_a = np.append(tracing_a,np.nan)
                    tracing_id = np.append(tracing_id,np.nan)
                    continue
                m_p=m_p[0][0]
                tracing_a=np.append(tracing_a, marr[m_p])
                tracing_id=np.append(tracing_id,mID[m_p])
            if (t==t_st):
                tracing_array=tracing_a
                tracing_id_array=tracing_id
                continue
            tracing_array=np.vstack((tracing_array,tracing_a))
            tracing_id_array=np.vstack((tracing_id_array,tracing_id))
        np.save("tracing_array",tracing_array)
        np.save("tracing_id_array",tracing_id_array)
        
class MarkerTracing_time(object):
    def __init__(self):      
        self.fl=flac.Flac()

    def place(self,marker_ID,t_st,t_ed):
        marker_x=np.array([])
        marker_z=np.array([])
        for t in range(t_st,t_ed+1):
            mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
            m_p=np.where(mID==marker_ID)
            if (len(m_p[0])==0):
                marker_x=np.append(marker_x,np.nan)
                marker_z=np.append(marker_z,np.nan)
                continue
            m_p=m_p[0][0]
            marker_x=np.append(marker_x,mx[m_p])
            marker_z=np.append(marker_z,mz[m_p])
        return marker_x,marker_z
    def phase(self,marker_ID,t_st,t_ed):
        marker_phase=np.array([])
        for t in range(t_st,t_ed+1):
            mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
            m_p = np.where(mID==marker_ID)
            if (len(m_p[0])==0):
                marker_phase=np.append(marker_phase,np.nan)
                continue
            m_p = m_p[0][0]
            marker_phase=np.append(marker_phase,mphase[m_p])
        return marker_phase
    def tmpr(self,marker_ID,t_st,t_ed):
        marker_tmpr=np.array([])
        for t in range(t_st,t_ed+1):
            tmpr=self.fl.read_temperature(t)
            nz=len(tmpr[0,:])
            mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
            mtmpr=flac.marker_interpolate_node(ntriag, ma1, ma2, nz, tmpr)
            m_p = np.where(mID==marker_ID)
            if (len(m_p[0])==0):
                marker_tmpr=np.append(marker_tmpr,np.nan)
                continue
            m_p = m_p[0][0]
            marker_tmpr=np.append(marker_tmpr,mtmpr[m_p])
        return marker_tmpr
    def pres(self,marker_ID,t_st,t_ed):
        marker_pres=np.array([])
        for t in range(t_st,t_ed+1):
            pres=self.fl.read_pres(t)
            nz=len(pres[0,:])
            mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
            mpres=self.flac.marker_interpolate_elem(ntriag, nz, pres)
            m_p = np.where(mID==marker_ID)
            if (len(m_p[0])==0):
                marker_pres=np.append(marker_pres,np.nan)
                continue
            m_p = m_p[0][0]
            marker_pres=np.append(marker_pres,mpres[m_p])
        return marker_pres
class MarkerTracing_array(object):
    def __init__(self):
        self.fl=flac.Flac()
    def place(self,marker_array,t):
        marker_x=np.array([])
        marker_z=np.array([])
        mx, mz, m_age, mphase, mID, ma1, ma2, ntriag = self.fl.read_markers(t)
        for ID in marker_array:
            m_p=np.where(mID==ID)
            if (len(m_p[0])==0):
                marker_x=np.append(marker_x,np.nan)
                marker_z=np.append(marker_z,np.nan)
                continue
            m_p=m_p[0][0]
            marker_x=np.append(marker_x,mx[m_p])
            marker_z=np.append(marker_z,mz[m_p])
        return marker_x,marker_z
class Tect_line(object):
    def __init__(self,path):
        self.path=path
    def TCline(self,file_name):
        file_path=os.path.join(self.path,file_name)
        line=np.loadtxt(file_path)
        return line

        
  
def hsv2rgb(hsv_number):
    rgb_array=colorsys.hsv_to_rgb(hsv_number, 1, 1)
    return rgb_array    
def make_rgb_array(n_color):
    hsv_array=np.linspace(0,0.8,n_color)
    rgb_array=[]
    for i in range(len(hsv_array)):
        rgb_color=hsv2rgb(hsv_array[i])
        rgb_array.append(rgb_color)
    return rgb_array
   
def topo_max(x,z,p,sr):
    max_z=max(z[p-sr:p,0])
    p=np.where(z[:,0]==max_z)
    p = p[0][0]
    return p
def topomax_xID(t,t_st,x,z,sr,max_zp):
    if (t==t_st and t>3):
        max_z=max(z[:,0])
        max_zp=np.where(z[:,0]==max_z)
        max_zp = max_zp[0][0]
    elif (t==3):
        fl = flac.Flac()
        phase=fl.read_phase(t)
        for i in range(len(phase)-1,-1,-1):
            if (phase[i,0]==11):
                break
        max_z=max(z[i-sr:i,0])
        max_zp=np.where(z[:,0]==max_z)
        max_zp = max_zp[0][0]
    elif (t<3):
        print("error : t<3")
    else :
        max_zp=topo_max(x, z, max_zp, sr)
    return max_zp

def t2time(t):
    time=round((t-1)*0.1,1)
    return time
def smooth_2d_array(array,n):
    for k in range(n):
        for i in range(1,len(array)-1):
            for j in range(1,len(array[0,:])-1):
                array[i,j]=(array[i-1,j-1]+array[i,j-1]+array[i+1,j-1]+\
                    array[i-1,j]+array[i,j]+array[i+1,j]+\
                        array[i-1,j+1]+array[i,j+1]+array[i+1,j+1])/9
    return array
def smooth_2d_array_surf(array,n,surf_weight):
    down=(1-surf_weight)/3
    up=surf_weight/3
    for k in range(n):
        for i in range(1,len(array)-1):
            for j in range(0,len(array[0,:])-1):
                if (j==0):
                    array[i,j]=(array[i-1,j]*up+array[i,j]*up+array[i+1,j]*up\
                            +array[i-1,j+1]*down+array[i,j+1]*down+array[i+1,j+1]*down)
                else:
                    array[i,j]=(array[i-1,j-1]+array[i,j-1]+array[i+1,j-1]+\
                        array[i-1,j]+array[i,j]+array[i+1,j]+\
                            array[i-1,j+1]+array[i,j+1]+array[i+1,j+1])/9
    return array
def smooth_1d_array(array,n):
    first_non_nan_index = np.where(~np.isnan(array))[0][0]
    #print(first_non_nan_index)
    for i in range(n):
        for j in range(first_non_nan_index+1,len(array)-1):
            array[j]=array[j-1]*0.25+array[j]*0.5+array[j+1]*0.25
    return array
def node2ele(node_array):
    ele_array=np.zeros([len(node_array)-1,len(node_array[0,:])-1])
    for i in range(len(node_array)-1):
        for j in range(len(node_array[0,:])-1):
            ele_array[i,j]=(node_array[i,j]+node_array[i+1,j]+node_array[i,j+1]+node_array[i+1,j+1])*0.25 
    return ele_array


    

if __name__ == '__main__':
    print("exe in here")











