# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy.http import Request
import scrapy
from lxml import etree
import urlparse
from scrapy import signals
from selenium import webdriver
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import CrawlSpider, Rule
import tutorial.settings
from ..items import GuinessItem
from ..tools.common import get_md5
import urlparse


class GuinnessSpider(RedisCrawlSpider):
    name = 'guinness'
    allowed_domains = ['guinnessworldrecords.cn']
    # start_urls = [
    #     'http://www.guinnessworldrecords.cn/news'
    # redis-cli lpush gns:start_urls http://www.guinnessworldrecords.cn/news
    # ]
    redis_key = 'gns:start_urls'

    rules = [
        Rule(link_extractor=LinkExtractor(allow=('/news\?page=[0-9]+'))),
        Rule(link_extractor=LinkExtractor(allow=('/news/[0-9]+.*')), callback='parse_item')
    ]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GuinnessSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print 'guinness closed'

    def parse_item(self, response):
        l = GuinessItem()
        l['title'] = response.xpath('//div[@class="page-header block block-11-12"]/h1/text()').extract()[0]
        l['message_url'] = response.url
        l['data_id'] = get_md5(l['message_url'])
        l['content'] = response.xpath('//*[@id="main"]/div/div[2]/div/div[1]/div/div[2]').xpath('string(.)').extract_first().strip()
        l['image_url'] = urlparse.urljoin(response.url, response.xpath('//*[@id="main"]/div/div[2]/div/div[1]/div/figure/img/@src').extract_first())
        l['add_time'] = datetime.utcnow()
        yield l