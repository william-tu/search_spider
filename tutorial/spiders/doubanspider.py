# -*- coding: utf-8 -*-
import scrapy
from scrapy import  signals
from ..items import DoubanItem
from ..tools.common import get_md5

from selenium import webdriver
from datetime import datetime
from lxml import etree



class DoubanSpider(scrapy.Spider):
	name = 'douban'
	allowed_domains = ['douban.com']
	start_urls = [
		'https://www.douban.com/explore/'
	]

	def __init__(self):
		self.browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe ")


	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(DoubanSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signals.spider_closed)
		return spider


	def spider_closed(self,spider):
		print 'browser closed'
		self.browser.quit()

	def parse(self,response):

		message = response.xpath('//*[@id="gallery_main_frame"]/div[@class="item"]').extract()
		for m in message:
			l = DoubanItem()
			selector = etree.HTML(m)
			l['title'] = selector.xpath('//div[@class="title"]/a/text()')[0].strip()
			l['content'] = selector.xpath('//p/a/text()')[0].strip() if selector.xpath('//p/a/text()') else \
				','.join(selector.xpath('//span/@style')).replace('background-image:url(','').replace(')','').strip()
			l['message_url'] = selector.xpath('//div[@class="title"]/a/@href')[0]
			l['id'] = get_md5(l['message_url'])
			if selector.xpath('//div[@class="pic"]/a/@style'):
				l['image_url'] = selector.xpath('//div[@class="pic"]/a/@style')[0][21:-1]
			elif l['content'].startswith('https'):
				l['image_url'] = selector.xpath('//div[@class="first-pic"]/a/img/@src')[0]
			else:
				l['image_url'] = ''
			l['source_from'] = u'豆瓣'
			l['add_time'] = datetime.utcnow()
			yield l




