# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:49:23 2016
e.g.: utc_to_local(t.timetuple()):

@author: liang.kuang
"""
import time
import calendar
import datetime
def utc_to_local(t_tuple):
    secs = calendar.timegm(t_tuple)
    localStruct = time.localtime(secs)
    return datetime.datetime(*localStruct[:6])
