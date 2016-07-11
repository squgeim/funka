# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import traceback
import json
import sys

class OddscheckerPipeline(object):

    def open_spider(self, spider):
        self.conn = psycopg2.connect('dbname=oddschecker user=squgeim')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        game = item['game']
        mid = item['match_id']
        match_name = item['match']
        tournament = item['tournament']
        odds = json.dumps(item['odds'])
        datetime = item['datetime']

        try:
            self.cur.execute('UPDATE odds SET odds=%(odds)s WHERE mid=%(mid)s; '
                'INSERT INTO odds (game, mid, match_name, tournament, odds, datetime) '
                'SELECT %(game)s, %(mid)s, %(match_name)s, %(tournament)s, %(odds)s, %(datetime)s WHERE NOT EXISTS (SELECT 1 from odds WHERE mid=%(mid)s);',
                {'game':game, 'mid':mid, 'match_name':match_name, 'tournament':tournament, 'odds':odds, 'datetime':datetime})
        except psycopg2.Error:
            traceback.print_exc(file=sys.stdout)
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.conn.commit()