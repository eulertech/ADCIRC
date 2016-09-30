# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:03:05 2016
Code to read maxele.63, maxvel.63, maxwvel.63, maxrs.63, minpr.63
how to use: read_maxel(filename)
output: index, maxele, indexTime, maxeleTime
@author: liang.kuang
"""
def isNotEmpty(s):
    return bool(s and s.strip())

def read_maxele(filename):
    #from ADCIRC.Grid.Read_Grid import read_grid
    import numpy as np
    print("Starting read maxele/vel global field to nparray")
    f = open(filename)
    f.readline()
    line2  = f.readline()
    [ITemp, NP, DTNSGE, NSPOOLGE, IRTYPE] = line2.split()[0:5]
    NP = int(NP)
    line3 = f.readline()
    [TIME,TimeStep] = line3.split()    
    index = np.zeros([NP,1],dtype = int)
    maxele = np.zeros([NP,1],dtype = float)       
    
    cnt = 0
    while cnt < NP:
        line = f.readline()
        index[cnt,0] = int(line.split()[0])
        maxele[cnt,0] = float(line.split()[1])
        cnt = cnt + 1
        
        
    line = f.readline()
    indexTime = np.zeros([NP,1],dtype = int)
    maxeleTime = np.zeros([NP,1],dtype = float)     
    if (isNotEmpty(line)):       
        cnt = 0
        while cnt < NP:
            line = f.readline()
            indexTime[cnt,0] = int(line.split()[0])
            maxeleTime[cnt,0] = float(line.split()[1])
            cnt = cnt + 1
    else:
        print("End of file!")        
        
    f.close()
    print("Maximum field reading finished!")    
    return index,maxele, indexTime, maxeleTime    
