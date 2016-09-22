# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:51:08 2016

@author: liang.kuang
"""

def sort_string(wordIn):
    wordOut = ''.join(sorted(wordIn))
    return wordOut

import re
S = input().strip()

#remove all non-alphabetic characters and to lowercase
regex = re.compile('[^a-zA-Z\s]')
S = regex.sub('',S).lower()

#sort all letters in each word
words = S.split()
individual_word_sorted = []
for w in range(len(words)):
    individual_word_sorted.append(sort_string(words[w]))
# sort the new list of words
#words_temp = individual_word_sorted.split()
    

#remove duplicate word
words_final_list = list(set(individual_word_sorted))
words_final_list.sort()

words_final = ' '.join(words_final_list)

print(words_final)

