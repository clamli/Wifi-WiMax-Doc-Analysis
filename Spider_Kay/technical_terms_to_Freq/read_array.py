# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:55:37 2018

@author: zhenkai wang
"""
import pickle
if __name__ == "__main__":
    file1 = "wordFreqArray.dat"
    file2 = "featureName.dat"
    featureName = pickle.load(open(file2, "rb"))
    wordFreqArray = pickle.load(open(file1, "rb"))
    print((wordFreqArray))
    print(len(featureName))
#    print(featureName)
