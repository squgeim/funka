import scrapy

from craigslist.items import CraigslistItem

class CraigsSpider(scrapy.Spider):

    name = "craigs"
    allowed_domains = ["tampa.craigslist.org"]
    start_urls = [
        "https://tampa.craigslist.org/pnl/apa/5577150767.html"
    ]

    def parse(self, response):
        item = CraigslistItem()

        title = response.xpath('//span[@id="titletextonly"]/text()')\
                .extract_first()
        desc = '\n'.join(line.strip() for line in \
                response.xpath('//section[@id="postingbody"]/text()').extract())
        price = response.xpath('//span[@class="price"]/text()').extract_first()
        attributes = [ int(x) for x in response\
                .xpath('//p[@class="attrgroup"]/span/b/text()').extract() ]

        item['title'] = title
        item['desc'] = desc
        item['price'] = price
        item['bedroom'] = attributes[0]
        item['bathroom'] = attributes[1]
        item['area'] = attributes[2] if len(attributes) == 3 else None

        reply_url = response.url.replace('pnl','reply/tpa')[:-5]
        request = scrapy.Request(reply_url, callback=self.parse_contact)
        request.meta['item'] = item
        return request

    def parse_contact(self, response):
        item = response.meta['item']

        phone_xpath, email_xpath, _, _ = response.xpath('//ul')

        phone = ' '.join( 
            phone_xpath.xpath('li/text()').extract_first().split()[1:]
            )
        email = email_xpath.xpath('li/a/text()').extract_first()

        item['phone'] = phone
        item['email'] = email

        yield item
