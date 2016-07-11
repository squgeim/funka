# -*- coding: utf-8 -*-
import scrapy
from oddschecker.items import GameItem

class OddsSpider(scrapy.Spider):
    name = "odds"
    allowed_domains = ["oddschecker.com"]
    football_urls = [
        'http://www.oddschecker.com/football/football-coupons/major-leagues-cups'
    ]
    horse_urls = [
        'http://www.oddschecker.com/horse-racing/'
    ]
    root_domain = 'http://oddschecker.com'

    def start_requests(self):
        for url in self.football_urls:
            yield scrapy.Request(url, callback = self.parse_football)

        for url in self.horse_urls:
            yield scrapy.Request(url, callback = self.parse_horse)

    def parse_horse(self, response):
        all_links = response.xpath('//a[@class="race-time time"]/@href').extract()
        for link in all_links:
            request = scrapy.Request(self.root_domain + link, callback = self.parse_odds)
            request.meta['game'] = 'horse'
            yield request

    def parse_football(self, response):
        all_links = response.xpath('//td[@class="betting"]/a/@href').extract()
        for link in all_links:
            request = scrapy.Request(self.root_domain + link, callback = self.parse_odds)
            request.meta['game'] = 'football'
            yield request

    def parse_odds(self, response):
        game = response.meta['game']
        item = GameItem()

        item['game'] = game

        match_id = response.xpath('//div[@id="oddsTableContainer"]/table/@data-mid').extract_first()
        name = response.xpath('//div[@id="oddsTableContainer"]/table/@data-sname').extract_first()
        datetime = response.xpath('//div[@id="oddsTableContainer"]/table/@data-time').extract_first()
        tournament = response.xpath('//div[@id="oddsTableContainer"]/table/@data-ename').extract_first()

        bookkeepers = response.xpath('//tr[@class="eventTableHeader"]/td/aside/a/@title').extract()

        teams = response.xpath('//div[@id="oddsTableContainer"]/table/tbody/tr')
        odds = {}

        for team in teams:

            if(game == 'horse'):
                if('eventTableRowNonRunner' in team.xpath('./@class').extract_first().split()): continue

            team_name = team.xpath('./@data-bname').extract_first()
            team_odds = team.xpath('.//td/text()').extract()
            team_best = team.xpath('.//td[contains(concat(" ", @class, " "), " b ")]/@data-o').extract_first()
            odds[team_name] = {
                'for': team_name,
                'odds': dict(zip(bookkeepers,team_odds)),
                'best': team_best
            }

        item['match_id'] = match_id
        item['match'] = name
        item['datetime'] = datetime
        item['tournament'] = tournament
        item['odds'] = odds

        yield item