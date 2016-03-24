# -*- coding: utf-8 -*-

import scrapy
from sjgtw.items import SjgtwItem
from scrapy.selector import Selector
from scrapy.http import FormRequest


class sjgtwSpider(scrapy.Spider):
    name = 'sjgtw'
    allow_domains = ["sjgtw.com"]
    start_urls = ['http://www.sjgtw.com/goodsClass/goodsClassIndex?clickId=6436']
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "clientId=38681443894000; clientId=38681446210000; JSESSIONID=372570A67852F5343A0E9C01BA4F5F6D; Hm_lvt_8908fa41684e227cc7f033849052cd8a=1458723279; Hm_lpvt_8908fa41684e227cc7f033849052cd8a=1458723806; CNZZDATA1256025023=1839444177-1458720018-%7C1458720018"
    }

    def parse(self, response):
        print(">> parsing..." + response.url)
        for line in response.xpath("//table[@id='goodsClassTable']/tbody/tr"):

            id = line.xpath("./@id")[0].extract()
            if id.find('child') == -1:
                # 标题行
                item = SjgtwItem()
                item['name'] = line.xpath('./td[1]/text()')[0].extract()
                item['model'] = line.xpath('./td[2]/text()')[0].extract()
                print(item['name'] + response.url)
                yield item

        next = response.xpath("//li[@class='next'][1]/a")
        if response.xpath("//li[@class='next'][1]/a"):
            nextPage = next.xpath("./@data-page")[0].extract()
            frmdata = {
                "pageNo": int(nextPage)
            }
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

