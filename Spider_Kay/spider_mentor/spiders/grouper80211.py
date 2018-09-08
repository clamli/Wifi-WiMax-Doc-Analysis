# -*- coding: utf-8 -*-
import scrapy
import re

class Grouper80211Spider(scrapy.Spider):
    name = 'grouper80211'
    allowed_domains = ['grouper.ieee.org']#should not include http prefix
    start_urls = ['http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/']
    # start_urls = ['http://grouper.ieee.org/groups/802/11/Documents/DocumentArchives/1990_docs/table.html']
    def parse_table(self, response):
        '''
        1990-1996
        Year	DCN	Rev	Title	File	Scanned PDF Filename	PDF Pages	Scanned PDF Notes
        1997 - 2000
        Year	DCN	Rev	SubGroup	Title	File
        '''
        rows = response.xpath('//tr')
        Year = self.getRow(rows, 1)
        DCN = self.getRow(rows, 2)
        Rev = self.getRow(rows, 3)#sometime is is " " (space) in the html instead of "&nbsp"
        Title = self.getRow(rows, 4)
        Doc = self.getUrl(rows, 5, response)
        ScannedPdf = self.getUrl(rows, 6, response)
        Note = self.getRow(rows, 8)
        for i in range(len(rows)):
            yield {'Year' : Year[i],
            'DCN' : DCN[i],
            'Rev' : Rev[i],
            'Title' : Title[i],
            'Doc' : Doc[i],
            'ScannedPd':ScannedPdf[i],
            'Note' : Note[i],
            'currPage' : response.url
            }


    def parse(self, response):
        allTables = response.xpath('//a[contains(@href, "_docs/table.html")]/@href').extract()
        allTablesUrls = [response.urljoin(halfUrl) for halfUrl in allTables]
        print(allTablesUrls)
        for url in allTablesUrls[1:8]:#these tables are in the same type
            yield scrapy.Request(url, callback = self.parse_table)

    def getRow(self, rows, idx):
        #if the content is '\xa0' means that it is empty record, we need to replace it into null
        result = rows.xpath('./td[' + str(idx) + ']/text()').extract()
        return [("null" if ((len(re.findall(r'\xa0', value)) >0)) else value) for value in result]
    def getUrl(self, rows, idx, response):
        rawData = rows.xpath('./td[' + str(idx) + ']').extract()
        result = []
        for row in rawData:
            p1 = r'href=\"(.*)\"'
            searchResult = re.findall(p1, row)
            if (searchResult):
                result.append(response.urljoin(searchResult[0]))
            else:
                result.append("null")
        return result
