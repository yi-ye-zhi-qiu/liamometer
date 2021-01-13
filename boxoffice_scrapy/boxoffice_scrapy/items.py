import scrapy

class scrapy_item(scrapy.Item):
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
