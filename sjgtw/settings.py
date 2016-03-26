# -*- coding: utf-8 -*-

# Scrapy settings for sjgtw project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sjgtw'
DOWNLOAD_DELAY = 5
SPIDER_MODULES = ['sjgtw.spiders']
NEWSPIDER_MODULE = 'sjgtw.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'sjgtw (+http://www.yourdomain.com)'


# Retry many times since proxies often fail
RETRY_TIMES = 3
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    # # Fix path to this module
    # 'sjgtw.middlewares.RandomProxy': 100,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

MONGODB_SERVER = 'guaxiaoda.cn'
MONGODB_PORT = 27017
MONGODB_DB = 'sjgtwdb'
MONGODB_COLLECTION_LINKS = 'sjgtw_catalog'
MONGODB_COLLECTION = 'sjgtw_goods'

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = '/Users/guanxiaoda/Documents/workspace/scrapy/sjgtw/proxys.txt'