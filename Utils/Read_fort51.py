# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:05:28 2016
fort51 = r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA07\fort.51"
fort51 = r"R:\Projects\ESTOFS_for_Micronesia\Data\Harmonic\HarmonicConstants_Fort51Format"
@author: liang.kuang
"""
import numpy as np
from collections import OrderedDict

def read_fort51(fort51):
    fin = open(fort51,'r')
    numConsts = fin.readline().split()[0]
    names = []
    for n in np.arange(int(numConsts)):
        names.append(fin.readline().split()[3].upper())
    numStations = int(fin.readline().split()[0])
    HC_model = []    
    stationsName = []
    for s in np.arange(numStations):
        print("reading %d th station harmonic constants from fort.51\n"%(s+1))
        values = []
        for i in np.arange(int(numConsts)+1):
            line = fin.readline()
            print(line)
            if i>0:
                values.append(line.split()[0:2]) 
            else:
                stationsName.append(line.strip())
                
        values = OrderedDict(zip(names,values))        
        HC_model.append(values)
    return OrderedDict(zip(stationsName,HC_model))    
        
    
