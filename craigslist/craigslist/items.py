# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    area = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()