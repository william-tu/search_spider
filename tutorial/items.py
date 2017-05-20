# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from es_models import DoubanType,GuokeType

class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    message_url = scrapy.Field()
    image_url = scrapy.Field()
    add_time = scrapy.Field()
    source_from = scrapy.Field()

    def save_es(self):
        Dt = DoubanType()
        Dt.id = self['id']
        Dt.title = self['title']
        Dt.content = self['content']
        Dt.message_url = self['message_url']
        Dt.image_url = self['image_url']
        Dt.add_time = self['add_time']
        Dt.source_from = self['source_from']
        Dt.save()


class GuokeItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    message_url = scrapy.Field()
    image_url = scrapy.Field()
    add_time = scrapy.Field()
    source_from = scrapy.Field()

    def save_es(self):
        Gt = GuokeType()
        Gt.id = self['id']
        Gt.title = self['title']
        Gt.content = self['content']
        Gt.message_url = self['message_url']
        Gt.image_url = self['image_url']
        Gt.add_time = self['add_time']
        Gt.source_from = self['source_from']
        Gt.save()


