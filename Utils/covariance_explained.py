# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 11:09:40 2016
This is to calculate the covariance explained for two series data.
input: d as dtype np.array
       m as dtype np.array

output: covariance explained (float)       
cov_exp = 100 * (std(data) - std(data-model))/std(data)

@author: liang.kuang
"""
import numpy as np
def cov_exp(d,m):
    d = np.asarray(d)
    m = np.asarray(m)
    assert(len(d) == len(m)), "The length of data and model not the same!"
    cov_explained = 100 * (np.std(d)-np.std((d-m)))/np.std(d)
    return cov_explained