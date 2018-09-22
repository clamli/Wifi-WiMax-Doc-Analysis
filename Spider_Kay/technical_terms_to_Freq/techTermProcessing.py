# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 00:39:41 2018
object: this file is a tool function collection for a dealing with tech Terms

@author: zhenkai wang(kay)
"""
import pickle, re
import string
def getDictOfAbb(*paths):
    #this file is a list of list, each of the sublist contains two string, first one is abbreviation, second one is full title
    #make it into a dictionary
    dictAbb = {}
    for path in paths:
        with open(path, 'rb') as fp:
            l = pickle.load(fp)
#     for key, value in dictAbb.iteritems():
    for i in range(len(l)):
        dictAbb[l[i][0]] = l[i][1].lower()
        
    return dictAbb
def getListOfTechTerms(dictAbb, *paths):
    
    try:
        with open("techTerms.dat", "rb") as f:
            technicalWords = pickle.load(f)
    except:
        technicalWords = []
        for path in paths:
            with open (path, 'rb') as fp:
                technicalWords += pickle.load(fp)
        for k, v in dictAbb.items():
            technicalWords.append(k)
            technicalWords.append(v)
        temp = list(set(technicalWords))
        technicalWords = []
        for word in temp:
            if (len(word) > 1):
                technicalWords.append(word)
        with open("techTerms.dat", "wb") as f:
            pickle.dump(technicalWords, f)
    return technicalWords

def getTechTerms(words, listOfTechTerm):
    #given a list of words, and a list of tecnical terms, find all occurance of technical word
    p1Match = r'^([A-Z]{2,})$'
    p2Contain = r'802'

    result = []
    wordNum = len(words)
    for i in range(wordNum):
        word = words[i]
#        word = transform(word)
        #if (word in listOfTechTerm):#since they are all lowercase in listOfTechTerm
        #    result.append(word)
        isTerm = False
        for term in listOfTechTerm:
            #correct match
            if word == term:
                isTerm = True
            splited_terms = term.split()
            
            if len(splited_terms) > 1:
                isEqual = True
                for idx in range(len(splited_terms)):
                    if (i + idx > wordNum - 1):
                        break
                    if (words[i + idx] != splited_terms[idx]):
                        isEqual = False
                if (isEqual):
                    result.append(term)       
                
            
            
                
                
        if (isTerm):
            result.append(word)
#        elif (len(word) > 1):
#            p1Result = re.match(p1Match, word)#all uppercase
#            p2Result = re.findall(p2Contain, word)#contains 802.
#            p3Result = hasCharDig(word)#contains at least one char and digit
#            p4Result = re.findall('http', word)
#            #print(word, " ", p1Result, " ", p2Result)
#            if (p1Result is not None ) or len(p2Result) > 0 or p3Result:
#                if len(p4Result) == 0:
#                    result.append(word)
    #delete stopword
    stopWords = getStopWords()
    wordsFiltered = [] 
    for w in result:
        if w not in stopWords:
            wordsFiltered.append(w)
    return wordsFiltered


