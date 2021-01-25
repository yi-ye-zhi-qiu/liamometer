import scrapy

#items ~= dictionaries in scrapy, the below dictionaries are used for data
#note: these are all *strings*

class SequelItem(scrapy.Item):
    mojo_title = scrapy.Field()
    has_sequel = scrapy.Field()

#for BoxOfficeMojo:
class BoxItem(scrapy.Item):
    #movie title
    title = scrapy.Field()
    domestic_revenue = scrapy.Field()
    international_revenue = scrapy.Field()
    world_revenue = scrapy.Field()
    #distributor = Disney or something like that
    distributor = scrapy.Field()
    opening_revenue = scrapy.Field()
    #number of theaters movie premiered in
    opening_theaters = scrapy.Field()
    budget = scrapy.Field()
    MPAA = scrapy.Field()
    genres = scrapy.Field()
    release_days = scrapy.Field()

    #would advise looking at something like this in the future:
    #re_release = scrapy.Field()

#for RottenTomatoes:
class TomatoItem(scrapy.Item):
    mojo_title = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    criticscore = scrapy.Field()
    criticcount = scrapy.Field()
    audiencescore = scrapy.Field()

#for RottenTomatoes:
class HeirloomItem(scrapy.Item):
    mojo_title = scrapy.Field()
    url = scrapy.Field()
    tomato_criticcount = scrapy.Field()
    tomato_audiencecount = scrapy.Field()
    tomato_image = scrapy.Field()

#SIDENOTE: why heirloom AND tomato? We split it up into two steps: (1) search rotten tomatoes by movie name
#from box office mojo and fetch the url for that movie on RottenTomatoes and (2) read data from that url.

#for Metacritic:
class MetacriticItem(scrapy.Item):
    mojo_title = scrapy.Field()
    criticscore = scrapy.Field()
    criticcount = scrapy.Field()
    audiencescore = scrapy.Field()
    audiencecouny = scrapy.Field()

#for IMDb:
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
