# -*- coding: utf-8 -*-
#author: zhenkai wang
#date: 2018 Sept 08
import scrapy, re
import sys
sys.path.append("..\spiders")
from abstractGrouper import GrouperAPI

class Grouper2Spider(GrouperAPI):
    #this code is to crawl down table information during 1990-1996 in grouper website
    #this version did not crawl down the doc files.
    name = 'grouper2'
    allowed_domains = ['grouper.ieee.org']
    start_urls = ['http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/']
    # start_urls = ['http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/1990_docs/table.html']
    def parse_table(self, response):
        '''
        1990-1996
        Year	DCN	Rev	Title	File	Scanned PDF Filename	PDF Pages	Scanned PDF Notes
        1997 - 2000
        Year	DCN	Rev	SubGroup	Title	File
        '''

        rows = response.xpath('//tr')[1:]
        Year = []
        DCN = []
        Rev = []
        SubGroup = []
        Title = []#there can be some "void" in title
        Pdf = []
        for i in range(len(rows)):
            Year.append(self.getRow(rows[i], 1))
            DCN.append(self.getRow(rows[i], 2))
            Rev.append(self.getRow(rows[i], 3))
            SubGroup.append(self.getRow(rows[i], 4))
            Title.append(self.getRow(rows[i], 5))
            Pdf.append(self.getUrl(rows[i], 6, response))

        # Year = self.getRow(rows, 1)
        # DCN = self.getRow(rows, 2)
        # Rev = self.getRow(rows, 3)#sometime is is " " (space) in the html instead of "&nbsp"
        # Title = self.getRow(rows, 4)
        # Doc = self.getUrl(rows, 5, response)
        # ScannedPdf = self.getUrl(rows, 6, response)
        # Note = self.getRow(rows, 8)
        for i in range(len(rows)):
            yield {'Year': Year[i],
            'DCN' : DCN[i],
            'Rev' : Rev[i],
            'SubGroup' : SubGroup[i],
            'Title' : Title[i],
            'pdf' : Pdf[i],
            'currPage' : response.url
            }


    def parse(self, response):
        allTables = response.xpath('//a[contains(@href, "_docs/table.html")]/@href').extract()
        allTablesUrls = [response.urljoin(halfUrl) for halfUrl in allTables]
        print(allTablesUrls)
        yield {'Year':'Year', 'DCN':'DCN', 'Rev':'Rev', 'SubGroup':'SubGroup', 'Title':'Title', 'Pdf':'Pdf', 'CurrPage':'CurrPage'}
        for url in allTablesUrls[7:]:#these tables are in the same type
            yield scrapy.Request(url, callback = self.parse_table)
#
#    def getRow(self, row, idx):
#        #if the content is '\xa0' means that it is empty record, we need to replace it into null
#        result = row.xpath('./td[' + str(idx) + ']/text()')
#        if (result):
#            return [("null" if ((len(re.findall(r'\xa0', value)) >0)) else value) for value in result.extract()]
#        else:
#            return "null"
#    def getUrl(self, rows, idx, response):
#        rawData = rows.xpath('./td[' + str(idx) + ']')
#        if len(rawData) == 0:
#            return "null"
#        result = []
#        for row in rawData.extract():
#            p1 = r'href=\"(.*)\"'
#            searchResult = re.findall(p1, row)
#            if (searchResult):
#                result.append(response.urljoin(searchResult[0]))
#            else:
#                result.append("null")
#        return result
