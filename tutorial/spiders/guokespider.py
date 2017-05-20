# -*- coding: utf-8 -*-
import scrapy
from scrapy import  signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import GuokeItem
from  ..tools.common import get_md5

from datetime import datetime
from selenium import webdriver
from lxml import etree

class Guokespider(scrapy.Spider):
    name = 'guoke'
    allowed_domains = ['guokr.com']
    start_urls = [
        'http://www.guokr.com/scientific/'
    ]

    def __init__(self):
        self.browser = webdriver.PhantomJS(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe ")
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print 'browser closed'
        self.browser.quit()

    def parse(self,response):
        message = response.xpath('//div[@id="waterfall"]/div[@class="article"]').extract()
        for m in message:
            l = GuokeItem()
            selector = etree.HTML(m)
            l['title'] = selector.xpath('//h3/a/text()')[0]
            l['message_url'] = selector.xpath('//h3/a/@href')[0]
            l['id'] = get_md5(l['message_url'])
            l['image_url'] = selector.xpath('//a[@href="'+l['message_url']+'"]/img/@src')[0] if selector.xpath('//a[@href="'+l['message_url']+'"]/img/@src') else ''
            l['content'] = selector.xpath('//p[@class="article-summary"]/text()')[0]
            l['add_time'] = datetime.utcnow()
            l['source_from'] = u'果壳网'

            yield  l





