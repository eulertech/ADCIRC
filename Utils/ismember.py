# -*- coding: utf-8 -*-
"""
Created on Fri May 13 14:12:59 2016

@author: liang.kuang
"""
def ismember(a, b):
    bind = {}
    for i, elt in enumerate(b):
        if elt not in bind:
            bind[elt] = i
    return [bind.get(itm, None) for itm in a] 