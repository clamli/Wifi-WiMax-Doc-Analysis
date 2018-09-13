# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 23:09:24 2018

@author: zhenkai wang
"""
#for the mentor 802 11 and 802 16, we try to extract the author name and compnay name seperately, if there are several authors listed,
#use ; to seperate them

import csv, re
def extract_name(column):
    #this is for mentor website table
    # some have pattern like this
    # Amjad Soomro, Atul Garg, Javier Del Prado (Philips)
    #
    p4Author= r'^([^\(\)]+)'
    p4Company = r'\((.+)\)'
    authors = []
    companies = []
    for value in column:
        author = re.findall(p4Author, value)
        if (author):
            temp = [a.strip() for a in author[0].strip().split(",")]
            temp = ";".join(temp)
            authors.append(temp)
        else:
            author.append("no name")
        
        company = re.findall(p4Company, value)
        if (company):
            "if company name contains comma, then it will be sperated into 2 columns"
            companies.append('\"' + company[0].strip() + '\"')
        else:
            companies.append("no company")
    return authors, companies, []

def extract_name2(column):

    p4Title =  r'^([^\(\)]+)'
    p4AuthorCompany = r'\((.+)\)'
    titles = []
    authorCompanies = []
    authors = []
    companies = []
    for value in column:
        title = re.findall(p4Title, value)
        if (title):
            titles.append(title[0])
        else:
            titles.append("null")
        
        authorCompany = re.findall(p4AuthorCompany, value)
        if (authorCompany):
            "if company name contains comma, then it will be sperated into 2 columns"
            authorCompanies.append(authorCompany[0])
            author, company = process1(authorCompany[0])
            companies.append(company)
            authors.append(author)
        else:
            companies.append("no company")
            authors.append("no name")
    return authors, companies, titles
    
def process1(value):
    #this is used to extract author and company
        #for 1990-1996 documents , example like this
    #(Simon Black, Symbionics)
    #(Vic Hayes, Chair, AT&T WCND Utrecht)
    #(Vic Hayes - AT&T WCND Utrecht)
    #(Vic Hayes, Lucent Technologies, Chair)
    #(Larry van der Jagt, Knowledge Implementations, Inc.)
    segs = [s.strip() for s in re.split(r',|-', value)]
    numSegs = len(segs)
    if (numSegs == 1):
        return segs[0], "no company"
    elif (numSegs == 2):
        return segs[0], '\"' + segs[1] + '\"'
    else:
        idxInc = -1
        idxChair = -1
        notAuthorIdx = []
        company = ""
        author = ""
        for i in range(numSegs):
            seg = segs[i]
            if (seg == "Inc."):
                
                #means there is a comma in the middle of company name
                #like (Larry van der Jagt, Knowledge Implementations, Inc.)
                idxInc = i;
                company = segs[idxInc - 1] + " Inc."
                notAuthorIdx = [idxInc - 1, idxInc]
            if (seg == "Chair"):
                idxChair = i
                notAuthorIdx.append(idxChair)
            idxs = []
            for idx in range(numSegs):
                if idx not in notAuthorIdx:
                    idxs.append(idx)
            if (company):
                author = ";".join([segs[i] for i in idxs])
                
            else:
                company = segs[len(idxs) - 1]
                author = ";".join([segs[i] for i in idxs[0:-2]])
        return author, '\"' + company + '\"'
            
            
            
                
        
    
    
def parse_file(path, keyColumnIdx, savePath, downloadColumnIdx, titleColumnIdx, extractFunc = extract_name):
    with open(path, errors = 'ignore') as f:
        csv_reader = csv.reader(f, delimiter=",")
        next(csv_reader)
        author_companies = []
        downloads = []
        titles = []
        for row in csv_reader:
            author_companies.append(row[keyColumnIdx])
            downloads.append(row[downloadColumnIdx])
            titles.append(row[titleColumnIdx])
            
        if (titles):
            authors, companies , _ = extractFunc(author_companies)
        else:
            authors, companies , titles = extractFunc(author_companies)
    with open(savePath, "w", newline="") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter = ',',quoting = csv.QUOTE_MINIMAL)
        csvWriter.writerow(["author", "company", "download", "title", "before parsing"])
        for i in range(len(authors)):
            csvWriter.writerow([authors[i], companies[i], downloads[i], titles[i], author_companies[i]])
        
                

if __name__ == "__main__":
    file1 = "..\80211_mentor_1to573.csv"
    columnIdx1 = 6
    savePath1 = "80211_mentor_1to573_author_info.csv"
    file2= "..\80216_mentor_1to21.csv"
    columnIdx2 = 6
    savePath2 = "80216_mentor_1to21_author_info.csv"
    file3 = "..\grouper_1990to1996.csv"
    columnIdx3 = 3
    savePath3 = "grouper_1990to1996_author_info.csv"
    parse_file(file1, columnIdx1, savePath1, 8, 5)#1919 missing companies, no missing authors
    parse_file(file2, columnIdx2, savePath2, 8, 5)#147 missing companies, no mising authors
    parse_file(file3, columnIdx3, savePath3, 5, -1, extract_name2)