#run: nohup scrapy crawl mojo_spider -o mojo_macm1.csv --logfile mojomac1.log & scrapy crawl heirloom_spider -o heirloom_macm1.csv --logfile heirloom_macm1.log
#for each spider run: scrapy crawl mojo_spider -L WARN  for clean output
#or: scrapy crawl heirloom_spider -L WARN               for clean output
import scrapy
from ..items import BoxItem
import csv
from scrapy_splash import SplashRequest
import re
import json
from pprint import pprint

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

class mojo_spider(scrapy.Spider):
    #FULLY FUNCTIONAL, runtime 1.5 hr
    name = "mojo_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.mojo_spiderPipeline': 300},
    }
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
      "https://www.boxofficemojo.com/year/2017/",
      "https://www.boxofficemojo.com/year/2018/",
      "https://www.boxofficemojo.com/year/2019/",
      "https://www.boxofficemojo.com/year/2020/"
    ]
    #note: 2017, 2018, 2019 have ~800  rows
    #note: 2020 is only @ 454 as of 16-Jan-2021
    for year in [2017, 2018, 2019, 2020]:
        start_urls.append("https://www.boxofficemojo.com/year/"+str(year)+"/")
    def parse(self, response):
        #for TESTING
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:2]:
        #for PRODUCTION
        # for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:len(response.xpath('//*[@id="table"]/div/table/tr'))]:
            href = tr.xpath('./td[2]/a/@href')
            url = response.urljoin(href[0].extract())
            try:
                yield scrapy.Request(url, callback=self.parse_page_contents)
            except IndexError as ie:
                print(bcolors.WARNING + "Ignoring error in '{}': '{}'.".format(url, ie) + bcolors.ENDC)
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

class heirloom_spider(scrapy.Spider):
    name = "heirloom_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.heirloom_spiderPipelines': 300}
    }
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ['https://www.rottentomatoes.com/']

    def start_requests(self):
        #define search request from mojo.csv title entries
        #this runs almost instantly
        with open('/Users/liamisaacs/Desktop/github repositories/metis-project2/boxoffice_scrapy/mojo.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            mojo_titles = []
            for row in csv_reader:
                #rotten tomatoes replaces : with 3A
                row[0] = row[0].replace(':', '%3A')
                #search strings are just each word followed by %20
                mojo_titles.append('%20'.join(row[0].split(' ')))

        #for TESTING
        mojo_titles = mojo_titles[1:2]

        for i in mojo_titles:
            #for each movie build url
            url = 'https://www.rottentomatoes.com/search?search=' + i
            print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        raw_json = response.xpath('//script[@id="movies-json"]/text()').get()
        json_data = json.loads(raw_json)

        #for learning, please uncomment the below two lines
        #this shows you what the raw json is, what we parse
        # print(bcolors.OKGREEN + bcolors.BOLD + "Raw json ==>" +bcolors.ENDC)
        # pprint(json_data)

        base_json = json_data["items"][0]

        return {
            'url': 'placeholder',
            'title': base_json["name"],
            'criticscore': base_json["tomatometerScore"]["score"],
            'criticcount': 'placeholder',
            'audiencescore': base_json["audienceScore"]["score"]
        }
