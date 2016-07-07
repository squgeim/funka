# -*- coding: utf-8 -*-
import scrapy
from oddschecker.items import FootballItem

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["oddschecker.com"]
    start_urls = (
        'http://www.oddschecker.com/football/football-coupons/major-leagues-cups',
    )
    root_domain = 'http://oddschecker.com'

    def parse(self, response):
        all_links = response.xpath('//td[@class="betting"]/a/@href').extract()
        for link in all_links:
            yield scrapy.Request( self.root_domain + link, callback = self.parse_football_match )

    def parse_football_match(self, response):
        item = FootballItem()
        
        name = response.xpath('//table[@class="eventTable "]/@data-sname').extract_first()
        datetime = response.xpath('//table[@class="eventTable "]/@data-time').extract_first()
        tournament = response.xpath('//table[@class="eventTable "]/@data-ename').extract_first()

        bookkeepers = response.xpath('//tr[@class="eventTableHeader"]/td/aside/a/@title').extract()

        team1, team2 = name.split(' v ')

        team1_odds = response.xpath('//tr[@data-bname="{0}"]/td/text()'.format(team1)).extract()
        team2_odds = response.xpath('//tr[@data-bname="{0}"]/td/text()'.format(team2)).extract()
        draw_odds = response.xpath('//tr[@data-bname="{0}"]/td/text()'.format('Draw')).extract()

        team1_best_odd = response.xpath('//tr[@data-bname="{0}"]/td[contains(concat(" ", @class, " "), " b ")]/@data-o'.format(team1)).extract_first()
        team2_best_odd = response.xpath('//tr[@data-bname="{0}"]/td[contains(concat(" ", @class, " "), " b ")]/@data-o'.format(team2)).extract_first()
        draw_best_odd = response.xpath('//tr[@data-bname="{0}"]/td[contains(concat(" ", @class, " "), " b ")]/@data-o'.format('Draw')).extract_first()

        item['match'] = name
        item['tournament'] = tournament
        item['datetime'] = datetime
        item['team1'] = team1
        item['team2'] = team2
        item['team1_odds'] = {
            'for': team1,
            'best': team1_best_odd,
            'odds': dict(zip(bookkeepers, team1_odds))
        }
        item['team2_odds'] = {
            'for': team2,
            'best': team2_best_odd,
            'odds': dict(zip(bookkeepers, team2_odds))
        }
        item['draw_odds'] = {
            'for': 'Draw',
            'best': draw_best_odd,
            'odds': dict(zip(bookkeepers, draw_odds))
        }

        yield item