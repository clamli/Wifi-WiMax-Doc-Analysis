# -*- coding: utf-8 -*-

"""
Created on Sat Sep 22 00:35:14 2018

@author: zhenkai wang(Kay)
object: this code is used to a tool function collection for getting the files
"""
import fitz, re, random, os
#import nltk
from nltk import word_tokenize, pos_tag, ne_chunk, chunk
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from functools import partial
import pickle
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

#def getAllFiles(dirPath, storeName = "allFileName.dat"):
def getAllFiles(dirPath):
    storeName = dirPath.split("\\")[-1] + "Filename.dat"
#    print(os.listdir(dirPath))
    try:
        with open(storeName, "rb") as f:
            selectedFiles = pickle.load(f)
        print("loading previous all file Names")
        return selectedFiles
    except:            
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
        pickle.dump(goodFiles, open(storeName, "wb"))
        return goodFiles


def getSelectedFileNames(pdfDir, start, end, storeName = "randomIdx.dat"):
    fileNames = getAllFiles(pdfDir);
    try:
        with open(storeName, "rb") as f:
            
            fileIdxWanted = pickle.load(f)
        print("loading previous ", storeName, " success")
            
    except:
        print("loading new ", storeName, " success")
        fileIdxWanted = random.sample(range(len(fileNames)), len(fileNames))
        pickle.dump(fileIdxWanted, open(storeName, "wb"))
        #if want to change the randomIdx, then delete the comment
    selectedFiles = []
    for idx in fileIdxWanted:
        selectedFiles.append(fileNames[idx])
    
    #make sure not exceed
    end = min(end, len(selectedFiles))
    return selectedFiles[start:end]#[start,start + 1, xxx, end- 1]