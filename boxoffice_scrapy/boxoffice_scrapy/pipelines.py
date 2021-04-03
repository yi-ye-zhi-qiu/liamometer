"""
Scrapy pipelines are used to process scrapy items.
Where scrapy items are dictionary-like objects, pipelines are for processing them.

In this file, we process

IMDb data --> imdb_spiderPipelines
Metacritic data --> metacritic_spiderPipelines
RottenTomatoes data --> (1) heirloom_spiderPipelines (2) tomato_spiderPipelines
**NOTE**: we will create a tomatoes_final in a cleaned data which merges these two...
BoxOfficeMojo data --> mojo_spiderPipeline

Each pipeline is automatically called by the spider.
"""

import csv
from .items import bcolors

class imdb_spiderPipelines(object):
    """
    Takes in mojo item, and adds it row-by-row to a csv, dumps out imdb.csv
    """

    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/imdb.csv")
        self.csvwriter = csv.writer(open("imdb.csv", "w", newline=''))
        self.csvwriter.writerow(["mojo_title", "imdbpicture", "imdbscore", "imdbcount", "metafromimdb"])

    def process_item(self, item, spider):
        row = []
        row.append(item["mojo_title"])
        row.append(item["imdbpicture"])
        row.append(item["imdbscore"])
        row.append(item["imdbcount"])
        row.append(item["metafromimdb"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==> " + bcolors.ENDC + row[0])
        return item

    def close_spider(self, spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + " Dumped data into boxoffice_scrapy/imdb.csv")

class metacritic_spiderPipelines(object):
    """
    Takes in metacritic item, and adds it row-by-row to a csv, dumps out metacritic.csv
    """
    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/metacritic.csv")
        self.csvwriter = csv.writer(open("metacritic.csv", "w", newline=''))
        self.csvwriter.writerow(["mojo_title", "criticscore", "criticcount", "audiencescore", "audiencecount"])

    def process_item(self, item, spider):
        row = []
        row.append(item["mojo_title"])
        row.append(item["criticscore"])
        row.append(item["criticcount"])
        row.append(item["audiencescore"])
        row.append(item["audiencecount"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==> " + bcolors.ENDC + row[0])
        return item

    def close_spider(self,spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + " Dumped data into boxofficescrapy/metacritic.csv")

class heirloom_spiderPipelines(object):
    """
    Takes in rottentomatoes search item, and adds it row-by-row to a csv, dumps out heirloom.csv
    """
    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/heirloom.csv")
        self.csvwriter = csv.writer(open("heirloom.csv", "w", newline=''))
        self.csvwriter.writerow(["mojo_title", "url","title", "criticscore", "criticcount", "audiencescore"])

    def process_item(self, item, spider):
        row = []
        row.append(item["mojo_title"])
        row.append(item["url"])
        row.append(item["title"])
        row.append(item["criticscore"])
        row.append(item["criticcount"])
        row.append(item["audiencescore"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==>" + bcolors.ENDC + row[1])
        return item

    def close_spider(self, spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + " Dumped data into boxoffice_scrapy/heirloom.csv")

class tomato_spiderPipelines(object):
    """
    Takes in rottentomatoes item, and adds it row-by-row to a csv, dumps out rotten_tomatoes.csv
    """
    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/heirloom.csv")
        self.csvwriter = csv.writer(open("rotten_tomatoes.csv", "w", newline=''))
        self.csvwriter.writerow(["url", "mojo_title", "criticcount", "audiencecount", "tomato_image"])

    def process_item(self, item, spider):
        row = []
        row.append(item["mojo_title"])
        row.append(item["url"])
        row.append(item["tomato_criticcount"])
        row.append(item["tomato_audiencecount"])
        row.append(item["tomato_image"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==>" + bcolors.ENDC + row[1])

    def close_spider(self, spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + " Dumped data into boxoffice_scrapy/heirloom.csv")

class mojo_spiderPipeline(object):
    """
    Takes in boxoffice item, and adds it row-by-row to a csv, dumps out mojo.csv
    """

    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/mojo.csv")
        self.csvwriter = csv.writer(open("mojo.csv", "w", newline=''))
        self.csvwriter.writerow(["title", "domestic_revenue", "world_revenue", "distributor", "opening_revenue", "opening_theaters", "budget", "MPAA", "genres", "release_days"])
        #this one takes 1-2 seconds to start-up, so I include this..
        print(bcolors.OKGREEN + bcolors.BOLD + "One second..." + bcolors.ENDC)

    def process_item(self, item, spider):
        row = []
        row.append(item["title"])
        row.append(item["domestic_revenue"])
        row.append(item["world_revenue"])
        row.append(item["distributor"])
        row.append(item["opening_revenue"])
        row.append(item["opening_theaters"])
        row.append(item["budget"])
        row.append(item["MPAA"])
        row.append(item["genres"])
        row.append(item["release_days"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==>" + bcolors.ENDC + row[0])
        return item

    def close_spider(self, spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + "Dumped data into boxoffice_scrapy/mojo.csv")
