# -*- coding: utf-8 -*-
import scrapy
from scrapy import  signals
from ..items import ZhihuItem
from  ..tools.common import get_md5


from datetime import datetime
from lxml import etree
import urlparse

class GuokeSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['daily.zhihu.com']
    start_urls = [
        'http://daily.zhihu.com'
    ]

    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GuokeSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print 'guoke closed'

    def parse(self,response):
        message = response.xpath('//div[@class="wrap"]').extract()
        for m in message:
            l = ZhihuItem()
            selector = etree.HTML(m)
            l['title'] = selector.xpath('//span[@class="title"]/text()')[0]
            l['message_url'] = urlparse.urljoin(response.url,response.url+selector.xpath('//a/@href')[0])
            l['id'] = get_md5(l['message_url'])
            l['image_url'] = selector.xpath('//a/img/@src')[0]
            l['content'] = ''
            l['add_time'] = datetime.utcnow()
            l['source_from'] = u'知乎日报网'

            yield  l



