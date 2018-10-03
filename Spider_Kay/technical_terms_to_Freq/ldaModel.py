# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 07:39:17 2018


@author: Zhenkai Wang(kay)
this code is redeveloped from the code in following links:
https://blog.csdn.net/Eastmount/article/details/50891162
https://blog.csdn.net/Eastmount/article/details/50824215
try to use a lda model in word-freq-matrix
"""

import os  
import sys
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 
import pickle, json

def trick(wordList):
    newList = []
    for word in wordList:
        if (word == "IEEE"):
            continue
        newList.append(word)
    return newList

if __name__ == "__main__":
 
#    filePath = "listOfWordLists.dat"
#    fileNames = pickle.load(open(fileNamesPath, "rb"))  
    
#    wordListsPath = "listOfWordDicts.dat"
    
    #use both 
    collection = "useBoth_"
    wordListsPath = "file_400_minDf_1_useAB_listOfWordDicts.dat"
    
    
#    collection  = "onlyAbb_"
#    wordListsPath = "Abbreviation_from_files_400.dat"
#    wordListsPath = "Abbreviation_from_files_1000.dat"
#    wordListsPath = "Abbreviation_from_files_All.dat"
#    fileNamesPath = "computedFiles.dat"
    listOfWordListsDict = pickle.load(open(wordListsPath, "rb"))
    listOfWordLists = []
    fileNames = []
    
    for file, wordList in listOfWordListsDict.items():
#        print(wordList)
        listOfWordLists.append(wordList)
        fileNames.append(file)
    print("num of docs:", len(listOfWordLists))
    minCount = int(len(fileNames) / 100);
    print("minCount", minCount)
    vectorizer = CountVectorizer(min_df = minCount,tokenizer=lambda doc: doc, lowercase=False)
    X= vectorizer.fit_transform(listOfWordLists)
    print(X.shape)

#    X = vectorizer.fit_transform(corpus)
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()
 
    print(len(weight))
#    print(weight[:5, :5])
 
    #LDA算法
    print('LDA:')
    import lda
    import lda.datasets
    numTopic = 10
    numIter = 500
    model = lda.LDA(n_topics= numTopic, n_iter= numIter, random_state=1)
    model.fit(np.asarray(weight))     # model.fit_transform(X) is also available
    topic_word = model.topic_word_    # model.components_ also works
 
    #文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
#    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))
 
#    print("file num", len(fileNames))

 
    #输出前10篇文章最可能的Topic
    labels = []      
    for n in range(len(listOfWordLists)):
        topic_most_pr = doc_topic[n].argmax()
        labels.append(topic_most_pr)
#        print("doc: {},topic: {}".format(n, topic_most_pr))
    
    #count label distribution
    labelMap = {}
    for item in labels:
        labelMap[item] = labelMap.get(item, 0) + 1
    print("stats of topics amony documents:")
    print(labelMap)
    # one result: {1: 176, 4: 104, 2: 55, 0: 93, 3: 70}
    #write the label to file
    import datetime
    date = datetime.datetime.now()
    prefix = collection + str(date.month) + str(date.day) + "date_" + str(X.shape[0]) + "file_" + str(X.shape[1]) + "word_" + str(minCount) + "mindf_" + str(numTopic) + "topic_" + str(numIter) + "iter_"
    with open(prefix + "model.dat", "wb" ) as f:
        pickle.dump(model, f)
    with open(prefix + "labels.txt", "w" ) as f:
        for i in range(len(labels)):
            item = labels[i]
            file = fileNames[i]
            f.write("%s\t:%s\n" %(file, item))
    #write down a dictionary, whose key is the topic index, value is the list of files 
    #classified into this topic
    with open(prefix + "filesInDiffTopics.txt", "w") as f:
        tempDict = {}
        for i in range(numTopic):
            tempDict[i] = []
        for i in range(len(labels)):
            item = labels[i]
            file = fileNames[i]
            tempDict[item].append(file)
            
        with open(prefix + "dict_topic_files.dat", "wb") as d:
            pickle.dump(tempDict, d)
#        json.dump(tempDict, f)
        for k, l in tempDict.items():
            f.write(str(k) + "\t:" + str(labelMap[k]) + "\n")
            for elem in l:
                f.write(str(elem) + "\n")
            f.write("\n")
#        f.write("\n")
#        for k, v in labelMap.items():
#            f.write(str(k) + "\t" + str(v) + "\n")
    #match the label to document name
    
    
        
    #计算文档主题分布图
    import matplotlib.pyplot as plt  
#    f, ax= plt.subplots(6, 1, figsize=(8, 8), sharex=True)  
#    for i, k in enumerate([0, 1, 2, 3, 8, 9]):  
#        ax[i].stem(doc_topic[k,:], linefmt='r-',  
#                   markerfmt='ro', basefmt='w-')  
#        ax[i].set_xlim(-1, 2)     #x坐标下标
#        ax[i].set_ylim(0, 1.2)    #y坐标下标
#        ax[i].set_ylabel("Prob")  
#        ax[i].set_title("Document {}".format(k))  
#    ax[5].set_xlabel("Topic")
#    plt.tight_layout()
#    plt.show() 
    
    #show the top words in each topic    
#    featureName = pickle.load(open("featureName.dat", "rb"))
    vocabulary = vectorizer.vocabulary_;
    tempDict = {};
    for word, idx in vocabulary.items():
        tempDict[idx] = word
    featureNames = []
    for i in range(len(tempDict)):
        featureNames.append(tempDict[i])
#    print(featureNames)
    with open(prefix + "topic_word.txt", "w" , errors= "ignore") as f:
        tempDict = {}
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(featureNames)[np.argsort(topic_dist)][:-(numTopic+5):-1]
            tempDict[i] = topic_words
            topic_words = trick(topic_words)
            lineContent = '*Topic {}\n- {}\n'.format(i, ','.join(topic_words))
            f.write(lineContent)
            print(lineContent)
        with open(prefix + "dict_topic_wordList.dat", "wb") as d:
            pickle.dump(tempDict, d)
        
    


