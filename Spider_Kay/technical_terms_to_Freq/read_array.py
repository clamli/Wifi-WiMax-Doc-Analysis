# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:55:37 2018

@author: zhenkai wang(Kay)
"""
import pickle
import scipy
if __name__ == "__main__":
    file1 = "wordFreqArray.dat"
    file2 = "featureName.dat"
    file3 = "computedFiles.dat"
    featureName = pickle.load(open(file2, "rb"))
    wordFreqArray = pickle.load(open(file1, "rb"))
    fileName = pickle.load(open(file3, "rb"))
    print(fileName)
#    print((wordFreqArray))
#    print(len(featureName))
#    print(featureName)
    X = wordFreqArray
    cooccurMatrix = Xc = (X.T * X)
    Xc.setdiag(0) 
#    print(Xc.todense())
    cx = scipy.sparse.coo_matrix(Xc)
    rows = zip(cx.row, cx.col, cx.data);
#    for i,j,v in rows:
#        print("(%d, %d), %s,(%s, %s)" % (i,j,v, featureName[i], featureName[j]))
#    print(cx.shape)

    print("number of word selected:", len(featureName))
    
    ## here we create the co-occurance matrix
    import csv
    with open("occurMatrix.csv", "w") as f:
        csvWriter = csv.writer(f,delimiter=',', quoting=csv.QUOTE_MINIMAL)
        print("OK")
        for i,j,v in rows:
            csvWriter.writerow([i,j,v, featureName[i], featureName[j]])
#    techTermPath1 = "word_list1"
#    techTermPath2 = "word_list2"
#    techTermPath3 = "word_list3"
#    techTermPath4 = "word_list4"
#    print(pickle.load(open(techTermPath1, "rb")))