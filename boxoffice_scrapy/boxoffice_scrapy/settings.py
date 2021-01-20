BOT_NAME = 'boxoffice_scrapy'

SPIDER_MODULES = ['boxoffice_scrapy.spiders']
NEWSPIDER_MODULE = 'boxoffice_scrapy.spiders'

ROBOTSTXT_OBEY = False

STATS_DUMP = False

#goes 100->200->300
# ITEM_PIPELINES = {
#     'boxoffice_scrapy.pipelines.mojo_spiderPipeline': 100,
#     'boxoffice_scrapy.pipelines.heirloom_spiderPipelines': 200,
#     'boxoffice_scrapy.pipelines.budget_spiderPipelines': 300,
#     'boxoffice_scrapy.pipelines.metacritic_spiderPipelines': 400
# }
HTTPERROR_ALLOWED_CODES  =[404]

#impersonate user with user_agent

#identify as common browser, add in delays (slow down scraping)
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 5

#create somewhat realistic browsing pattern
AUTOTHROTTLE_ENABLED = True

from boxoffice_scrapy.utils import get_random_agent

USER_AGENT = get_random_agent()
