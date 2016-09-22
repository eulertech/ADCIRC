# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 10:53:00 2016
Code to analyse bathymetry data from Cuong (csv comma seprated)
1. read in csv file
2. parse the data
3. scatter plot of the footstamp
4. save figures
@author: liang.kuang
"""
import os,matplotlib
import numpy as np
import pandas as pd
import timeit
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
plt.close('all')

startYear = 2010
endYear = 2017

norm = matplotlib.colors.Normalize(vmin = startYear, vmax = endYear)
print(norm(2013)) # 0.xx
cmap = matplotlib.cm.get_cmap('Set1')
clrs = [[cmap(norm(y))] for y in range(startYear,endYear)]
# read in coastline file USA
coastline = r'C:\Matlab_toolbox\surgeLAB\data\coastlines\usa.dat'
cst = pd.read_csv(coastline,delim_whitespace=True, names = ['Lon','Lat'],na_values = 'NaN')


start = timeit.timeit()                     
 
baseDir = r'R:\Projects\HSSOFS\Data\4_KUANG_WANG'

buffer = 0.25
bathy_all = pd.DataFrame()
for year in range(startYear,endYear,1):
    [maxx,maxy] = [-999,-999]
    [minx,miny] = [999,999]
    fig = plt.figure(year,dpi=200)
    fig.clf()
    ax = fig.add_axes([0.1 ,0.1 ,0.8,0.8])
    ax.plot(cst.Lon,cst.Lat,linewidth = 0.2, color='k',label='coastline')
    try:
        filename = os.path.join(baseDir,str(year)+'.csv') 
        colNames = ['Survey_ID','Calculated_Lat','Calculated_Lon','Original_Depth','End_year','V_Datum']
        bathy = pd.read_csv(filename,header=None, names = colNames,skipinitialspace = True ,skip_blank_lines = True,
                           warn_bad_lines = True, skipfooter = 2, engine = 'python', converters = {-1: lambda s: s.strip()})
        bathy_all = bathy_all.append(bathy,ignore_index=True)                       
        
        ax.plot( bathy['Calculated_Lon'], bathy['Calculated_Lat'],  linestyle='',marker='o',markersize = 1,mfc=clrs[year-startYear][0][0:3], mec= clrs[year-startYear][0][0:3],label=str(year))                       
        if(bathy.Calculated_Lon.min()< minx):
            minx = bathy.Calculated_Lon.min() - buffer
        if(bathy.Calculated_Lat.min() < miny):
            miny = bathy.Calculated_Lat.min()- buffer
        if(bathy.Calculated_Lon.max()> maxx):
            maxx = bathy.Calculated_Lon.max()+ buffer
        if(bathy.Calculated_Lat.max() > maxy):
            maxy = bathy.Calculated_Lat.max()+ buffer
        ax.set_xlim([minx,maxx])
        ax.set_ylim([miny,maxy])    
        ax.set_title('Bathymetry footstamp in: ' + str(year))      
        ax.legend()
        picname = os.path.join(baseDir,'Z_individual_bathymetry_footstamp_'+str(year)+'.png')
        plt.savefig(picname,dpi=300)

    except:
        pass
concatFileName = os.path.join(baseDir,str(startYear)+'to'+str(endYear)+bathy.V_Datum[0]+'.csv')
bathy_all.to_csv(concatFileName,sep=',',index = False,float_format='%.6f', columns = ['Calculated_Lon','Calculated_Lat','Original_Depth'] )                                         
endtime = timeit.timeit()


print("processing time:%5.4f second"% (endtime-start))                   

