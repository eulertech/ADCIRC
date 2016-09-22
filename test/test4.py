# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 10:43:16 2016

@author: liang.kuang
"""

import math
#build the model
def log_reg_model(coef, model_input):
    #coef: list of log regression coefficent
    f = float(coef[-1])
    for i in range(len(model_input)):
        f = f + float(coef[i]) * float(model_input[i])
    return 1/(1+math.exp(-f))    


model_coef = input().strip().split()
model_input = input().strip().split()
print(log_reg_model(model_coef, model_input))