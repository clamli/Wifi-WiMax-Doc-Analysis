# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:55:37 2018

@author: zhenkai wang(Kay)
parallel version of word-freq-matrix building.
"""
import fitz, re, os, pickle, multiprocessing
#import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, chunk
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from functools import partial
numCount = 0
path1 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_01.pdf"
path2 = "F:\\WireLessNLPGRA\\code\\NamedEntityRecognition\\some_proposal\\C802162a-01_06.pdf"
techTermPath = "words"
dictPath = "dict"
pdfDir =  "F:\\WireLessNLPGRA\\80216CompProj"#change this to the pdf folders
from fileProcessing import *
from techTermProcessing import *

def getPage(path):
# =============================================================================
#     get all the pages of file, return a list of string, each string is content of one page
# =============================================================================
    doc = fitz.open(path)
    content = []
    for i in range(doc.pageCount):
        content.append(doc.getPageText(i))
    return content
def abstractExtracter(firstPage):
# =============================================================================
#     extract abstract of the first page
# =============================================================================
    pAbstract = r'^Abstract\s(.+)'
    candidate = [re.findall(pAbstract,line) for line in firstPage.split('\n')]
    abstract = []
    for sen in candidate:
        if (len(sen) > 0):
            abstract.append(sen[0])
    return abstract[0]
def getStopWords():
# =============================================================================
#     #we return the stopWords in NLTK database
# =============================================================================
    return set(stopwords.words('english'))
def transform(word):
# =============================================================================
#     if a word is all upper case then return itself otherwise should return word lower case 
# =============================================================================
    isAllUpper = (word == word.upper())
    if isAllUpper:
        pass
    else:
        word = word.lower()
    return word

def getTechTerms(words, listOfTechTerm):
# =============================================================================
#     #given a list of words from a doc, and a list of tecnical terms, find all occurance of technical word
# =============================================================================
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
def hasCharDig(word):
# =============================================================================
#     #check whether a word has both digit and char
# =============================================================================

    hasChar = False
    hasWord = False
    for i in range(len(word)):
        c = word[i]
        if(c.isdigit()):
            hasChar = True
        if(c.isalpha()):
            hasWord = True
    return hasChar & hasWord
def getListOfTechTerms(dictAbb, *paths, isReset = False):
# =============================================================================
#     #functions: from both <abb, full title> dictionary and tech terms list, extract
#     #add both key and value in dictionary, add all the tech terms in tech terms list
#     #isReset: if true, then read all the files, if false, just try to read the dumped record of tech terms
# 
# =============================================================================
    try:
        if (isReset):
            raise Exception("reseting")
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
            if (len(word) > 1 and word.lower() != "ieee"):
                
                technicalWords.append(word)
        
        with open("techTerms.dat", "wb") as f:
            pickle.dump(technicalWords, f)
            
    
    print("finish loading technical terms list")
        
    return technicalWords

def getContent(textPath):
# =============================================================================
# #    input is the path of pdf file, return all of the words(segemented by \s \n)
# #    remove all punctuation
# =============================================================================
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
# =============================================================================
#     #transform a list of word to a dictionary whose key is word and value is the count of key occurring time in the list
# =============================================================================
    wordFreq = [wordList.count(p) for p in wordList]
    return dict(zip(wordList, wordFreq))

def getFreqDict(filePath, listOfTechTerms):
# =============================================================================
#     #given a file Path, extract all the tech terms in it according to listOfTechTerms
#     #return a word-freq-dict
# =============================================================================
    wordsFiltered = getContent(filePath)
    #print(wordsFiltered)

    #listOfTechTerms.append("Recommended Practice")#just a test
    potentialTechTerms = getTechTerms(wordsFiltered, listOfTechTerms)
#    print(potentialTechTerms)
    wordFreqDict = wordListToFreqDict(potentialTechTerms)
    return wordFreqDict
def getAllFiles(dirPath):
# =============================================================================
#     #get all the pdf files in the folder, only those can be parsed
# =============================================================================
    files = [os.path.join(dirPath, f) for f in os.listdir(dirPath)]

    files = list(filter(lambda f: f.endswith(('.pdf', '. PDF')), files))
    print("total number of pdf files under directory: ", len(files))
    goodFiles = []
    for file in files:
        try:
            doc = fitz.open(file)
        except:
            pass
        else:
            goodFiles.append(file)
    print("good file num: ",len(goodFiles))
    return goodFiles

def getAllDicts(files, listOfTechTerms, numFile):
# =============================================================================
#     # get a list of dicts, each is the word-freq-dict of a file
# =============================================================================
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

def getList(file, listOfTechTerms, dictAbb):
# =============================================================================
#     #get a list of word lists, each element is the word extracted from file from files
#     #replace all the words  that occurring in key set of dictAbb by corresponding full titles
# =============================================================================
    global numCount
    listOfWords = []

    try:
        wordsFiltered = getContent(file)
        techTerms = getTechTerms(wordsFiltered, listOfTechTerms)
        for i in range(len(techTerms)):
            abb = techTerms[i]
            fullTitle = dictAbb.get(abb, None)
            if fullTitle is not None:
                techTerms[i] = fullTitle
#                    print("changeing ", abb, " \t to ", fullTitle)
            listOfWords.append(techTerms)
        print(numCount, "\t", file)
        numCount += 1
            #here delete the duplicate one
    except:
        pass#if can't open the file then do nothing
    return (listOfWords, file)


def getDictOfAbb(*paths):
# =============================================================================
#     #this file is a list of list, each of the sublist contains two string, first one is abbreviation, second one is full title
#     #make it into a dictionary
# =============================================================================
    dictAbb = {}
    for path in paths:
        with open(path, 'rb') as fp:
            l = pickle.load(fp)
#     for key, value in dictAbb.iteritems():
    for i in range(len(l)):
        dictAbb[l[i][0]] = l[i][1].lower()

    return dictAbb
from itertools import product
if __name__ == "__main__":
    #key paras
    minCount = 5
    numFile = 400;
    
    
    #prepocessing
    dictAbb1 = getDictOfAbb(dictPath)
    #if put trus as third para, then it will reextract the tech terms from files
    listOfTechTerms1 = getListOfTechTerms(dictAbb1, techTermPath, True)
    print("finish loading")
    #get all the files
    
    fileNames = getSelectedFileNames(pdfDir, 0, numFile);
    print("start parallal processing")
    np = 16
    p = multiprocessing.Pool(np)
    output = p.map(partial(getList, listOfTechTerms = listOfTechTerms1, dictAbb = dictAbb1),  [file for file in fileNames])
#    print(len(output[0]))
    listOfWordLists = []
    computedFiles = []
    for out in output:
        if (len(out[0]) > 0):
            listOfWordLists.append(out[0][0])
            computedFiles.append(out[1])
    print(listOfWordLists[0])
    print("number of files:", len(computedFiles))
    
    
    vec = CountVectorizer(min_df = minCount,tokenizer=lambda doc: doc, lowercase=False)
    wordFreqArray = vec.fit_transform(listOfWordLists)
#    listOfDicts = getAllDicts(fileNames, listOfTechTerms, numFile)
#    vec = DictVectorizer()
#    wordFreqArray = vec.fit_transform(listOfDicts)
    featureName = vec.get_feature_names()
#    print(wordFreqArray)
#    print(featureName)
    
    #save key variables
    keyWord = "file_" + str(numFile) + "_minDf_" + str(minCount) + "_"
    pickle.dump(computedFiles, open(keyWord + "computedFiles.dat", "wb"))
    pickle.dump(wordFreqArray, open(keyWord + "wordFreqArray.dat", "wb"))
    pickle.dump(featureName, open(keyWord + "featureName.dat", "wb"))
    pickle.dump(listOfWordLists, open(keyWord + "listOfWordLists.dat", "wb"))
    
    pickle.dump(computedFiles, open("computedFiles.dat", "wb"))
    pickle.dump(wordFreqArray, open("wordFreqArray.dat", "wb"))
    pickle.dump(featureName, open("featureName.dat", "wb"))
    pickle.dump(listOfWordLists, open("listOfWordLists.dat", "wb"))
