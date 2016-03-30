# -*- coding: utf-8 -*-

import scrapy

from sjgtw.items import SjgtwItem
import os
import json
from scrapy import log
import re
import pymongo


class sjgtwSpider(scrapy.Spider):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    name = 'sjgtw'
    allow_domains = ["sjgtw.com"]

    # urls to crawl
    path = os.getcwd()
    f = open('./sjgtw/sjgtw_leaves.json', 'r')
    jsonList = json.load(f)
    f.close()
    start_urls = []
    for jo in jsonList:
        start_urls.append(jo['url'])



    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "clientId=38681443894000; clientId=38681446210000; JSESSIONID=372570A67852F5343A0E9C01BA4F5F6D; Hm_lvt_8908fa41684e227cc7f033849052cd8a=1458723279; Hm_lpvt_8908fa41684e227cc7f033849052cd8a=1458723806; CNZZDATA1256025023=1839444177-1458720018-%7C1458720018"
    }

    def __init__(self):
        connection = pymongo.MongoClient("mongodb://guanxiaoda.cn:27017")
        db = connection['sjgtwdb']
        collection = db['sjgtw_info']
        # item crawled before
        log.msg("loading crawled items from each url...")
        self.urlItems = {}
        pipeline = [
            {
                "$group":{
                    "_id":"$url","count":{"$sum":1}
                }
            }
        ]

        result = list(collection.aggregate(pipeline))
        for i,item in enumerate(result):
            self.urlItems[item['_id']] = item['count']
            if i % 100 == 0 : print(i)
        log.msg("read %d crawled urls" % len(result))
        super(sjgtwSpider, self).__init__()


    def parse(self, response):
        print(">> parsing..." + response.url)
        # calculate complete percent
        count = 0
        resultCount = response.xpath("//div[@class='result']/text()")
        if len(resultCount) > 0:
            text = resultCount[0].extract().encode('utf-8')
            countStr = text[text.find("共")+3:text.find("条")]
            count = int(countStr)
        else:
            line = response.xpath("//table[@id='goodsClassTable']/tbody/tr[not(contains(@id,'child'))]")
            if len(line) > 0:
                count = len(line)
        if count == 0:
            log.msg("no item found on this page : %s" % response.url)
            return
        if response.url in self.urlItems:
            url_crawled_count = self.urlItems[response.url]
            if url_crawled_count:
                percent =  float("%d.00"%url_crawled_count)/float(count)
                if percent > 0.95:
                    log.msg("url has been crawled completely %f : %s " % (percent, response.url))
                    return

        for line in response.xpath("//table[@id='goodsClassTable']/tbody/tr"):

            id = line.xpath("./@id")[0].extract()

            if id.find('child') == -1:
                # - title line -
                item = SjgtwItem()

                dataNum = line.xpath("./@data")
                if len(dataNum) > 0:
                    item['dataNum'] = dataNum[0].extract()
                name = line.xpath('./td[1]/text()')
                if len(name) > 0:
                    item['name'] = name[0].extract()
                model = line.xpath('./td[2]/text()')
                if len(model) > 0:
                    item['model'] = model[0].extract()
                unit = line.xpath('./td[3]/text()')
                if len(unit) > 0:
                    item['unit'] = unit[0].extract()
                price = line.xpath('./td[4]/text()')
                if len(price) > 0:
                    item['price'] = price[0].extract()
                address = line.xpath('./td[5]/text()')
                if len(address) > 0:
                    item['address'] = address[0].extract()
                brand = line.xpath('./td[6]/text()')
                if len(brand) > 0:
                    item['brand'] = brand[0].extract()
                manufacturer = line.xpath('./td[7]/a/text()')
                if len(manufacturer) > 0:
                    item['manufacturer'] = manufacturer[0].extract()
                    item['manufacturer_url'] = "http://www.sjgtw.com%s" % line.xpath("./td[7]/a/@href")[0].extract().encode("utf-8")
                    # href = manufacturer[0].xpath("./..")
                    # print(href)
                    #
                addition = line.xpath('./td[7]/a/text()')
                if len(addition) > 0:
                    item['addition'] = addition[0].extract()
                # - detail line -
                # //table[@id='goodsClassTable']/tbody/tr[@id='row_0']/following-sibling::*[1]
                detailLine = line.xpath("./following-sibling::*[1]")
                upList = detailLine.xpath("./td/div[1]//tr[@trstepprice]//text()")
                if len(upList) > 0:
                    up = ""
                    for u in upList:
                        up += u.extract()
                    item['unit_price'] = up
                infoList = detailLine.xpath("./td/div[2]/dl/dd")
                if len(infoList) > 0:
                    texture = infoList[0].xpath("./text()").extract()
                    item['texture'] = texture
                    num = infoList[1].xpath("./text()").extract()
                    item['num'] = num
                    standard = infoList[2].xpath("./text()").extract()
                    item['standard'] = standard
                    train_mod = infoList[3].xpath("./text()").extract()
                    item['train_mod'] = train_mod
                    certify = infoList[4].xpath("./text()").extract()
                    item['certify'] = certify
                    preparation = infoList[5].xpath("./text()").extract()
                    item['preparation'] = preparation
                item['deliver_or_not'] = None
                dis = detailLine.xpath("./td/div[3]/div/label[contains(@id,'distance')]/span/text()")
                if len(dis) > 0:
                    item['dis'] = dis[0].extract()

                    # item['texture']
                    # item['num']
                    # item['standard']
                    # item['train_mod']
                    # item['certify']
                    # item['preparation']
                    # item['deliver_or_not']
                    # item['dis']
                item['url'] = response.url

                # print(response.url + "{\n" + json.dumps(dict(item)) + "}")
                yield item

        next = response.xpath("//li[@class='next'][1]/a")
        if response.xpath("//li[@class='next'][1]/a"):
            nextPage = next.xpath("./@data-page")[0].extract()
            frmdata = {
                "pageNo": int(nextPage)
            }
            log.msg("request: %s & %s " % (response.url, nextPage))
            yield scrapy.FormRequest(response.url, callback=self.parse, headers=self.headers,
                                     formdata={"pageNo": nextPage})

            # for href in response.xpath('//a[@href]/@href').extract():
            #     if href.find('goodsClass/goodsClassIndex?clickId=6436') == -1:
            #         continue
            #
            #     # print(href)
            #     yield scrapy.Request("http://www.sjgtw.com%s" % href, callback=self.parse_items)

            # def parse_items(self, response):
            # 列表


            # 翻页
