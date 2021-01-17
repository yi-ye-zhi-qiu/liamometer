import csv

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

class heirloom_spiderPipelines(object):

    def __init__(self):
        print(bcolors.OKCYAN + "Adding column names to heirloom csv" + bcolors.ENDC)
        self.csvwriter = csv.writer(open("heirloom_macm1.csv", "w", newline=''))
        self.csvwriter.writerow(["title", "criticscore", "criticcount", "audiencescore"])

    def process_item(self, item, spider):
        row = []
        row.append(item["title"])
        row.append(item["criticscore"])
        row.append(item["criticcount"])
        row.append(item["audiencescore"])
        self.csvwriter.writerow(row)
        print(bcolors.OKCYAN + "Added " + row[0] + "to csv" + bcolors.ENDC)
        return item

    def close_spider(self, spider):
        print(bcolors.OKCYAN + " 🕷 Spider closed, 爬虫结束了！ 🕷" + bcolors.ENDC)

class mojo_spiderPipeline(object):
    #FULLY FUNCTIONAL
    def __init__(self):
        print(bcolors.OKCYAN + "Adding column names to mojo csv" + bcolors.ENDC)
        self.csvwriter = csv.writer(open("mojo_macm1.csv", "w", newline=''))
        self.csvwriter.writerow(["title", "domestic_revenue", "world_revenue", "distributor", "opening_revenue", "opening_theaters", "budget", "MPAA", "genres", "release_days"])

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
        print(bcolors.OKBLUE + "Added "+row[0]+ " to csv" + bcolors.ENDC)
        return item

    def close_spider(self, spider):
        print(bcolors.OKCYAN + " 🕷 Spider closed， 爬虫结束了！  🕷" + bcolors.ENDC)
