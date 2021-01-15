#run: nohup scrapy crawl mojo_spider -o mojo.csv --logfile mojo.log & scrapy crawl tomato_spider -o tomato.csv --logfile tomato.log
import scrapy
from ..items import BoxItem

class mojo_spider(scrapy.Spider):
    name = "mojo_spider"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
      "https://www.boxofficemojo.com/year/2017/",
      "https://www.boxofficemojo.com/year/2018/",
      "https://www.boxofficemojo.com/year/2019/",
      "https://www.boxofficemojo.com/year/2020/"
    ]
    #note: 2017, 2018, 2019 have ~800  rows
    #note: 2020 is limiting @ 454
    for year in [2017, 2018, 2019, 2020]:
        start_urls.append("https://www.boxofficemojo.com/year/"+str(year)+"/")
    def parse(self, response):
        #for TESTING
        #for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:2]:
        #for PRODUCTION
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:len(response.xpath('//*[@id="table"]/div/table/tr'))]:
            href = tr.xpath('./td[2]/a/@href')
            url = response.urljoin(href[0].extract())
            try:
                yield scrapy.Request(url, callback=self.parse_page_contents)
            except IndexError as ie:
                print("Ignoring error in '{}': '{}'.".format(url, ie))
    def parse_page_contents(self, response):
        item = BoxItem()

        elements = []
        for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]:
            elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))

            if 'MPAA' in elements:
                m = elements.index('MPAA') + 1
                loc_MPAA = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(m)
                item['MPAA'] = response.xpath(loc_MPAA)[0].extract()
            else:
                item['MPAA'] = 'N/A'
            if 'Budget' in elements:
                y = elements.index('Budget') + 1
                loc_budget = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/span/text()').format(y)
                item["budget"] = response.xpath(loc_budget)[0].extract()
            else:
                item['budget'] = 'N/A'
            if 'Release Date' in elements:
                z = elements.index('Release Date') + 1
                loc_releasedate = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/a/text()').format(z)
                item["release_days"] = response.xpath(loc_releasedate)[0].extract()
            else:
                item['release_days'] = 'N/A'
            if 'Genres' in elements:
                w = elements.index('Genres') + 1
                loc_genres = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()').format(w)
                item['genres'] = ', '.join(response.xpath(loc_genres)[0].extract().split())
            else:
                item['genres'] = 'N/A'
            if 'Opening' in elements:
                v = elements.index('Opening') + 1
                loc_openingrevenue = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/span/text()').format(v)
                item["opening_revenue"] = response.xpath(loc_openingrevenue)[0].extract()
            else:
                item['opening_revenue'] = 'N/A'
            if 'Widest Release' in elements:
                b = elements.index('Widest Release') + 1
                loc_openingtheaters = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()').format(b)
                item["opening_theaters"] = ' '.join(response.xpath(loc_openingtheaters)[0].extract().split())
            else:
                item['opening_theaters'] = 'N/A'
            if 'Distributor' in elements:
                c = elements.index('Distributor') + 1
                loc_distributor = ('//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()').format(c)
                item["distributor"] = response.xpath(loc_distributor)[0].extract()
            else:
                item['distributor'] = 'N/A'

        item['title'] = response.xpath('//*[@id="a-page"]/main/div/div[1]/div[1]/div/div/div[2]/h1/text()')[0].extract()
        item['domestic_revenue'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()
        item['world_revenue'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[3]/span[2]/a/span/text()')[0].extract()
        yield item

import scrapy
from scrapy import Spider, Selector
import random
import requests
import re
import math
import time
import colors
from termcolor import colored


class tomato_spider(scrapy.Spider):
    name = 'tomato_spider'
    allowed_domains = ['https://www.rottentomatoes.com']
    start_urls = ["https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_art_house__international_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_kids__family_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_musical__performing_arts_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_special_interest_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_sports__fitness_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_television_movies/",
                  "https://www.rottentomatoes.com/top/bestofrt/top_100_western_movies/"]

    soft_failures = 0
    hard_failures = 0

    def parse(self, response):
        top100 = response.xpath('/html/body/div[4]/div[2]/div[1]/section/div/table//@href').extract()

        for selector in top100:
            url = 'https://www.rottentomatoes.com' + selector
            try:
                yield self.get_movieinfo(url)
            except IndexError as ie:
                print("Ignoring error in '{}': '{}'.".format(url, ie))

    @staticmethod
    def _get_content(link):
        """
        Politely request the page content at link.
        """

        content = requests.get(link).text

        x = 3 + 2 * random.random()
        time.sleep(x)

        return content

    def get_movieinfo(self, url):
        print("Getting movie info for '{}'".format(url))

        content = tomato_spider._get_content(url)

        def make_xpath(sibling_value):
            return '//div[@class="meta-label subtle" and text()="{}: "]/following-sibling::div/text()'.format(sibling_value)

        def grab_data(name, my_xpath, force=False):
            def print_failures(is_hard):
                print("\n{} fail to xpath '{}'!! '{}'. \nsoft fails: {}, hard_fails: {}\n".format(
                    "\tHARD" if is_hard else "Soft", name, my_xpath, self.soft_failures, self.hard_failures))

            try:
                return Selector(text=content).xpath(my_xpath)[0].extract().strip()
            except Exception as e:
                if force:
                    self.soft_failures += 1
                    print_failures(False)
                    return None

                self.hard_failures += 1
                print_failures(True)
                raise e

        return {
            "title": grab_data("title", '//h1[@class="mop-ratings-wrap__title mop-ratings-wrap__title--top"]/text()'),
            "criticscore": grab_data("criticscore", '//*[@id="tomato_meter_link"]/span[2]/text()'),
            "criticcount": grab_data("critic count", '//small[@class="mop-ratings-wrap__text--small"]/text()'),
            "audiencescore": grab_data("audiencescore", '//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]/text()')
        }

# # ------------ TESTING OUR SCRAPY: ------------
#
# #urls follow pattern of https://www.boxofficemojo.com/release/rl2708702721/?ref_=bo_yld_table_1
# #use scrapy shell to debug w/out having to run the entire spider
# #EXAMPLE:
# scrapy shell "https://www.boxofficemojo.com/year/2017/"
# #find xpath of each href
# response.xpath('//*[@id="table"]/div/table/tr[2]/td[2]/a/@href')[0].extract()
# #returns: '/release/rl1182631425/?ref_=bo_yld_table_1'
# response.urljoin('/release/rl1182631425/?ref_=bo_yld_table_1')
# #returns: 'https://www.boxofficemojo.com/release/rl2708702721/? ref_=bo_yld_table_1'
#scrapy shell 'https://www.boxofficemojo.com/release/rl2708702721/? ref_=bo_yld_table_1'
#response.xpath('') this is how you test if your xpath works without having to run the spider each time
