# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

from similarweb.items import SimilarwebItem
from selenium.common.exceptions import NoSuchElementException as noelm

class MonsterSpider(scrapy.Spider):
    name = "monster"
    allowed_domains = ["www.similarweb.com"]
    start_urls = (
        'https://www.similarweb.com/website/monster.com',
    )

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        print(response.url)
        item = SimilarwebItem()
        self.driver.get(response.url)
        item['similarweburl'] = response.url
        try:
            item['domain'] = self.driver.find_element_by_xpath('//div[@class="stickyHeader-info"]/div/a').get_attribute('href')
        except noelm:
           item['domain'] = None
        
        try:
           item['desc'] = chrome.find_element_by_xpath('//div[@class="stickyHeader-info"]/div/div[@class="analysis-descriptionText"]').text
        except noelm:
           item['desc'] = None

        try:
            globl_elm = chrome.find_element_by_xpath('//div[@class="rankingItems"]/div[@data-rank-subject="Global"]')
            item['ranks_global_rank'] = globl_elm.find_element_by_xpath('.//div[@class="rankingItem-content"]/div/span').text
        except noelm:
            item['ranks_global_rank'] = None

        try:
            country_elm = chrome.find_element_by_xpath('//div[@class="rankingItems"]/div[@data-rank-subject="Country"]')
            item['ranks_country_rank'] = country_elm.find_element_by_xpath('.//div[@class="rankingItem-content"]/div/span').text
        except noelm:
            item['ranks_country_rank'] = None

        try:
            catg_elm = chrome.find_element_by_xpath('//div[@class="rankingItems"]/div[@data-rank-subject="Category"]')
            item['ranks_category_rank'] = catg_elm.find_element_by_xpath('.//div[@class="rankingItem-content"]/div/span').text
            catg_desc = catg_elm.find_element_by_css_selector('.rankingItem-subTitle').text.split(' > ')
            item['ranks_category_main_catg'] = catg_desc[0] if len(catg_desc) > 0 else None
            item['ranks_category_sub_catg'] = catg_desc[1] if len(catg_desc) > 1 else None
        except noelm:
            item['ranks_category_rank'] = None
            item['ranks_category_main_catg'] = None
            item['ranks_category_sub_catg'] = None
             
        try:
            header_elm = chrome.find_element_by_css_selector('.js-analysisHeader')
            item['engagement_date'] = header.text.split('\n')[0].split('(')[-1].split(')')[0]
        except noelm:
            item['engagement_date'] = None
        
        try:
            visits = chrome.find_element_by_css_selector('.engagementInfo-content[data-type="visits"]')
            item['engagement_total_visits'] = visits.find_element_by_css_selector('.engagementInfo-value').text
        except noelm:
            item['engagement_total_visits'] = None

        try:
            time = chrome.find_element_by_css_selector('.engagementInfo-content[data-type="time"]')
            item['engagement_avg_time_on_page'] = time.find_element_by_css_selector('.engagementInfo-value').text
        except noelm:
            item['engagement_avg_time_on_page'] = None

        try:
            page_view = chrome.find_element_by_css_selector('.engagementInfo-content[data-type="ppv"]')
            item['engagement_avg_page_views'] = page_view.find_element_by_css_selector('.engagementInfo-value').text
        except noelm:
            item['engagement_avg_page_views'] = None

        try:
            bounce_rate = chrome.find_element_by_css_selector('.engagementInfo-content[data-type="bounce"]')
            item['engagement_bounce_rate'] = page_view.find_element_by_css_selector('.engagementInfo-value').text
        except noelm:
            item['engagement_bounce_rate'] = None

        try:
            countries = chrome.find_element_by_id('geo-countries-accordion')
            item['traffic_by_countries'] = [ {'Country': country.find_element_by_css_selector('.country-name').text,
                    'Percentage': country.find_element_by_css_selector('.traffic-share-value').text } \
                    for country in countries.find_elements_by_css_selector('.accordion-group') ]
        except noelm:
            item['traffic_by_countries'] = None

        try:
            direct = chrome.find_element_by_css_selector('.trafficSourcesChart-item.direct')
            item['traffic_sources_direct_percent'] = direct.find_element_by_css_selector('.trafficSourcesChart-value').text
        except noelm:
            item['traffic_sources_direct_percent'] = None

        try:
            item['traffic_sources_referrals_percent'] = chrome.find_element_by_css_selector('.subheading-value.referrals').text
        except noelm:
            item['traffic_sources_referrals_percent'] = None

        try:
            refs = chrome.find_elements_by_css_selector('.referralsSites.referring .websitePage-listItemTitle')
            item['traffic_sources_referrals_top_referring_domains'] = [ {'Domain' : domain.text} for domain in refs ]
        except noelm:
            item['traffic_sources_referrals_top_referring_domains'] = None

        try:
            dest = chrome.find_elements_by_css_selector('.referralsSites.destination .websitePage-listItemTitle')
            item['traffic_sources_referrals_top_destination_domains'] = [ {'Domain' : domain.text} for domain in dest ]
        except noelm:
            item['traffic_sources_referrals_top_destination_domains'] = None

        try:
            item['traffic_sources_search_percent'] = chrome.find_element_by_css_selector('.subheading-value.searchText').text
        except noelm:
            item['traffic_sources_search_percent'] = None

        try:
            search = chrome.find_elements_by_xpath('//div[@class="searchPie"]/div/span[@class="searchPie-number"]')
            percentages = [ s.text for s in search ]
            item['traffic_sources_search_organic_percent'] = percentages[0] if len(percentages) > 0 else None
            item['traffic_sources_search_paid_percent'] = percentages[1] if len(percentages) > 1 else None
        except noelm:
            item['traffic_sources_search_organic_percent'] = None
            item['traffic_sources_search_paid_percent'] = None

        try:
            lists = [ l.text.split('\n') for l in chrome.find_elements_by_css_selector('.searchKeywords-text') ]
            item['traffic_sources_search_organic_keywords'] = lists[0][1:-1]
            item['traffic_sources_search_organic_total'] = lists[0][-1].split()[1]
            item['traffic_sources_search_paid_keywords'] = lists[1].text.split('\n')[1:-1]
            item['traffic_sources_search_paid_total'] = lists[1][-1].split()[1]
        except noelm:
            item['traffic_sources_search_organic_keywords'] = None
            item['traffic_sources_search_organic_total'] = None
            item['traffic_sources_search_paid_keywords'] = None
            item['traffic_sources_search_paid_total'] = None

        yield item
