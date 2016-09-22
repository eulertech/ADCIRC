# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:37:28 2016
input: stationID, constituents
output: file for fort.51 format for stationID
@author: liang.kuang
"""
import numpy as np
from collections import OrderedDict
from ADCIRC.Data.Get_Harmonics_COOPS import get_ha

def harmonics2fort51(stationID, constituents=['K1','K2','M2','N2','O1','P1','Q1','S2']):
    stationID = 1630000
    hcs = get_ha(stationID)
    