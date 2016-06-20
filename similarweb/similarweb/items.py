# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SimilarwebItem(scrapy.Item):
    # define the fields for your item here like:
    similarweburl = scrapy.Field()
    domain = scrapy.Field()
    desc = scrapy.Field()
    ranks_global_rank = scrapy.Field()
    ranks_country_rank = scrapy.Field()
    ranks_category_rank = scrapy.Field()
    ranks_category_main_catg = scrapy.Field()
    ranks_category_sub_catg = scrapy.Field()
    engagement_date = scrapy.Field()
    engagement_total_visits = scrapy.Field()
    engagement_visits = scrapy.Field()
    engagement_avg_time_on_page = scrapy.Field()
    engagement_avg_page_views = scrapy.Field()
    engagement_bounce_rate = scrapy.Field()
    traffic_by_countries = scrapy.Field()
    traffic_sources_direct_percent = scrapy.Field()
    traffic_sources_referrals_percent = scrapy.Field()
    traffic_sources_referrals_top_referring_domains = scrapy.Field()
    traffic_sources_referrals_top_referring_total = scrapy.Field()
    traffic_sources_referrals_top_destination_domains = scrapy.Field()
    traffic_sources_referrals_top_destination_total = scrapy.Field()
    traffic_sources_search_percent = scrapy.Field()
    traffic_sources_search_organic_percent = scrapy.Field()
    traffic_sources_search_organic_keywords = scrapy.Field()
    traffic_sources_search_organic_total = scrapy.Field()
    traffic_sources_search_paid_percent = scrapy.Field()
    traffic_sources_search_paid_keywords = scrapy.Field()
    traffic_sources_search_paid_total = scrapy.Field()
    traffic_sources_social_percent = scrapy.Field()
    traffic_sources_social_domains = scrapy.Field()
    traffic_sources_mail_percent = scrapy.Field()
    traffic_sources_display_advertising_percent = scrapy.Field()
    traffic_sources_display_advertising_top_publishers_domains = scrapy.Field()
    traffic_sources_display_advertising_top_publishers_total = scrapy.Field()
    traffic_sources_display_advertising_top_ad_networks = scrapy.Field()
    audience_interests_main_category = scrapy.Field()
    audience_interests_sub_category = scrapy.Field()
    audience_interests_percent = scrapy.Field()
    also_visited_websites_domains = scrapy.Field()
    also_visited_websites_total = scrapy.Field()
    topics = scrapy.Field()
    similar_sites = scrapy.Field()
    related_mobile_apps_google_play = scrapy.Field()
    related_mobile_apps_app_store = scrapy.Field()
    pass
