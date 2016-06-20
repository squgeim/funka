# -*- coding: utf-8 -*-

# Scrapy settings for similarweb project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'similarweb'

SPIDER_MODULES = ['similarweb.spiders']
NEWSPIDER_MODULE = 'similarweb.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'similarweb (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

#Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Host': 'www.similarweb.com',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Cookie': 'loyal-user=%7B%22date%22%3A%222016-06-15T11%3A32%3A55.188Z%22%2C%22isLoyal%22%3Atrue%7D; i_72623ev9=75; UTGv2=h4b4a643ca913ace6f2c368a0f77e0f14c62; _ga=GA1.2.1381343462.1465990374; loyal-user=%7B%22date%22%3A%222016-06-15T11%3A32%3A55.188Z%22%2C%22isLoyal%22%3Afalse%7D; _vwo_uuid_v2=2ED031469E9B4EBA123FF40B67324C7E|59ba42ac4081a510600811892d89996a; _mkto_trk=id:891-VEY-973&token:_mch-similarweb.com-1465990395436-19672; _pk_id.1.fd33=83db009ee2b8a442.1465990400.1.1465992771.1465990400.; _pk_ses.1.fd33=*; user_num=nowset; intercom-visitor-semaphore-e74067abd037cecbecb0662854f02aee12139f95=1; intercom-id=81fa975e-653f-413a-85d1-a0d2a57dfd77; sbtsck=jav; SPSI=368af2b002c3462e99ffb7453d85e28c; PRLST=af; PRUM_EPISODES=s=1465993099472&r=https%3A//www.similarweb.com/website/monster.com; adOtr=faB2A080b; sc_is_visitor_unique=rx8617147.1465992771.8A70C52FF3644F61A709C6A8D5B2DEB6.1.1.1.1.1.1.1.1.1',
#     'Connection': 'keep-alive',
#     'Cache-Control': 'max-age=0',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'similarweb.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'similarweb.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'similarweb.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
