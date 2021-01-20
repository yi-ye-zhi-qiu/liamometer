import scrapy

#items ~= dictionaries in scrapy, the below dictionaries are used for data

#for BoxOfficeMojo:
class BoxItem(scrapy.Item):
    title = scrapy.Field()
    domestic_revenue = scrapy.Field()
    world_revenue = scrapy.Field()
    distributor = scrapy.Field()
    opening_revenue = scrapy.Field()
    opening_theaters = scrapy.Field()
    budget = scrapy.Field()
    MPAA = scrapy.Field()
    genres = scrapy.Field()
    release_days = scrapy.Field()

#for RottenTomatoes:
class TomatoItem(scrapy.Item):
    mojo_title = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    criticscore = scrapy.Field()
    criticcount = scrapy.Field()
    audiencescore = scrapy.Field()

#for the-numbers.com, a site used to fetch budget
class BudgetItem(scrapy.Item):
    mojo_title = scrapy.Field()
    budget_site_title = scrapy.Field()
    budget = scrapy.Field()
    url = scrapy.Field()

class HeirloomItem(scrapy.Item):
    mojo_title = scrapy.Field()
    url = scrapy.Field()
    tomato_criticcount = scrapy.Field()
    tomato_audiencecount = scrapy.Field()
    tomato_image = scrapy.Field()

class MetacriticItem(scrapy.Item):
    mojo_title = scrapy.Field()
    criticscore = scrapy.Field()
    criticcount = scrapy.Field()
    audiencescore = scrapy.Field()
    audiencecouny = scrapy.Field()

class IMDBItem(scrapy.Item):
    mojo_title = scrapy.Field()
    imdbpicture = scrapy.Field()
    imdbscore = scrapy.Field()
    imdbcount = scrapy.Field()
    metafromimdb = scrapy.Field()

#for coloring terminal text:
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
