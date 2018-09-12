# -*- coding: utf-8 -*-
import scrapy, re

'''
data description:
author attribute:
1. null Void means no b_data_row
2. (Mike Trompower - Aironet)
   (Vic Hayes, Lucent Technologies, Chair)
  (Vic Hayes, Chair, Lucent Technologies)
  (Simon Black, Symbionics)
3. those line has no author-company info but has the title
  we need to indentify them
'''
class GroupernewSpider(scrapy.Spider):
    #this code is to crawl down table information during 1990-1996
    name = 'grouperNew'
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
        Rev = []
        Title = []
        Doc = []
        ScannedPdf = []
        Note = []
        for i in range(len(rows)):
            Year.append(self.getRow(rows[i], 1))
            DCN.append(self.getRow(rows[i], 2))
            Rev.append(self.getRow(rows[i], 3))
            Title.append(self.getRow(rows[i], 4))
            Doc.append(self.getUrl(rows[i], 5, response))
            ScannedPdf.append(self.getUrl(rows[i], 6, response))
            Note.append(self.getRow(rows[i], 8))
        # Year = self.getRow(rows, 1)
        # DCN = self.getRow(rows, 2)
        # Rev = self.getRow(rows, 3)#sometime is is " " (space) in the html instead of "&nbsp"
        # Title = self.getRow(rows, 4)
        # Doc = self.getUrl(rows, 5, response)
        # ScannedPdf = self.getUrl(rows, 6, response)
        # Note = self.getRow(rows, 8)
        for i in range(len(rows)):
            yield {'Year' : Year[i],
            'DCN' : DCN[i],
            'Rev' : Rev[i],
            'Title' : Title[i],
            'Doc' : Doc[i],
            'ScannedPdf':ScannedPdf[i],
            'Note' : Note[i],
            'currPage' : response.url
            }


    def parse(self, response):
        allTables = response.xpath('//a[contains(@href, "_docs/table.html")]/@href').extract()
        allTablesUrls = [response.urljoin(halfUrl) for halfUrl in allTables]
        print(allTablesUrls)
        yield {'Year':'Year', 'DCN':'DCN', 'Rev':'Rev', 'Title':'Title', 'Doc' : 'Doc', 'ScannedPdf':'ScannedPdf', 'Note' : 'Note', 'CurrPage':'CurrPage'}
        for url in allTablesUrls[0:7]:#these tables are in the same type
            yield scrapy.Request(url, callback = self.parse_table)

    def getRow(self, row, idx):
        #if the content is '\xa0' means that it is empty record, we need to replace it into null
        result = row.xpath('./td[' + str(idx) + ']/text()')
        if (result):
            return [("null" if ((len(re.findall(r'\xa0', value)) >0)) else value) for value in result.extract()]
        else:
            return "null"
    def getUrl(self, rows, idx, response):
        rawData = rows.xpath('./td[' + str(idx) + ']')
        if len(rawData) == 0:
            return "null"
        result = []
        for row in rawData.extract():
            p1 = r'href=\"(.*)\"'
            searchResult = re.findall(p1, row)
            if (searchResult):
                result.append(response.urljoin(searchResult[0]))
            else:
                result.append("null")
        return result
