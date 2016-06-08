# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CraigslistPipeline(object):
    def process_item(self, item, spider):
        if item['desc']:
            item['blurb'] = item['desc'][:100]
            item['blurb'] += '...' if len(item['desc']) > 100 else ''
        return item
