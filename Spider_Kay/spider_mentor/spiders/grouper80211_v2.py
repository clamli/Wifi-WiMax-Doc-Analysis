# -*- coding: utf-8 -*-
import scrapy
import re

class Grouper80211V2Spider(scrapy.Spider):
    name = 'grouper80211_V2'
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
        


        Year2 = self.getRow(secondRows, 1)
        DCN2 = self.getRow(secondRows, 2)
        Rev2 = self.getRow(secondRows, 3)
        SubGroup2 = self.getRow(secondRows,4)
        Title2 = self.getRow(secondRows, 5)
        File2 = self.getUrl(secondRow, 6)
        for i in range(len(secondRows)):
            yield {'Year': Year2[i],
            'DCN' : DCN2[i],
            'Rev' : Rev2[i],
            'SubGroup' : SubGroup2[i],
            'Title' : Title2[i],
            'File2' : File2[i],
            'currPage' : response.url
            }

    def parse(self, response):
        allTables = response.xpath('//a[contains(@href, "_docs/table.html")]/@href').extract()
        allTablesUrls = [response.urljoin(halfUrl) for halfUrl in allTables]
        print(allTablesUrls)
        for url in allTablesUrls[8:]:
            yield scrapy.Request(url, callback = self.parse_table)

    def getRow(self, rows, idx):
        #if the content is '\xa0' means that it is empty record, we need to replace it into null
        result = rows.xpath('./td[' + str(idx) + ']/text()').extract()
        return [("null" if (re.findall(r'\xa0', value)) else value) for value in result]
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
