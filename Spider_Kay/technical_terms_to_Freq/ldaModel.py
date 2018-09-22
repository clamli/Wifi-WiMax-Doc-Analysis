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
import pickle


if __name__ == "__main__":
 

    listOfWordLists = pickle.load(open("listOfWordLists.dat", "rb"))
    print("num of docs:", len(listOfWordLists))
    minCount = 5;
    vectorizer = CountVectorizer(min_df = minCount,tokenizer=lambda doc: doc, lowercase=False)
    X= vectorizer.fit_transform(listOfWordLists)

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
    model = lda.LDA(n_topics= numTopic, n_iter=500, random_state=1)
    model.fit(np.asarray(weight))     # model.fit_transform(X) is also available
    topic_word = model.topic_word_    # model.components_ also works
 
    #文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
#    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))
    fileNames = pickle.load(open("fileNames.dat", "rb"))   
    print("file num", len(fileNames))

 
    #输出前10篇文章最可能的Topic
    label = []      
    for n in range(len(listOfWordLists)):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
#        print("doc: {},topic: {}".format(n, topic_most_pr))
    
    #count label distribution
    labelMap = {}
    for item in label:
        labelMap[item] = labelMap.get(item, 0) + 1
    print("stats of topics amony documents:")
    print(labelMap)
    # one result: {1: 176, 4: 104, 2: 55, 0: 93, 3: 70}
    #write the label to file
    with open("label.txt", "w" ) as f:
        for item in label:
            f.write("%s\n" % item)
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
    featureName = pickle.load(open("featureName.dat", "rb"))
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(featureName)[np.argsort(topic_dist)][:-(numTopic+1):-1]
        print('*Topic {}\n- {}'.format(i, ','.join(topic_words)))



