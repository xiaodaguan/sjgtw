# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.exceptions import DropItem


class SjgtwPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient("mongodb://guanxiaoda.cn:27017")
        db = connection['sjgtwdb']

        self.collection = db['sjgtw_info']

    def process_item(self, item, spider):
        valid = True
        if item['name'] and item['model'] and item['price']:
            valid = True
        else:
            valid = False
            DropItem('info not complete %s ' % item['name'])

        if valid:
            self.collection.insert(dict(item))
            log.msg("item wrote to mongodb database %s/%s" % ('sjgtwdb', 'sjgtw_info'))
        return item
