# -*- coding: utf-8 -*-
import urlparse
from datetime import datetime

import scrapy
from lxml import etree
from scrapy import signals

from ..items import ZhihuItem
from ..tools.common import get_md5


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['daily.zhihu.com']
    start_urls = [
        'http://daily.zhihu.com'
    ]

    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ZhihuSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print 'zhihu closed'

    def parse(self, response):
        message = response.xpath('//div[@class="wrap"]').extract()
        for m in message:
            selector = etree.HTML(m)
            yield scrapy.Request(url=urlparse.urljoin(response.url, response.url + selector.xpath('//a/@href')[0]),
                                 callback=self.parse_content)

    def parse_content(self, response):
        print response
        l = ZhihuItem()
        l['title'] = response.xpath('//h1[@class="headline-title"]/text()').extract()[0]
        l['message_url'] = response.url
        l['id'] = get_md5(l['message_url'])
        l['image_url'] = response.xpath('//div[@class="img-wrap"]/img/@src').extract()[0]
        l['add_time'] = datetime.utcnow()
        l['source_from'] = u'知乎日报网'
        content = ''.join(response.xpath('//div[@class="content"]/p/text()').extract())
        if len(content) > 100:
            l['content'] = content[:100]
        else:
            l['content'] = content
        yield l
