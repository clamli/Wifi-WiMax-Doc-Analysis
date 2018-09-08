import scrapy


class MentorSpider(scrapy.Spider):
    #this code is used for crawl down all the information from mentor website
    name = "mentor"
    allowed_domians = ["mentor.ieee.org"];
    # start_urls = ["https://mentor.ieee.org/802.11/documents"]
    start_urls = ["https://mentor.ieee.org/802.16/documents"]
    # start_urls = ["https://mentor.ieee.org/802.11/documents?n=505"]




    def parse(self, response):
        isGoNext = True#iterate to next page or not
        # //basic version
                # mainInfo = response.xpath("//td/text()").extract()
                # num = int(len(mainInfo) / 6);
                # timeInfo = response.xpath('//*[contains(@class, "b_data_row")]//td/div/text()').extract()
                # download = response.xpath('//*[@class="list_actions"]/a/@href').extract();

        # path = "F:\WireLessNLPGRA\wenjian.csv"
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
        'Download' : 'Download',
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
            # CreatedTime.append(timeInfo[i*2])
            # Year.append(mainInfo[i*6])
            # DCN.append(mainInfo[i*6 + 1])
            # Rev.append(mainInfo[i*6 + 2])
            # Group.append(mainInfo[i*6 + 3])
            # Title.append(mainInfo[i*6 + 4])
            # Author.append(mainInfo[i*6 + 5])
            # UploadedTime.append(timeInfo[i*2 + 1])
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



        # wb = xlwt.Workbook()
        # sheet = wb.add_sheet("page1_80211")
        #
        # for i in range(num):
        #     sheet.write(i, 0, timeInfo[i*2])
        #     sheet.write(i, 1, mainInfo[i*6])
        #     sheet.write(i, 2, mainInfo[i*6 + 1])
        #     sheet.write(i, 3, mainInfo[i*6 + 2])
        #     sheet.write(i, 4, mainInfo[i*6 + 3])
        #     sheet.write(i, 5, mainInfo[i*6 + 4])
        #     sheet.write(i, 6, mainInfo[i*6 + 5])
        #     sheet.write(i, 7, timeInfo[i*2 + 1])
        #     sheet.write(i, 8, download[i])
        # wb.save(path)
        # print("successfully write in " + str(num) + " rows")
#        yield Request(url)

        # for i in range(num):
        #     yield {"created time": timeInfo[i*2],
        #          "year": mainInfo[i*6],
        #          "DCN": mainInfo[i*6 + 1],
        #          "Rev": mainInfo[i*6 + 2],
        #          "Group": mainInfo[i*6 + 3],
        #          "Title": mainInfo[i*6 + 4],
        #          "Author": mainInfo[i*6 + 5],
        #          "uplodated time": timeInfo[i*2 + 1],
        #          "dowload": download[i]}
