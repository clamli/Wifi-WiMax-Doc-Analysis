#author: zhenkai wang
#date: 2018 Sept 08
import scrapy


class MentorSpider(scrapy.Spider):
    #this code is used for crawl down all the information from mentor website, final version
    #this version did not try to seperate the author and affiliation
    name = "mentor"
    allowed_domians = ["mentor.ieee.org"];
    # start_urls = ["https://mentor.ieee.org/802.11/documents"]#switch to this when you want the information in 802.11
    start_urls = ["https://mentor.ieee.org/802.16/documents"]
    # start_urls = ["https://mentor.ieee.org/802.11/documents?n=505"]




    def parse(self, response):
        isGoNext = True#iterate to next page or not
        table = response.xpath('//tr[contains(@class, "b_data_row")]')
        num = len(table)
        dcnInfo = table.xpath('.//td[@class="dcn_ordinal"]/text()').extract()
        timeInfo = table.xpath('./td/div/text()').extract()
        download = table.xpath('./td[@class="list_actions"]/a/@href').extract()
        longInfo = table.xpath('./td[@class="long"]/text()').extract()
        groupInfo = table.xpath('./td[5]/text()').extract()
        CreatedTime = []
        Year = []
        DCN = []
        Rev = []
        Group = []
        Title = []
        Author = []
        UploadedTime = []
        yield {'CreatedTime' : 'CreatedTime',
        'Year' : 'Year',
        'DCN' : 'DCN',
        'Rev' : 'Rev',
        'Group' : 'Group',
        'Title' : 'Title',
        'Author' : 'Author',
        'UploadedTime' :'UploadedTime',
        'Download' : 'Actions',
        'CurrPage' : 'CurrPage'
        }

        for i in range(num):
            CreatedTime.append(timeInfo[i*2])
            UploadedTime.append(timeInfo[i*2 + 1])
            Year.append(dcnInfo[i*3])
            DCN.append(dcnInfo[i*3 + 1])
            Rev.append(dcnInfo[i*3 + 2])
            Group.append(groupInfo[i])
            Title.append(longInfo[i*2])
            Author.append(longInfo[i*2 + 1])
        for i in range(num):
            yield {'Created Time': CreatedTime[i],
            'Year': Year[i],
            'DCN' : DCN[i],
            'Rev': Rev[i],
            'Group': Group[i],
            'Title': Title[i],
            'Author':Author[i],
            'Upload Time': UploadedTime[i],
            'dowload':response.urljoin(download[i]),
            'currPage':response.url}
        if isGoNext:
            nextPage = response.xpath('//div[@class="pager"]//a')[-1]
            nextPage_url = nextPage.xpath('./@href').extract()[0]
            absolute_nextPage_url = response.urljoin(nextPage_url)
            yield scrapy.Request(absolute_nextPage_url)
