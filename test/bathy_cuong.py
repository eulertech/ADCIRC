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
fig,ax = plt.subplots()
ax.plot(cst.Lon,cst.Lat,linewidth = 0.2, color='k',label='coastline')

start = timeit.timeit()                     
 
baseDir = r'R:\Projects\HSSOFS\Data\4_KUANG_WANG'
[maxx,maxy] = [-999,-999]
[minx,miny] = [999,999]
buffer = 2
bath = pd.DataFrame()
for year in range(startYear,endYear,1):
    try:
        filename = os.path.join(baseDir,str(year)+'.csv') 
        colNames = ['Survey_ID','Calculated_Lat','Calculated_Lon','Original_Depth','End_year','V_Datum']
        bathy = pd.read_csv(filename,header=None, names = colNames,skipinitialspace = True ,skip_blank_lines = True,
                           warn_bad_lines = True, skipfooter = 2, engine = 'python', converters = {-1: lambda s: s.strip()})
        #bathy = bathy.append(bathy_single,ignore_index=True)
                       
#concatFileName = os.path.join(baseDir,str(startYear)+'to'+str(endYear)+bathy.V_Datum[0]+'.csv')
#bathy.to_csv(concatFileName,sep=',',index = False,float_format='%.6f', columns = ['Calculated_Lon','Calculated_Lat','Original_Depth'] )                   
        ax.plot( bathy['Calculated_Lon'], bathy['Calculated_Lat'],  linewidth = 0.1, linestyle='',marker='o',mfc=clrs[year-startYear][0][0:3], mec= clrs[year-startYear][0][0:3],label=str(year))                       
        if(bathy.Calculated_Lon.min()< minx):
            minx = bathy.Calculated_Lon.min() - buffer
        if(bathy.Calculated_Lat.min() < miny):
            miny = bathy.Calculated_Lat.min()- buffer
        if(bathy.Calculated_Lon.max()> maxx):
            maxx = bathy.Calculated_Lon.max()+ buffer
        if(bathy.Calculated_Lat.max() > maxy):
            maxy = bathy.Calculated_Lat.max()+ buffer
    except:
        pass
    
ax.set_xlim([minx,maxx])
ax.set_ylim([miny,maxy])    
ax.set_title('Bathymetry footstamp after ' + str(startYear))      
ax.legend()
#plot a special interest box
ax.plot([-72.932159,-72.865965,-72.865965,-72.932159,-72.932159],
        [40.708575,40.708575,40.754674,40.754674,40.708575],'r-',linewidth=2)
ann = ax.annotate("Pelican Island",
                  xy=(-72.896960,40.724810), xycoords='data',
                  xytext=(-72.5, 40.4), textcoords='data',
                  size=9, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="black",ec='black'), 
                  )       
                       
endtime = timeit.timeit()
picname = os.path.join(baseDir,'individual_bathymetry_footstamp_'+str(startYear)+'to'+str(endYear)+'.png')
plt.savefig(picname,dpi=400)


print("processing time:%5.4f second"% (endtime-start))                   

#concatinate file
#concatFileName = os.path.join(baseDir,str(startYear)+'to'+str(endYear))
#fout = open(concatFileName,'wa')
#for year in range(startYear,endYear,1):
#    filename = os.path.join(baseDir,str(year)+'.csv') 
#    lines = open(filename,'r').readlines()
#    fout.write(lines)
        

