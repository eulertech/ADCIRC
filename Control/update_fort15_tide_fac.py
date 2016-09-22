# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:00:38 2016
tidefacFile = r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA13\tide_fac.out"
fort15 = r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA13\fort.15"
update_fort15_tidefac(fort15,fileOut,tidefacFile)
@author: liang.kuang
"""
import os
import numpy as np
from ADCIRC.Utils.Read_tide_fac import read_tide_fac
def update_fort15_tidefac(fort15,tidefacFile):
    fileOut = os.path.join(os.path.dirname(fort15),"tidefac.fort.15")   
    tidefac = read_tide_fac(tidefacFile)

    old15 = open(fort15,'r').readlines()
    headerline = 30
    NTIF = int(old15[headerline].split()[0])     #numer of tidal potential constituents
    #headerline = headerline + 2 + NTIF*4
        

    fout = open(fileOut,'w')
    for n in np.arange(headerline+1):
        fout.write("%s"%(old15[n]))
       
# update tide_fac line by line        
    for n in np.arange(NTIF):
        constName= old15[headerline+1+n*2].split()[0].upper()
        values = old15[headerline+1+n*2+1].split()[0:5]
        values[3] = str(tidefac[constName][0])
        values[4] = str(tidefac[constName][1])       
        fout.write("%s"%(old15[headerline+1+n*2]))
        fout.write(' '.join(values)+'\n')
       # fout.write("%f %f %f %f %f"%( [float(x) for x in values] ) )
    NBFR = int(old15[headerline+NTIF*2+1].split()[0])     #numer of tidal potential constituents        
    fout.write("%d\n"%(NBFR))   
    
    for n in np.arange(NBFR):
        constName= old15[headerline+2+NTIF*2+n*2].split()[0].upper()
        values = old15[headerline+2+NTIF*2+n*2+1].split()[0:3]
        print(constName)
        print(values)
        values[1] = str(tidefac[constName][0])
        values[2] = str(tidefac[constName][1])       
        fout.write("%s"%(old15[headerline+2+NTIF*2+n*2]))
        fout.write(' '.join(values)+'\n')       
#        fout.write("%f %f %f"%( [float(x) for x in values] ))               
    
    for n in np.arange(headerline+2+NTIF*2+NBFR*2,len(old15)):
        fout.write("%s"%(old15[n]))


    fout.close()    
    print("File with new tidal potential saved at: %s\n"%fileOut)
