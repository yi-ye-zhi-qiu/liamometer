#run: nohup scrapy crawl mojo_spider -o mojo_macm1.csv --logfile mojomac1.log & scrapy crawl heirloom_spider -o heirloom_macm1.csv --logfile heirloom_macm1.log
#for each spider run: scrapy crawl mojo_spider -L WARN                   for clean output
#                     scrapy crawl heirloom_spider -L WARN               for clean output
#                     scrapy crawl budget_spider -L WARN                 for clean output
#libraries listed in order they are used
import scrapy
from ..items import BoxItem, bcolors
import csv
#import json
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#from pprint import pprint
import re

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
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:10]:
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
    #MVP functional (missing count of how MANY critic/audience scores) 50/min.
    #runtime 1.5 hr.
    #takes in 3108, spits out 2773
    name = "heirloom_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.heirloom_spiderPipelines': 300}
    }
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ['https://www.rottentomatoes.com/']

    def start_requests(self):
        #define search request from mojo.csv title entries
        #this runs almost instantly
        with open('/Users/liamisaacs/Desktop/github repositories/metis-project2/boxoffice_scrapy/mojo_macm1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            mojo_titles, row_title = [], []
            for row in csv_reader:
                #rotten tomatoes replaces : with 3A
                row_title.append(row[0])

                row[0] = row[0].replace(':', '%3A')
                #search strings are just each word followed by %20
                mojo_titles.append('%20'.join(row[0].split(' ')))

        #NOTE: for TESTING only use 1-10 rows
        mojo_titles = mojo_titles[1:10]

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
        #we avoid time.sleep because it blocks Twisted reactor & eliminates Scrapy's concurrency advantage

class tomato_spider(scrapy.Spider):
    name = "tomato_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.tomato_spiderPipelines': 300},
    }
    allowed_domains = ["rottentomatoes.com"]

    def start_requests(self):
        #define search request from mojo.csv title entries
        #this runs almost instantly

        #CHANGE THIS TO YOUR OWN FILEPATH FOR rotten_tomatoes.csv
        with open('/mnt/c/Users/xtras/liam_code/boxoffice_scrapy/rotten_tomatoes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            tomato_url, mojo_title = [], []
            for row in csv_reader:
                #rotten tomatoes replaces : with 3A
                mojo_title.append(row[0])

                tomato_url.append(row[1])


        #THIS IS A LIST OF URLS WE WILL SCRAPE FROM, DELETE IF WORKING
        tomato_url = tomato_url[1:]
        #print(tomato_url)

        counter = 1
        for i in tomato_url:
            url = i
            print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + url)

            #WE REQUEST ROTTENTOMATOES TO GIVE US THE WEBSITE
            yield scrapy.Request(url=url, meta={'mojo_title': mojo_title[counter], 'link': url}, callback=self.parse)
            counter+=1

    def parse(self, response):
        mojo_title = response.meta['mojo_title']
        link = response.meta['link']
        #We need two things: the # of critic reviews (total count underneath tomatometer) THIS IS CALLED tomato_criticcount
        #and the # of audience reviews (total count underneath audience score) THIS IS CALLED tomato_audiencecount

        #I already have the review values themselves

        try:
            tomato_criticcount = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small/text()')[0].extract()
            tomato_criticcount = ''.join(re.findall(r'\d+', tomato_criticcount))
        except:
            tomato_criticcount = '"N/A"'
        try:
            tomato_audiencecount = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong')[0].extract()
            tomato_audiencecount = ''.join(re.findall(r'\d+', tomato_audiencecount))
        except:
            tomato_audiencecount = "N/A"
        try:
            tomato_image = response.xpath('//*[@id="topSection"]/div[1]/div/img["srcset"]')[0].extract()
            #response.xpath('//*[@id="topSection"]/img["srcset"]')[0].extract()
            #tomato_image = re.match('([^\s]+)', tomato_image)
        except:
            tomato_image = "N/A"
        return{
            'mojo_title': mojo_title,
            'url': link,
            'tomato_criticcount': tomato_criticcount,
            'tomato_audiencecount': tomato_audiencecount,
            'tomato_image': tomato_image
        }



    #need to search each url on rotten tomatoes


