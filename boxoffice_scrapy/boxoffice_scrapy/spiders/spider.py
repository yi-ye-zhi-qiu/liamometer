#run: nohup scrapy crawl mojo_spider -o mojo_macm1.csv --logfile mojomac1.log & scrapy crawl heirloom_spider -o heirloom_macm1.csv --logfile heirloom_macm1.log
#for each spider run: scrapy crawl mojo_spider -L WARN                   for clean output
#                     scrapy crawl heirloom_spider -L WARN               for clean output
#                     scrapy crawl budget_spider -L WARN                 for clean output
#libraries listed in order they are used
"""
NOTE: if you download this code, you must change the following lines of code to be *your* file paths, not mine:
line 157, 243, 326, 399.

Thanks!
"""


import scrapy
from ..items import BoxItem, bcolors
import csv
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint
import re

class mojo_spider(scrapy.Spider):
    #FULLY FUNCTIONAL, runtime 1.5 hr
    """
    Takes in: start_urls, which is set to 2017-2020.

    Notes:
    This will 'crawl' box office mojo urls for years of '17, '18 '19 and '20.
    Crawling will pull the following fields per movie:
    Title, MPAA, Budget, Release Date, Genres, Opening Revenue, World Revenue, Distributor, Reelase Date and Opening Theaters (how many theaters the movie premiered at)
    These fields are stored in a scrapy item, which is a dictionary-like object (so we are basically using a dictionary)
    If any of the above fields is missing, it will populate N/A. This is true for all except Title, Domestic Revenue, and World Revenue.
    Those three are mandatory categories.
    This is also sped up by using a generator function (hence yield instead of return).
    The scrapy item, or the dictionary data per item, is put into a csv file row by row (your terminal will echo this).
    This is specified in scrapy by the "pipeline" for that spider, here we have it set to mojo_spiderPipeline.

    Output:
    A csv called "mojo.csv", around 3.1k rows long.
    """
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
    #FULLY FUNCTIONAL
    #runtime 1.5 hr.
    #takes in 3108, spits out 2773
    """
    Assembly of RottenTomatoes data is split into two spiders, we crawl
    1. heirloom_spider
    2. tomato_spider

    Why do we have two?

    Heirloom spider takes in mojo_csv, and grabs RottenTomatoes urls for each movie. This is a dynamic search pattern. This is what will get you IP banned.
    By dynamically searching we preserve 90% of data, and don't have to drop a bunch of rows because we "guess" at what the url is based off a given site pattern.
    It's better to do dynamic searches like this always between websites, as the urls per movie will be different, the backend databases are never going to be the same.
    It's worth noting that approach usually involves disobeying robots.txt though, and can get you banned (temporarily).

    Takes in: mojo_csv file.
    Spits out: heirloom.csv, a bunch of rotten_tomatoes urls and critic/audience scores. These will be "N/A" if they're not found.

    We use fuzzywuzzy to double-check the search result and make sure it's the same as the movie we want.

    """
    name = "heirloom_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'boxoffice_scrapy.pipelines.heirloom_spiderPipelines': 300}
    }
    allowed_domains = ["www.rottentomatoes.com"]

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

        #So, on each search result RottenTomatoes makes an internal API request, which contains JSON data.
        #This would save us the second step if the JSON data is complete, but it only gives critic and audience score,
        #not the *number* of scores per each.

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
    """
    This is our step 2 for RottenTomatoes data, where we just query each url we found, and use xpath
    to get each data point we require. These are "N/A" if they do not exist.
    """


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

class metacritic_spider(scrapy.Spider):
    #FULLY functional
    #runtime 2 hrs
    #3108 movies in, 1971 rows out
    """
    Takes in: mojo_csv and searches metacritic reviews.

    Returns audience score and count, critic score and count (count = how many reviews there were).

    NOTE: for metacritic we just "guess" the url based off a pattern, we AVOID disobeying robots.txt, and AVOID searching.
    This is OK, it preserves about 70% of data.

    If there's an error in finding the url, we return "Link error". If we find the url but can't find the score for any of the fields, that field will show up as "N/A".

    """

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
    """
    Takes in: mojo_csv
    Spits out: IMDb data for each movie. We "guess" the URL again here, but this preserves 90% of data (exact: 89.5%), or returns 2.7k rows from a 3.1k input.
    The result is returned as "imdb.csv".
    Data is processed in the imdb_spiderPipelines.
    """


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
