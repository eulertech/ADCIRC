# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:14:55 2016

@author: liang.kuang
"""

from ADCIRC.Grid.Plot_Grid import plot_grid
from ADCIRC.Grid.Read_Grid import read_grid
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

from ADCIRC.Data.Get_Harmonics_COOPS import get_ha
myGrid= read_grid(r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA07\fort.14")
estofs_pacific_grid = read_grid(r'R:\Projects\ESTOFS_for_Micronesia\Grid\ESTOFS_Pacific\estofs-pac.fort.14')
plot_grid(estofs_pacific_grid)

#
lat = [13.449388,
13.424384,
7.349525 ,
8.731548 ,
15.230230,
18.873332,
7.329697 ,
3.969614 ,
11.541603,
19.190176,
7.024590 ,
7.374270 ,
12.906077]

lon = [144.654394,
144.797866,
151.483199,
167.745876,
145.728086,
166.511164,
134.458232,
146.696721,
154.540181,
155.769250,
158.230432,
151.999001,
132.385197
]
fig1 = plt.figure(1, figsize=(8,4),dpi = 200)
fig1.clf()
fig1.add_axes([0.1,0.1,0.8,0.8])

m = Basemap(projection = 'ortho',lat_1=0,lat_2=23.5, lat_0=13, lon_0 = 170, resolution = 'l', area_thresh=1000.0)
m.drawcoastlines()
#    m.bluemarble()
#    m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua',alpha=0.5)
m.drawparallels(np.arange(-90.,120.,30.))
m.drawmeridians(np.arange(0.,360.,60.))
plt.gca().set_aspect('equal') 
x_OBC,y_OBC = m(myGrid.obc_locations[:,0], myGrid.obc_locations[:,1])
m.plot(x_OBC,y_OBC)
x_OBC2,y_OBC2 = m(estofs_pacific_grid.obc_locations[:,0], estofs_pacific_grid.obc_locations[:,1])
m.plot(x_OBC2,y_OBC2)

lon = np.asarray(lon)
lat= np.asarray(lat)
xlon, ylat = m(lon,lat)
m.scatter(xlon[0:7],ylat[0:7],8,marker='o', color='r',label='COOPS Tidal Station') 
m.scatter(xlon[6:],ylat[6:],8,marker='<',color='g', label = 'DART')
leg = plt.legend(fontsize=8)
leg.draggable()
plt.title("Historical and active tide stations",fontsize=8)
plt.savefig(r"R:\Projects\ESTOFS_for_Micronesia\Data\co_ops\NOAA_Tidal_Stations_Pacific.png",dpi=400)
stationID = 1890000
HA = get_ha()