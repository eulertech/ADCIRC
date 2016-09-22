# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:49:43 2016
update harmonic constants at open boundaries in fort.15
update_fort15_obc(fort15,OBC_HC_file)
input: Harmonic constants at OBC saved in fort.15 format
input: fort.15 filename
output: new fort.15
    OBC_HC_file = r"C:\Matlab_toolbox\tmd_toolboxv204\OUT\TMD.fort.15"
    fort15 = r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA13\tidefac.fort.15"
@author: liang.kuang
"""
import os
import numpy as np

def update_fort15_obc(fort15,OBC_HC_file):

    fileOut = os.path.join(os.path.dirname(fort15),"OBC.fort.15")
    
    OBC = open(OBC_HC_file,'r').readlines()
    old15 = open(fort15,'r').readlines()
    headerline = 30
    NTIF = int(old15[headerline].split()[0])     #numer of tidal potential constituents
    NBFR = int(old15[headerline+NTIF*2+1].split()[0])  
    headerline = headerline + 2 + NTIF*2 + NBFR*2
        
    
    
    fout = open(fileOut,'w')
    for n in np.arange(headerline):
        fout.write("%s"%(old15[n]))
        
    for n in np.arange(len(OBC)):
        fout.write("%s"%(OBC[n]) )
        headerline = headerline + 1
        
    for n in np.arange(headerline,len(old15)):
        fout.write("%s"%(old15[n]))


    fout.close()    
    print("File with new OBC saved at: %s\n"%fileOut)
    

        
    
    
    
