#author: zhenkai wang
#data:2018 Sept 11

import scrapy, re
from abc import ABCMeta, abstractmethod
class GrouperAPI(scrapy.Spider):
    @abstractmethod
    def parse(self, response):
        pass
    @abstractmethod
    def parse_table(self, response):
        pass

    def processData(self, value):
        isEmpty = (len(re.findall(r'\xa0', value)) > 0) | (value.strip() == "")
        if (isEmpty):
            return "null"
        else:
            return value.strip()

    def getRow(self, row, idx):
        #if the content is '\xa0' means that it is empty record, we need to replace it into null
        result = row.xpath('./td[' + str(idx) + ']/text()').extract()
        if (result):
            return [self.processData(value) for value in result]
        else:
            return "null"



    def getUrl(self, rows, idx, response):
        rawData = rows.xpath('./td[' + str(idx) + ']')
        if len(rawData) == 0:
            return "null"
        result = []
        for row in rawData.extract():
            p1 = r'href=\"(.*?)\"'
            searchResult = re.findall(p1, row)

            if (searchResult):
                urls = [response.urljoin(url) for url in searchResult]
                result.append(";".join(urls))
            else:
                result.append("null")
        return result
