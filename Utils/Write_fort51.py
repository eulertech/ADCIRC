# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:37:28 2016
dump coops harmonic constants from get_ha function to fort.51 format
input: stationID, constituents
output: file for fort.51 format for stationID
e.g. write_fort51(data, constituents=['K1','K2','M2','N2','O1','P1','Q1','S2'],filOut)
@author: liang.kuang
"""
import numpy as np
from collections import OrderedDict
from ADCIRC.Data.Get_Harmonics_COOPS import get_ha

def write_fort51(data, constituents=['K1','K2','M2','N2','O1','P1','Q1','S2'],filOut):
    #stationID = 1890000
    data = get_ha(stationID)
    del data[0]
    fileOut = str(stationID)+"_HC_fort51.out"
    f = open(fileOut,'w')    
     
    f.write("%d\n"%stationID)
    for n in np.arange(len(constituents)):
        for m in np.arange(len(data)):
            if(data[m]['Name'] == constituents[n]): 
                f.write("%10.4f %10.4f\n"%(float(data[m]['Amplitude']), float(data[m]['Phase'])))
    
    
    f.close()
    print("Successfully get Harmonic Constants from coops website and saved to fort51 format\n")