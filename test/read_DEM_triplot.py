# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 10:53:00 2016
Code to analyse bathymetry data from Cuong (csv comma seprated)
1. Read DEM file (geoTIFF)
Read a raster file a numpy array with GDAL
@author: liang.kuang
"""
import timeit,time
import os, glob,sys 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ADCIRC.Grid.Read_Grid import read_grid
from ADCIRC.Grid.Plot_Grid import plot_grid
def mask_triagles(xy,triangles,boundsList):
    #return a index array for masking triangle array 
    from matplotlib.path import Path
    x = xy[:,0].flatten()
    y = xy[:,1].flatten()
    xmid = x[triangles].mean(axis=1)
    ymid = y[triangles].mean(axis=1)
    xy_tri=np.zeros([len(xmid),2])
    xy_tri[:,0] = xmid
    xy_tri[:,1] = ymid
    [xmin,ymax,xmax,ymin] = boundsList
    polygon = [[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]
    p = Path(polygon)
    index = p.contains_points(xy_tri)  # Logical values array
    mask = (1-index).astype(bool)  #mask the triangles outside the box
    #mask_array = np.transpose(np.tile(index,(3,1)))
#    triangle_in = np.reshape(triangles[mask_array],(-1,3))
    #triangles_masked =   np.ma.masked_array(triangles,mask=mask_array)
    return mask
    
def extract_gridpoints(grid,boundsList):
    #input: gridObj return from read_grid, boundlist=[ulx,uly,lrx,lry] =[xmin,ymax,xmax,ymin]
    #output: returns an 2D numpy array: nodes_in and 1D logical array: index
    from matplotlib.path import Path    
    [xmin,ymax,xmax,ymin] = boundsList
    polygon = [[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]
    p = Path(polygon)
    nodes = grid.coordinates[:,0:2] #get lon,lat only
    dep = grid.coordinates[:,2]
    index = p.contains_points(nodes)  # Logical values array
    mask_array = np.transpose(np.tile(index,(2,1)))
    #nodes_masked = np.ma.masked_array(nodes,mask = mask_array)    
    #mask = nodes_masked.mask
    #nodes_in = np.reshape(nodes[mask],(-1,2))
    nodes_in = np.reshape(nodes[mask_array],(-1,2))
    depths_in = dep[index] # might be a problem for NumPy 1.11 release 2016-08-19
#    xbounds = [xmin,xmax,xmax,xmin,xmin]
#    ybounds = [ymin,ymin,ymax,ymax,ymin]
    #plt.close('all')
#    plt.ax = plt.figure(num=100,figsize=(5,5),dpi=100)
#    plt.clf()
#    ax.plot(xbounds,ybounds,'k-')
#    ax.plot(nodes_in[:,0],nodes_in[:,1],'ro')
#    ax.set_title('Verifying the points are inside the DEM boundary')
    return nodes_in,index,depths_in
def merge_grid(original_grid, new_depth,index):
    import copy
    #input: gridObj, new_depth as nparray or list
    #output: new_grid object
    new_grid = copy.deepcopy(original_grid)
    xyz = new_grid.coordinates
    depth0 = np.ma.masked_array(xyz[:,2],mask=index)
    depth0[depth0.mask] = new_depth
    xyz[:,2] = depth0.data    
    new_grid.coordinates = xyz
    #nodeNums=np.asarray(np.arange(0,len(depth_original),1))
    #nodes_replace=nodeNum[index]
    return new_grid  #new grid per se
    
def map_dem_points(points,DEMdata,DEMinfo,depths_in,missingData = -999999.0):
    #input: points 2D array(lon,lat)
    #get the nearest (i,j) in DEM    
    # GDAL provids the top-left coordinate (lat, lon)
    ulx = DEMinfo[0]
    uly = DEMinfo[3]
    #get pixel size( resolution)
    res_we = abs(DEMinfo[1])
    res_ns = abs(DEMinfo[5])    
    depthList = []
    for n in range(len(points)):
        print(n)
        point_location = points[n]
        j = int(round((point_location[0] - ulx)/res_we))
        i = int(round((uly - point_location[1])/res_ns)) 
        if(DEMdata[i,j] != missingData and np.isnan(DEMdata[i,j]) == False):
            depth = -1.0 * DEMdata[i,j]
            print('New depth @ (%d) is %.1f, original depth is %.1f\n' %(n,depth, depths_in[n]))                
        else:
            depth = depths_in[n]
            print('Keep same depth (original depth): %.1f---(%.1f)\n'%(depth,depths_in[n]))
            #ax.plot(points[0],points[1],'ro',xx[i,j],yy[i,j],'g^')  #for debug purpose
            #time.sleep(1)
            #print("No DEM coverage for location: %.5f,%.5f (keep original value)\n"%(point_location[0],point_location[1]))
        depthList.append(depth)
    return depthList
#dep = list(map(map_dem_points, nodes_in,data,info))
def read_DEM(RasterFileName):
    from osgeo import gdal
    gdal.UseExceptions()
    try:    
        datafile = gdal.Open(RasterFileName)
        #get a quick resulotion checks
        print(datafile.GetMetadata())
    except RuntimeError:
        print('Unable to open Raster file')
        sys.exit(1)    
    try:    
        srcband = datafile.GetRasterBand(1)  #get a raster band
    except RuntimeError:
        print('Band (%i) not found' %1)
        sys.exit(1)    
    #list band statistics
    for band in range(datafile.RasterCount):
        band+= 1
        print("Getting Band: ", band)
        srcband = datafile.GetRasterBand(band)
        if srcband is None:
            continue
        
        stats = srcband.GetStatistics(True,True)
        if stats is None:
            continue
        print("[STATS] = Minimum=%.3f, Maximum= %.3f, Mean = %.3f, StdDev = %.3f"%(stats[0],stats[1],stats[2],stats[3]))
    info = datafile.GetGeoTransform()   #(ulx, uly, lrx, lry, we_res, ns_res)
    data = srcband.ReadAsArray()
    return data,info
# GDAL does not use python exceptions by default
import matplotlib.tri as tri    
plt.close('all')
coastline = r'C:\Matlab_toolbox\surgeLAB\data\coastlines\usa.dat'
cst = pd.read_csv(coastline,delim_whitespace=True, names = ['Lon','Lat'],na_values = 'NaN')
fort14 = r"B:\HSOFS\grid\plot.grd"
original_grid = read_grid(fort14)    
xy = original_grid.coordinates[:,0:2]
depth_original = original_grid.coordinates[:,2]
triangles = original_grid.triangles.astype(int)-1
#create triangulation
originalgrid_triang = tri.Triangulation(xy[:,0],xy[:,1],triangles=triangles,mask=None)
#
start = timeit.default_timer()
vmin = -999999.0
steps = 100
buffer=0.1
dataDir = r"B:\HSOFS\Data\2014-post_sandy_noaa_dem"
plt.close('all')
plotit = True
#get a list of Raster file
fileList = glob.glob(os.path.join(dataDir,'*.tif'))
for n in [0]: #range(len(fileList)):
    RasterFileName = fileList[n]
    data,info = read_DEM(RasterFileName)
    
    # GDAL provids the top-left coordinate (lat, lon)
    ulx = info[0]
    uly = info[3]
    #get pixel size( resolution)
    res_we = abs(info[1])
    res_ns = abs(info[5])

    x_bounds = [info[0],info[0]+res_we*(data.shape[1]-1),info[0]+res_we*(data.shape[1]-1),info[0],info[0]]
    y_bounds = [info[3],info[3],info[3]-res_ns*(data.shape[0]-1), info[3]-res_ns*(data.shape[0]-1),info[3]]
    [ulx,uly,lrx,lry] = [min(x_bounds),max(y_bounds),max(x_bounds),min(y_bounds)]
    boundsList = [ulx,uly,lrx,lry]

        
#get the grid points inside the DEM boundary
    nodes_in,index_mask_1d,depths_in = extract_gridpoints(original_grid,boundsList)  
#interpolate the depth to points    
    print('mapping DEM depth to nodes in the bounds\n')
    new_depth = np.asarray(map_dem_points(nodes_in,data,info,depths_in))
#return new gridObj
    print('Merge new depth into original ADCIRC grid object\n')
    new_grid = merge_grid(original_grid, new_depth,index_mask_1d)    
    if (plotit == True):
    #plot subset
    #[ulx,uly,lrx,lry] = [-74.075,40.3,-74.05,40.25]
    #sub-sampling the DEM data for plot
        xplot = np.arange(ulx,lrx,res_we*steps)
        yplot = np.arange(uly,lry,-res_ns*steps)
        xx,yy = np.meshgrid(xplot,yplot)
        start_i = round((ulx - info[0])/res_we)
        #end_i = round((lrx - info[0])/res_we)
        start_j = round((info[3]-uly)/res_ns)
        #end_j = round((info[3] - lry)/res_ns)
        end_i = start_i + data.shape[1]
        end_j = start_j + data.shape[0]
        print(start_i,end_i, start_j,end_j)
        cplot = data[start_j:end_j:steps,start_i:end_i:steps]          
        #xplot = xx[0::steps,0::steps]
        #yplot = yy[0::steps,0::steps]
        cplot[cplot==vmin] = np.nan
        cplot = -1.0 * cplot
        print(xx.shape,yy.shape,cplot.shape)

        #plot the coastlines
        colormap = plt.cm.jet
        fig,axes = plt.subplots(num=n+1,nrows=1,ncols = 4,figsize = (16,4),dpi=300)
        for ax in axes:
            ax.plot(cst.Lon,cst.Lat,linewidth = 0.2, color='k',label='coastline')    
            ax.plot(x_bounds,y_bounds,'k-')
            #ax.grid(color='gray',linestyle=':', linewidth = 2)                    
            ax.set_xlim([min(x_bounds)-buffer,max(x_bounds)+buffer])
            ax.set_ylim([min(y_bounds)-buffer,max(y_bounds)+buffer])
            ax.set_title(RasterFileName.split('\\')[-1],fontsize=5)
            ax.tick_params(labelsize=4)
        #subplot 311
        #set cmap min and max values
        vminval = -10 #for plot    
        vmaxval = round(max(np.nanmax(cplot),np.nanmax(depths_in)))    
    
        heatmap = axes[0].pcolor(xplot,yplot,cplot, cmap=colormap,  
                            vmin=vminval, vmax=np.nanmax(cplot))
        heatmap.cmap.set_under('white')       
        #bar = plt.colorbar(heatmap, extend='both',ax = axes[0])
        #subplot 312
        tri_maskindex = mask_triagles(xy,triangles,boundsList)
        masked_originalgrid_triang = originalgrid_triang
        masked_originalgrid_triang.set_mask(tri_maskindex)
        
        hd0 = axes[1].tripcolor(masked_originalgrid_triang, depth_original, edgecolors = 'none',
                                shading='flat',vmin=vminval,vmax=vmaxval,cmap=colormap)
                    
        #hd0 = axes[1].scatter(nodes_in[:,0],nodes_in[:,1], c=depths_in, s = 5, marker='s', edgecolors='none',
        #                    vmin =vminval,vmax=vmaxval,cmap=colormap  )
                            
        #plt.colorbar(hd0, extend='both',ax = axes[1]) 
        axes[1].set_xlim([min(x_bounds)-buffer,max(x_bounds)+buffer])
        axes[1].set_ylim([min(y_bounds)-buffer,max(y_bounds)+buffer])
        axes[1].set_title("Original Depth (m)",fontsize=6)                       
        #subplot 313
        depth_interp = new_grid.coordinates[:,2]     
        hd1 = axes[2].tripcolor(masked_originalgrid_triang, depth_interp, edgecolors = 'none',
                                shading='flat',vmin=vminval,vmax=vmaxval,cmap=colormap)       
        #hd1 = axes[2].scatter(nodes_in[:,0],nodes_in[:,1], c=new_depth, s = 5, marker='s', edgecolors='none',
        #                    vmin =vminval,vmax=vmaxval,cmap=colormap )
        cb2 = plt.colorbar(hd1, extend='both',ax=axes[2]) 
        cb2.ax.tick_params(labelsize=5)        
        axes[2].set_title("Interpolated Depth (m)",fontsize=6)        
        axes[2].set_xlim([min(x_bounds)-buffer,max(x_bounds)+buffer])
        axes[2].set_ylim([min(y_bounds)-buffer,max(y_bounds)+buffer])
        #difference
        depth_diff = depth_interp-depth_original     
        hd2 = axes[3].tripcolor(masked_originalgrid_triang, depth_diff, edgecolors = 'none',
                                shading='flat',vmin=-2,vmax=2,cmap=colormap)     
        #hd2 = axes[3].scatter(nodes_in[:,0],nodes_in[:,1], c=new_depth-depths_in, s = 5, marker='s', edgecolors='none',
        #                    vmin =-2,vmax=2,cmap=colormap )
        cb3 =plt.colorbar(hd2, extend='both',ax=axes[3]) 
        cb3.ax.tick_params(labelsize=5)
        axes[3].set_title("New Depth - Original Depth (m)",fontsize=6)        
        axes[3].set_xlim([min(x_bounds)-buffer,max(x_bounds)+buffer])
        axes[3].set_ylim([min(y_bounds)-buffer,max(y_bounds)+buffer])
       
        #fig.colorbar(hd1, ax=axes.ravel().tolist(),extend='both')
#        cax,kw = mpl.colorbar.make_axes([ax for ax in axes.flat])
#        plt.colorbar(im, cax=cax, **kw)
        picname = os.path.join(dataDir,'triplot_'+RasterFileName.split('\\')[-1].split('.')[0:-1][0]+'.png')
        plt.savefig(picname,dpi=300)
        for m in range(len(depth_original)):
            if(depth_original[m] != depth_interp[m]):
                print('depth different at %d'%m)
                
#       
#    del data
#    del cplot  ;  
stop = timeit.default_timer()
print("Total time in %.1f mintues"%((stop - start)/60))
##extract a subset of the data
#inDS = RasterFileName
#outDS = os.path.join(dataDir,'subset'+RasterFileName.split('\\')[-1] )
##set the bounds (upper lower x, upper lower y, lower right x, lower right y)
#ulx = -73.02114
#uly = 40.798108
#lrx = -72.734872
#lry = 40.65477


#translate = 'gdal_translate -projwin %s %s %s %s %s %s' %(ulx, uly, lrx, lry, inDS, outDS)
#os.system(translate)