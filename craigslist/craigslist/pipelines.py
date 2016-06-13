# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CraigslistPipeline(object):
    def process_item(self, item, spider):
        if item['images']:
            item['image_locations'] = []
            for image_dict in item['images']:
                item['image_locations'].append(image_dict['path'])
        return item