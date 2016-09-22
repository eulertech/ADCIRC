# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:30:55 2016

@author: liang.kuang
"""

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.mlab as mlab
import matplotlib 
import numpy as np
import scipy as sp
from mpl_toolkits.basemap import Basemap

#import matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import time
#matplotlib.style.use('ggplot')
fsize = 8
def plot_grid(myGrid):    
    startTime = time.clock()
    xy = sp.delete(myGrid.coordinates,2,1)  #remove third column
    triangles = myGrid.triangles-1  # adress python index from 0 issue
    depth = myGrid.coordinates[:,2]    
    temp = myGrid.lnd_locations;
    temp[temp==myGrid.missingData] = np.nan
    myGrid.lnd_locations = temp    
    
    temp = myGrid.obc_locations;
    temp[temp==myGrid.missingData] = np.nan
    myGrid.obc_locations = temp
    
    plt.close('all')
#    plt.hold(True)
    fig1 = plt.figure(1, figsize=(5,5),dpi = 200)
    fig1.clf()
    plt.gca().set_aspect('equal')
    #fig1.add_axes([0.1,0.1,0.8,0.8])

#    m = Basemap(projection = 'ortho', lat_0=13, lon_0 = 144, resolution = 'l', area_thresh=1000.0)
#    m.drawcoastlines()
#    m.bluemarble()
#    m.drawmapboundary(fill_color='aqua')
#    m.fillcontinents(color='coral',lake_color='aqua',alpha=0.5)
#    m.drawparallels(np.arange(-90.,120.,30.))
#    m.drawmeridians(np.arange(0.,360.,60.))
#    plt.gca().set_aspect('equal')
#    
#    x_OBC,y_OBC = m(myGrid.obc_locations[:,0], myGrid.obc_locations[:,1])
#    m.plot(x_OBC,y_OBC)
#    m.plot(myGrid.lnd_locations[:,0], myGrid.lnd_locations[:,1])
#    x,y = m(xy[:,0],xy[:,1])
#    plt.triplot(x,y,triangles,'g-',lw=0.03)    
    plt.plot(myGrid.obc_locations[:,0], myGrid.obc_locations[:,1],'g-',lw=0.3)
    plt.triplot(xy[:,0],xy[:,1],triangles,'g-',lw=0.3)    
    plt.title("ADCIRC Grid",fontsize=fsize)
    plt.xlabel('Longitude (degrees)',fontsize=fsize)
    plt.ylabel('Latitude (degrees)',fontsize=fsize)
#    fig1.tight_layout()
    plt.savefig('ADCIRC_Grid')
    
    fig2 = plt.figure(2, figsize = (5,5), dpi = 200)
    fig2.clf()
    plt.gca().set_aspect('equal')
#    plt.tricontour(xy[:,0],xy[:,1],depth,15,linewidths=0.5, colors='k')
#    plt.tricontourf(xy[:,0],xy[:,1],depth,15, cmap = plt.cm.jet,
#                    norm = plt.Normalize(vmax=abs(depth).max(), vmin = -abs(depth).max()))    
    plt.tripcolor(xy[:,0],xy[:,1],triangles, depth, edgecolors = 'none')
    plt.colorbar()                    
#    plt.xlim(130, 180);
#    plt.ylim(0,25);
    plt.xlabel('Longitude (degrees)',fontsize=fsize)
    plt.ylabel('Latitude (degrees)',fontsize=fsize)
    plt.title("Depth (m)", fontsize = fsize)
    fig2.tight_layout()

#    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    plt.show()

   # plt.setp(ax1.get_xticklabels(), rotation=0, fontisze = 8, visibile = True)
    plt.savefig('ADCIRC_Grid_Depth')
#    plt.savefig('ADCIRC_Grid', bbox_inches='tight',dpi = 400)
    
    elapsedTime = time.clock() - startTime
    print("Total elapsed time is %s !" %elapsedTime)
