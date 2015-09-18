# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Train(scrapy.Item):
    station = scrapy.Field()
    stops = scrapy.Field()
