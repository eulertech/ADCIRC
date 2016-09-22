# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 10:17:24 2016

@author: liang.kuang
"""

def collatz(n):
# if even
    if(n<1):
        return
    if(n%2 == 0):
        return int(n/2)
    else:
        return int(3*n + 1) 
        
myInput = input().strip().split()
N = int(myInput[0])  # n
K = int(myInput[1])  # k times

for i in range(K):
    N = collatz(N)
    
    
print(N)    