import csv
from .items import bcolors

class budget_spiderPipelines(object):

    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/budget.csv")
        self.csvwriter = csv.writer(open("budget.csv", "w", newline=''))
        self.csvwriter.writerow(["mojo_title", "title", "budget", "url"])

    def process_item(self, item, spider):
        row = []
        row.append(item["mojo_title"])
        row.append(item["title"])
        row.append(item["budget"])
        row.append(item["url"])
        self.csvwriter.writerow(row)
        print(bcolors.OKGREEN + bcolors.BOLD + "Added to csv ==>" + bcolors.ENDC + row[0])
        return item

    def close_spider(self, spider):
        print(bcolors.OKGREEN + bcolors.BOLD + "Done ==>" + bcolors.ENDC + " Dumped data into boxoffice_scrapy/budget.csv")

class imdb_spiderPipelines(object):

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

    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/heirloom.csv")
        self.csvwriter = csv.writer(open("heirloom.csv", "w", newline=''))
        self.csvwriter.writerow(["url", "title", "criticscore", "criticcount", "audiencescore"])

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

class mojo_spiderPipeline(object):
    #FULLY FUNCTIONAL
    def __init__(self):
        print(bcolors.OKGREEN + bcolors.BOLD + "Writing ==>" + bcolors.ENDC + "boxoffice_scrapy/mojo.csv")
        self.csvwriter = csv.writer(open("mojo_macm1.csv", "w", newline=''))
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