class budget_spider(scrapy.Spider):
    #FULLY FUNCTIONAL
    #SLOWER because the-numbers.com (we use to fetch budgets) has stricter restrictions on scraping
    #we are forced to not only impersonate a user, but add-in download delays and autothrottle

    #runtime: ___
    name = "budget_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.budget_spiderPipelines': 300}
    }
    allowed_domains = ["www.the-numbers.com"]
    start_urls = ['https://www.the-numbers.com/']

    def start_requests(self):
        #define search request from mojo.csv title entries
        #this runs almost instantly
        with open('/Users/liamisaacs/Desktop/github repositories/metis-project2/boxoffice_scrapy/mojo_macm1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            mojo_titles, row_title = [], []
            for row in csv_reader:
                #store row_title just to print out success message in terminal
                row_title.append(row[0])

                #the-numbers works better on searches without characters like ":" or "-"
                row[0] = row[0].replace('-', ' ')
                row[0] = row[0].replace('Episode', 'Ep')
                row[0] = row[0].replace(':', ' ')

                #example search string: https://www.the-numbers.com/custom-search?searchterm=star+wars+ep+VII+last+jedi

                #search strings are just word+word+word
                mojo_titles.append('+'.join(row[0].split()))

        #NOTE: for TESTING only use 1-10 rows
        mojo_titles = mojo_titles[1:10]

        for i in mojo_titles:
            #for each movie build url
            url = 'https://www.the-numbers.com/custom-search?searchterm=' + i
            print(bcolors.OKGREEN + bcolors.BOLD + "Requesting (1 of 2 steps) ==> " + bcolors.ENDC + url)
            #NOTE: the-numbers will block you, so just pass in user-agent in settings.py
            #NOTE: we pass row_title in meta tag, such that we can reference it in the next class
            yield scrapy.Request(url=url, meta={'mojo_title': row_title[mojo_titles.index(i)+1]}, callback=self.parse)

    def parse(self, response):
        row_title = response.meta['mojo_title']
        try:
            link = 'https://www.the-numbers.com/' + response.xpath('//*[@id="page_filling_chart"]//tr//td//a/@href')[1].extract()
            print(bcolors.OKGREEN + bcolors.BOLD + "Requesting (2 of 2 steps) ==> " + bcolors.ENDC + link)
        #some movies on BoxOfficeMojo do not exist on the-numbers.com
        #so we have to yield results in a try-except condition, where non-existent results are replaced w/ N/A
            go_to_movie_link = scrapy.Request(url=link, callback=self.parse_each_movie, meta={'mojo_title': row_title, 'link': link})
            return go_to_movie_link
        except IndexError:
            print(bcolors.WARNING + bcolors.BOLD + "Request (2 of 2 steps) ==> " + bcolors.ENDC + "failed (non-fatal), movie" + bcolors.UNDERLINE + row_title + bcolors.ENDC + "DNE in the-numbers.com database")
            return{
                'mojo_title': row_title,
                'title': 'N/A',
                'url': 'N/A',
                'budget': 'N/A'
            }

    def parse_each_movie(self, response):
        row_title = response.meta['mojo_title']
        #title is invariably accurate, it will consistently be in the same spot
        title = response.xpath('//*[@id="main"]/div/h1/text()')[0].extract()
        link = response.meta['link']

        #for not wellknown movies, such as the remake of 1955 Senso (https://www.the-numbers.com/custom-search?searchterm=Senso)
        #there is no production budget, for this situation we just enter "N/A"
        #NOTE: this is assuming table is consistently ordered for movies that have budgets...

        #budget has to be "smart-searched", its position on the page is highly inconsistent
        elements = []
        #grab all elements present on page in table
        for i in range(0, len(response.xpath('//*[@id="summary"]//table//tr//td//b/text()'))-1):
            elements.append(''.join(response.xpath('//*[@id="summary"]//table//tr//td//b/text()')[i].extract().replace('\xa0', ' ')))
        #just examine production budget, wherever it appears on the page (messy)
        if 'Production Budget:' in elements:
            m = elements.index('Production Budget:')
            loc_budget = ('//*[@id="summary"]/table/tr[{}]/td[2]').format(m+1)
            budget = response.xpath(loc_budget)[0].extract()
            no_td_tags = re.compile('<.*?>')
            budget = re.sub(no_td_tags, '', budget)
            budget = budget.split('(')[0]
        else:
            budget = 'N/A'
        return {
            'mojo_title': row_title,
            'title': title,
            'url': link,
            'budget': budget
        }

class metacritic_spider(scrapy.Spider):
    #FULLY functional
    #runtime 2 hrs
    #3108 movies in, 1971 rows out
    name = "metacritic_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.metacritic_spiderPipelines': 300},
    }
    allowed_domains = ["metacritic.com"]

    def start_requests(self):

        with open('/Users/liamisaacs/Desktop/github repositories/metis-project2/boxoffice_scrapy/mojo_macm1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            mojo_titles, row_title = [], []
            for row in csv_reader:
                #rotten tomatoes replaces : with 3A
                row_title.append(row[0])

                row[0] = row[0].lower()
                row[0] = row[0].replace(':', '')
                #search strings are just each word followed by %20
                mojo_titles.append('-'.join(row[0].split(' ')))

        #NOTE: for TESTING only use 1-10 rows
        mojo_titles = mojo_titles[1:10]

        for i in mojo_titles:
            #for each movie build url
            try:
                url = 'https://www.metacritic.com/movie/' + i
                print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + url)
                #NOTE: we pass row_title in meta tag, such that we can reference it in the next class
                yield scrapy.Request(url=url, meta={'mojo_title': row_title[mojo_titles.index(i)+1]}, callback=self.parse)
            except:
                print(bcolors.WARNING + bcolors.BOLD + "Soft failure ==> " + bcolors.ENDC + "movie DNE or name mis-match for " + bcolors.UNDERLINE + row_title[i])

    def parse(self, response):
        mojo_title = response.meta['mojo_title']
        try:
            criticscore = response.xpath('//*[@id="main_content"]//table//tr//td//a/span/text()')[2].extract()
            # no_tags = re.compile('<.*?>')
            # critcscore = re.sub(no_tags, '', criticscore)
            if criticscore != 'No score yet':
                criticcount = response.xpath('//*[@id="main_content"]//table//tr//td//a/span/text()')[1].extract()
                criticcount = re.findall(r"\d+", criticcount)[0]
            else:
                criticcount = 'N/A'
            audiencescore = response.xpath('//*[@id="main_content"]//table//tr//td//table//tr//td//a/span/text()')[5].extract()
            if audiencescore != 'No score yet':
                audiencecount = response.xpath('//*[@id="main_content"]//table//tr//td//a/span/text()')[4].extract()
                audiencecount = re.findall(r"\d+", audiencecount)[0]
            else:
                audiencecount = response.xpath('//*[@id="main_content"]//table//tr//td//a/span/text()')[4].extract()
        except IndexError:
            print(bcolors.WARNING + bcolors.BOLD + "Soft failure ==> " + bcolors.ENDC + "movie DNE or name mis-match for " + bcolors.UNDERLINE + mojo_title)
            criticscore = 'Link error'
            criticcount = 'Link error'
            audiencescore = 'Link error'
            audiencecount = 'Link error'

        return{
            'mojo_title': mojo_title,
            'criticscore': criticscore,
            'criticcount': criticcount,
            'audiencescore': audiencescore,
            'audiencecount': audiencecount
        }

