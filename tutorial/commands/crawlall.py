# -*- coding: utf-8 -*-
import logging

from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        settings = get_project_settings()

        spider_loader = self.crawler_process.spider_loader
        for spidername in args or spider_loader.list():
            logging.info("Start crawlall :%r" % spidername)
            self.crawler_process.crawl(spidername)

        self.crawler_process.start()
