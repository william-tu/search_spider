# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random

from scrapy import signals
from scrapy.http import HtmlResponse


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        self.user_agent = crawler.settings.get("USER_AGENT_LIST")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # 随机选择user-agent
        ua = random.choice(self.user_agent)
        if ua:
            request.headers.setdefault('User-Agent', ua)


class JspageMoreMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'douban':
            spider.browser.get(request.url)
            for i in xrange(2):
                spider.browser.find_element_by_class_name('a_more').click()
                time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, request=request,
                                encoding='utf-8')
        elif spider.name == 'guoke':
            spider.browser.get(request.url)
            for i in xrange(2):
                js = "var q=document.documentElement.scrollTop=10000"
                spider.browser.execute_script(js)
                time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, request=request,
                                encoding='utf-8')
        return None
