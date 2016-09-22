# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:28:20 2016
compute root mean square error
RMSE(data,model) = sqrt(sum(m-d)**2)/len(data)
@author: liang.kuang
"""
import numpy as np
def RMSE(data,model):
    rmse = np.sqrt(np.sum((model-data)**2)/len(data))
    return rmse

