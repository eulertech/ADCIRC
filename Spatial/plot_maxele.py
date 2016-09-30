# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:03:05 2016

@author: liang.kuang
"""

from ADCIRC.Grid.Read_Grid import read_grid
from ADCIRC.Spatial.read_maxele import read_maxele
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import os
import matplotlib.tri as tri  

def plot_maxele(gridFileName,maxeleFileName,grid = False,fontsize = 8):
    fsize = fontsize
    myGrid = read_grid(gridFileName)
    [index,maxele, indexTime, maxeleTime] = read_maxele(maxeleFileName)
    xy = sp.delete(myGrid.coordinates,2,1)  #remove third column
    triangles = myGrid.triangles-1  # adress python index from 0 issue 
    originalgrid_triang = tri.Triangulation(xy[:,0],xy[:,1],triangles=triangles,mask=None)
    plt.close('all')
#    plt.hold(True)
    fig1 = plt.figure(1, figsize=(5,5),dpi = 200)
    fig1.clf()
    plt.gca().set_aspect('equal')
    if(grid == True):
        plt.plot(myGrid.obc_locations[:,0], myGrid.obc_locations[:,1],'g-',lw=0.3)
        plt.triplot(xy[:,0],xy[:,1],triangles,'g-',lw=0.3)
    plt.tripcolor(originalgrid_triang, maxele, edgecolors = 'none',
                                    shading='flat',vmin=vminval,vmax=vmaxval,cmap=colormap) 
    #plt.tripcolor(xy[:,0],xy[:,1],triangles, depth, edgecolors = 'none')
    plt.colorbar()                    
#    plt.xlim(130, 180);
#    plt.ylim(0,25);
    plt.xlabel('Longitude (degrees)',fontsize=fsize)
    plt.ylabel('Latitude (degrees)',fontsize=fsize)
    plt.title("Maximum Elevation (m)", fontsize = fsize)
    fig1.tight_layout()
    picName = os.path.join(os.path.dirname(maxeleFileName),'max elevation.png')     
    plt.savefig(picName)     