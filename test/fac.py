# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:14:59 2016

@author: liang.kuang
"""
def fac(n):
    if n == 0:
        return 1
    else:
        return n*fac(n-1)
def facMN(m,n):
    return fac(m)/fac(m-n)

vals = input().strip().split()
M = int(vals[0])
N = int(vals[1])
if(M<N):
    print(0)
elif(M==0 and N==0):
    print(0)    
else:
    print(int(facMN(M,N)/fac(N)))

