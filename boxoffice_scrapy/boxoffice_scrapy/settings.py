BOT_NAME = 'boxoffice_scrapy'

SPIDER_MODULES = ['boxoffice_scrapy.spiders']
NEWSPIDER_MODULE = 'boxoffice_scrapy.spiders'

#ignore robots.txt
ROBOTSTXT_OBEY = False

STATS_DUMP = False

#note: if you remove the below three settings you can pull data at like 50 rows/second, but you will
#ABSOLUTELY get banned

#impersonate user with user_agent
#identify as common browser, add in delays (slow down scraping)
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 1

#create somewhat realistic browsing pattern
AUTOTHROTTLE_ENABLED = True
