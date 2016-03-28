# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SjgtwItem(scrapy.Item):
    # define the fields for your item here like:
    dataNum = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    unit = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    brand = scrapy.Field()
    manufacturer = scrapy.Field()
    manufacturer_url = scrapy.Field()
    addition = scrapy.Field()
    unit_price = scrapy.Field()
    texture = scrapy.Field()
    num = scrapy.Field()
    standard = scrapy.Field()
    train_mod = scrapy.Field()
    certify = scrapy.Field()
    preparation = scrapy.Field()
    deliver_or_not = scrapy.Field()
    dis = scrapy.Field()
    url = scrapy.Field()
    pass
