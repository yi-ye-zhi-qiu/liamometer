#run: nohup scrapy crawl mojo_spider -o mojo_macm1.csv --logfile mojomac1.log & scrapy crawl heirloom_spider -o heirloom_macm1.csv --logfile heirloom_macm1.log
#for each spider run: scrapy crawl mojo_spider -L WARN  for clean output
#or: scrapy crawl heirloom_spider -L WARN               for clean output
import scrapy
from ..items import BoxItem, bcolors
import csv
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint

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
                yield scrapy.Request(url, callback=self.parse_page_contents, meta={'mojo_url': url})
            except IndexError as ie:
                print(bcolors.WARNING + "Ignoring error in '{}': '{}'.".format(url, ie) + bcolors.ENDC)
    def parse_page_contents(self, response):
        item = BoxItem()
        url = response.meta['mojo_url']
        print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + str(url))

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
    #MVP functional (missing count of how MANY critic/audience scores)
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
            mojo_titles, row_title = [], []
            for row in csv_reader:
                #rotten tomatoes replaces : with 3A
                row_title.append(row[0])

                row[0] = row[0].replace(':', '%3A')
                #search strings are just each word followed by %20
                mojo_titles.append('%20'.join(row[0].split(' ')))

        #NOTE: for TESTING only use 1-10 rows
        mojo_titles = mojo_titles[1:50]

        for i in mojo_titles:
            #for each movie build url
            url = 'https://www.rottentomatoes.com/search?search=' + i
            print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + url)

            #NOTE: we pass row_title in meta tag, such that we can reference it in the next class
            yield scrapy.Request(url=url, meta={'mojo_title': row_title[mojo_titles.index(i)+1]}, callback=self.parse)

    def parse(self, response):

        raw_json = response.xpath('//script[@id="movies-json"]/text()').get()
        json_data = json.loads(raw_json)
        row_title = response.meta['mojo_title']

        #for learning, please uncomment the below two lines, they show you the raw JSON
        # print(bcolors.OKGREEN + bcolors.BOLD + "Raw json ==>" +bcolors.ENDC)
        # pprint(json_data)

        #using fuzzy wuzzy token_sort_ratio to measure which search result is correct
        #this will generaly be list index 0 since we trust rottentomatoes search
        #algorithm, but this is just a quick double-check
        new_ratio = 0
        for i in range(0,len(json_data['items'])):
            #ok to use N^2 complexity, as json['items'] tends to be only 2-10 items long
            this_ratio = fuzz.token_sort_ratio(row_title, json_data["items"][i]["name"])
            if new_ratio < this_ratio:
                new_ratio = this_ratio
                closest_row_title = i

        base_json = json_data["items"][0]

        #critic or audience scores are often missing for non-rated (less popular) movies
        try:
            criticscore = base_json["tomatometerScore"]["score"]
        except KeyError:
            criticscore = "N/A"
        try:
            audiencescore = base_json["audienceScore"]["score"]
        except KeyError:
            audiencescore = "N/A"

        return {
            'mojo_title': row_title,
            'url': base_json["url"],
            'title': base_json["name"],
            'criticscore': criticscore,
            'criticcount': 'placeholder',
            'audiencescore': audiencescore
        }
        time.sleep(1)
