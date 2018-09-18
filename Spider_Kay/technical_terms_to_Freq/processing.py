# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 21:47:49 2018

@author: Zhenkai Wang
"""
#this code is used for extracting 

#this code is to use pattern matching and dictionary matching to find out the all the technical terms in documents
import fitz, re, os, pickle
#import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, chunk
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer


path1 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_01.pdf"
path2 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_06.pdf"
techTermPath1 = "word_list1"
techTermPath2 = "word_list2_abb_title"
techTermPath3 = "word_list3_abb_title"
techTermPath4 = "word_list4"
pdfDir =  "F:\\WireLessNLPGRA\\80216CompProj"

def getPage(path):
    #get all the pages of file, return a list of string, each string is content of one page
    doc = fitz.open(path)
    content = []
    for i in range(doc.pageCount):
        content.append(doc.getPageText(i))
    return content
def abstractExtracter(firstPage):
    #extract abstract of the first page
    pAbstract = r'^Abstract\s(.+)'
    candidate = [re.findall(pAbstract,line) for line in firstPage.split('\n')]
    abstract = []
    for sen in candidate:
        if (len(sen) > 0):
            abstract.append(sen[0])
    return abstract[0]
def getStopWords():
    return set(stopwords.words('english'))
def getTechTerms(words, listOfTechTerm):
    #given a list of words, and a list of tecnical terms, find all occurance of technical word
    p1Match = r'^([A-Z]{2,})$'
    p2Contain = r'802'

    result = []
    wordNum = len(words)
    for i in range(wordNum):
        word = words[i]
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
        elif (len(word) > 1):
            p1Result = re.match(p1Match, word)#all uppercase
            p2Result = re.findall(p2Contain, word)#contains 802.
            p3Result = hasCharDig(word)#contains at least one char and digit
            p4Result = re.findall('http', word)
            #print(word, " ", p1Result, " ", p2Result)
            if (p1Result is not None ) or len(p2Result) > 0 or p3Result:
                if len(p4Result) == 0:
                    result.append(word)
    #delete stopword
    stopWords = getStopWords()
    wordsFiltered = [] 
    for w in result:
        if w not in stopWords:
            wordsFiltered.append(w)
    return wordsFiltered
def hasCharDig(word):

    hasChar = False
    hasWord = False
    for i in range(len(word)):
        c = word[i]
        if(c.isdigit()):
            hasChar = True
        if(c.isalpha()):
            hasWord = True
    return hasChar & hasWord
def getListOfTechTerms(*paths):
    import pickle
    technicalWords = []
    for path in paths:
        with open (path, 'rb') as fp:
            technicalWords += pickle.load(fp)
    return technicalWords

def getContent(textPath):
    content = getPage(textPath)
    text1 = '.'.join(content)

    #words = nltk.word_tokenize(text1)
    sents = sent_tokenize(text1)
    words = []
    #delete punctuation
    for sent in sents:
        words += [word.strip(string.punctuation) for word in re.split(r'\s|\n', sent)]
    #delete stopword
#     stopWords = set(stopwords.words('english'))
#     wordsFiltered = [] 
#     for w in words:
#        if w not in stopWords:
#            wordsFiltered.append(w)

    wordsFiltered = words
    return wordsFiltered
def wordListToFreqDict(wordList):
    wordFreq = [wordList.count(p) for p in wordList]
    return dict(zip(wordList, wordFreq))

def getFreqDict(filePath, listOfTechTerms):
    wordsFiltered = getContent(filePath)
    #print(wordsFiltered)
    
    #listOfTechTerms.append("Recommended Practice")#just a test
    potentialTechTerms = getTechTerms(wordsFiltered, listOfTechTerms)
#    print(potentialTechTerms)
    wordFreqDict = wordListToFreqDict(potentialTechTerms)
    return wordFreqDict
def getAllFiles(dirPath):
#    print(os.listdir(dirPath))
    files = [os.path.join(dirPath, f) for f in os.listdir(dirPath)]
    print("total number of files under directory: ", len(files))
    files = filter(lambda f: f.endswith(('.pdf', '. PDF')), files)
    return list(files)

def getAllDicts(files, listOfTechTerms, numFile):
    
    listOfDicts = []
    count = 0
    for file in files:
        try:
            print(count, "\t: ", file)
            listOfDicts.append(getFreqDict(file, listOfTechTerms))
            count += 1
        except:
            pass
        if (count >= numFile):
            break
                
    return listOfDicts
def getAllLists(files, listOfTechTerms, dictAbb, numFile):
    for k, v in dictAbb.items():
        listOfTechTerms.append(k)
        listOfTechTerms.append(v)
    print(len(listOfTechTerms))
#    print(listOfTechTerms)
    listOfTechTerms = list(set(listOfTechTerms))
    print("after deleting duplication, num of tech terms: ", len(listOfTechTerms))
    print("total num of tech terms:", len(listOfTechTerms))
    pickle.dump(listOfTechTerms, open("listOfTechTerms.dat", "wb"))
    listOfWords = []
    count = 0
    for file in files:
        try:
            print(count, "\t", file)
            wordsFiltered = getContent(file)
            techTerms = getTechTerms(wordsFiltered, listOfTechTerms)
            for i in range(len(techTerms)):
                abb = techTerms[i]
                fullTitle = dictAbb.get(abb, None)
                if fullTitle is not None:
                    techTerms[i] = fullTitle
#                    print("changeing ", abb, " \t to ", fullTitle)
            listOfWords.append(techTerms)
            #here delete the duplicate one
            
            count += 1
        except:
#            print(ValueError)
            pass
            
        if (count >= numFile):
            break
    return listOfWords

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
        
if __name__ == "__main__":
    #prepocessing
    listOfTechTerms = getListOfTechTerms(techTermPath1, techTermPath4)#here it can take as much doc as possible
    dictAbb = getDictOfAbb(techTermPath2, techTermPath3)
    #get all the files
    numFile = 200
    minCount = 5
    fileNames = getAllFiles(pdfDir);
    listOfWords = getAllLists(fileNames, listOfTechTerms, dictAbb, numFile)
    vec = CountVectorizer(min_df = minCount,tokenizer=lambda doc: doc, lowercase=False)
    wordFreqArray = vec.fit_transform(listOfWords)
#    listOfDicts = getAllDicts(fileNames, listOfTechTerms, numFile)
#    vec = DictVectorizer()
#    wordFreqArray = vec.fit_transform(listOfDicts)
    featureName = vec.get_feature_names()
#    print(wordFreqArray)
#    print(featureName)
    pickle.dump(wordFreqArray, open("wordFreqArray.dat", "wb"))
    pickle.dump(featureName, open("featureName.dat", "wb"))
    
    
    
    