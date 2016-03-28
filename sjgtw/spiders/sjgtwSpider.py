# -*- coding: utf-8 -*-

import scrapy

from sjgtw.items import SjgtwItem
import os
import json
from scrapy import log


class sjgtwSpider(scrapy.Spider):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    name = 'sjgtw'
    allow_domains = ["sjgtw.com"]
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

    def parse(self, response):
        print(">> parsing..." + response.url)
        for line in response.xpath("//table[@id='goodsClassTable']/tbody/tr"):

            id = line.xpath("./@id")[0].extract()
            dataNum = line.xpath("./@data").extract()
            if id.find('child') == -1:
                # - title line -
                item = SjgtwItem()
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
