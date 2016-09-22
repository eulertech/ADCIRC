# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 15:50:57 2016
e.g. local_to_utc(t.timetuple())
@author: liang.kuang
"""

import time,calendar
import datetime

def local_to_utc(t_tuple):
    secs = time.mktime(t_tuple)
    utcStruct = time.gmtime(secs)
    return datetime.datetime(*utcStruct[:6])