# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 15:20:49 2016

@author: liang.kuang
"""

from sys import argv
script, filename = argv

txt = open(filename)

print ("Here's your file %r: "%filename)
print (txt.read())

print ("Type the filename again:")
file_again = input("> ")

txt_again = open(file_again)

print (txt_again.read())