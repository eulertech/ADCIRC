# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:50:37 2016
read tide_fac.out to dictionary
fileIn = r"R:\Projects\ESTOFS_for_Micronesia\runs\LTEA13\tide_fac.out"
returns dictionary
@author: liang.kuang
"""
import numpy as np
def read_tide_fac(fileIn):
    tf = np.loadtxt(fileIn,usecols = [1,2],skiprows=9)
    names = np.loadtxt(fileIn,dtype='str',usecols=[0],skiprows=9)
    names = [n[2:-1].upper() for n in names] 
    return dict(zip(names,tf))
            
        
