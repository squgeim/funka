# -*- coding: utf-8 -*-
import scrapy
from oddschecker.items import HorseracingItem

class HorseSpider(scrapy.Spider):
    name = "horse"
    allowed_domains = ["oddschecker.com"]
    start_urls = (
        'http://www.oddschecker.com/horse-racing/',
    )
    root_domain = 'http://oddschecker.com'

    def parse(self, response):
        all_links = response.xpath('//a[@class="race-time time"]/@href').extract()
        for link in all_links:
            yield scrapy.Request(self.root_domain + link, callback = self.parse_horseracing)

    def parse_horseracing(self, response):
        item = HorseracingItem()

        name = response.xpath('//div[@id="oddsTableContainer"]/table/@data-sname').extract_first()
        datetime = response.xpath('//div[@id="oddsTableContainer"]/table/@data-time').extract_first()
        tournament = response.xpath('//div[@id="oddsTableContainer"]/table/@data-ename').extract_first()

        bookkeepers = response.xpath('//tr[@class="eventTableHeader"]/td/aside/a/@title').extract()

        horses = response.xpath('//div[@id="oddsTableContainer"]/table/tbody/tr')
        odds = {}

        for horse in horses:

            if('eventTableRowNonRunner' in horse.xpath('./@class').extract_first().split()): continue

            horse_name = horse.xpath('./@data-bname').extract_first()
            horse_odds = horse.xpath('.//td/text()').extract()
            horse_best = horse.xpath('.//td[contains(concat(" ", @class, " "), " b ")]/@data-o').extract_first()
            odds[horse_name] = {
                'for': horse_name,
                'odds': dict(zip(bookkeepers,horse_odds)),
                'best': horse_best
            }

        item['match'] = name
        item['datetime'] = datetime
        item['tournament'] = tournament
        item['odds'] = odds

        yield item