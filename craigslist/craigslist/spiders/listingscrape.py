# -*- coding: utf-8 -*-
import scrapy

from craigslist.items import CraigslistItem

class ListingscrapeSpider(scrapy.Spider):
    name = "listingscrape"
    allowed_domains = ["tampa.craigslist.org"]
    start_urls = (
        'https://tampa.craigslist.org/search/apa',
    )

    def parse(self, response):
        url_start = ''.join(list( response.url.partition( \
                        response.url.split('/')[2] ))[:2])
    
        links = response.xpath('//a[@class="hdrlnk"]/@href').extract()
        for link in links:
            abs_url = url_start + link
            yield scrapy.Request(abs_url, callback=self.parse_detail)

        try:
            next_url = url_start + response\
                    .xpath('//a[@class="button next"]/@href').extract_first()
        
            yield scrapy.Request(next_url, callback=self.parse)
        except TypeError:
            print('Complete.')
        
    
    def parse_detail(self, response):
    
        url_start = ''.join(list( response.url.partition( \
                        response.url.split('/')[2] ))[:2])
                        
        item = CraigslistItem()
        
        title = response.xpath('//span[@id="titletextonly"]/text()')\
                .extract_first()
        
        price = response.xpath('//span[@class="price"]/text()').extract_first()
        
        attributes = response.xpath('//p[@class="attrgroup"]/span/b/text()')\
                .extract()

        address = response.xpath('//div[@class="mapaddress"]/text()')\
                .extract_first()

        latitude = response.xpath('//div[@id="map"]/@data-latitude')\
                .extract_first()

        longitude = response.xpath('//div[@id="map"]/@data-longitude')\
                .extract_first()
        
        desc_xpath = response.xpath('//section[@id="postingbody"]/text()')

        desc_contact_link = desc_xpath.xpath('//a[@class="showcontact"]/@href')\
                .extract_first()

        if desc_contact_link:
            desc_request = scrapy.Request( url_start + desc_contact_link,
                            callback=self.parse_desc )
            desc_request.meta['item'] = item
            yield desc_request
        else:
            desc = '\n'.join(line.strip() for line in desc_xpath.extract())
            item['desc'] = desc

        item['url'] = response.url
        item['title'] = title
        item['price'] = price
        item['bedroom'] = attributes[0] if len(attributes) >= 1 else None
        item['bathroom'] = attributes[1] if len(attributes) >= 2 else None
        item['area'] = attributes[2] if len(attributes) == 3 else None
        item['address'] = address
        item['latlong'] = (latitude, longitude)
        
        try:
            reply_url = url_start + response\
                .xpath('//span[@class="replylink"]/a[@id="replylink"]/@href')\
                .extract_first()
            request = scrapy.Request(reply_url, callback=self.parse_contact)
            request.meta['item'] = item
            yield request
            
        except TypeError:
            item['phone'] = None
            item['email'] = None
            yield item

    def parse_desc(self, response):
        item = response.meta['item']
        desc = '\n'.join(line.strip() for line in response.xpath('//')\
                .extract())
        item['desc'] = desc
        yield item
        
    def parse_contact(self, response):
        item = response.meta['item']
        
        try:
            phone = ' '.join(
                response.xpath('//a[starts-with(@href, "tel:")]/'
                'following-sibling::ul/li/text()').extract_first().split()[1:]
            )
        except AttributeError:
            phone = None

        email = response.xpath('//a[@class="mailapp"]/text()').extract_first()

        item['phone'] = phone
        item['email'] = email

        return item
