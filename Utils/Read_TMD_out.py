# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:16:54 2016
Read the harmonic constant output and save it for fort.15 ADCIRC format
read_TMD_hc(fileIn, constNamesInFort15,scale)
constNamesInFort15=['k1','k2','m2','n2','o1','p1','q1','s2','M4','MS4','MN4','MM','MF']
fileIn: name of input file
fileIn = r"C:\Matlab_toolbox\tmd_toolboxv204\OUT\MicronesiaTPXO8.out"
@author: liang.kuang
"""

import numpy as np
import os

def read_TMD_hc(fileIn,constNamesInFort15,scale=1):
    

    fileOut = os.path.join(os.path.dirname(fileIn),"TMD.fort.15") 
    HCs=np.loadtxt(fileIn,usecols=[0,1,4,5],skiprows=2)                
    names = np.loadtxt(fileIn,usecols=[3],dtype='str',skiprows=2)
    temp = np.unique(names)
    names = names[0:len(temp)]
    names = [n[2:-1].upper() for n in names] 
    print("Total %d harmonic constitutents extracted!"%(len(names)))
    
    
    fout = open(fileOut,'w')    
    for n in np.arange(len(names)):
        index = names.index(constNamesInFort15[n].upper())     
        amp = HCs[index::len(names),2] * scale
        phase = HCs[index::len(names),3]
        fout.write("%s\n" %(constNamesInFort15[n].upper()))
        for m in np.arange(len(amp)):
            fout.write("%8.6f %6.3f\n"%(amp[m],phase[m]))
    fout.close()
    print("file saved to %s\n"%(fileOut))
    
    
    