class imdb_spider(scrapy.Spider):
    name = "imdb_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.imdb_spiderPipelines': 300},
    }
    allowed_domains = ["imdb.com"]
    def start_requests(self):

        with open('/Users/liamisaacs/Desktop/github repositories/metis-project2/boxoffice_scrapy/mojo_macm1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            mojo_titles, row_title = [], []
            for row in csv_reader:
                row_title.append(row[0])
                row[0] = row[0].replace(':', '%3A')
                mojo_titles.append('+'.join(row[0].split(' ')))

        #NOTE: for TESTING only use 1-10 rows
        mojo_titles = mojo_titles[1:10]

        for i in mojo_titles:
            #for each movie build url
            try:
                url = 'https://www.imdb.com/search/title/?title=' + i
                print(bcolors.OKGREEN + bcolors.BOLD + "Requesting ==> " + bcolors.ENDC + url)
                #NOTE: we pass row_title in meta tag, such that we can reference it in the next class
                yield scrapy.Request(url=url, meta={'mojo_title': row_title[mojo_titles.index(i)+1]}, callback=self.parse)
            except:
                print(bcolors.WARNING + bcolors.BOLD + "Soft failure ==> " + bcolors.ENDC + "movie DNE or name mis-match for " + bcolors.UNDERLINE + row_title[i])

    def parse(self, response):
        row_title = response.meta['mojo_title']
        try:
            imdbpicture = response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[2]/a/img/@loadlate')[0].extract()
            imdbscore = response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/div/div[1]/strong/text()')[0].extract()
            imdbcount = response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/p[4]/span[2]/text()')[0].extract()
            metafromimdb = response.xpath('//*[@id="main"]/div/div[3]/div/div[1]/div[3]/div/div[3]/span/text()')[0].extract().strip()
        except IndexError:
            print(bcolors.WARNING + bcolors.BOLD + "Soft failure ==> " + bcolors.ENDC + "movie DNE or name mis-match for " + bcolors.UNDERLINE + row_title)
            imdbscore = 'Link error'
            imdbcount = 'Link error'
            metafromimdb = 'Link error'

        return{
            'mojo_title': row_title,
            'imdbpicture': imdbpicture,
            'imdbscore': imdbscore,
            'imdbcount': imdbcount,
            'metafromimdb': metafromimdb
        }
