BOT_NAME = 'boxoffice_scrapy'

SPIDER_MODULES = ['boxoffice_scrapy.spiders']
NEWSPIDER_MODULE = 'boxoffice_scrapy.spiders'

ROBOTSTXT_OBEY = False

STATS_DUMP = False

#goes 100->200->300
ITEM_PIPELINES = {
    'boxoffice_scrapy.pipelines.mojo_spiderPipeline': 100,
    'boxoffice_scrapy.pipelines.heirloom_spiderPipelines': 200,
    'boxoffice_scrapy.pipelines.budget_spiderPipelines': 300
}

#impersonate user with user_agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

#identify as common browser, add in delays (slow down scraping)
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1

#create somewhat realistic browsing pattern
AUTOTHROTTLE_ENABLED = True
