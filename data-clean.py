"""
Retrieve & clean data.
要拿data，有data之后，要打扫打扫🧹

Start with movies (pracitce-r)
用movies来练习一点点
asd
"""


## WANT: title, genre, release date, gross_$
## SLOW: BeautifulSoup

from bs64 import BeautifulSoup as soup
import requests as req
import re
import pandas as pd
import numpy as np

def webscrape_slower():

    def get_raw_data():

        #parent = top movies for 2020
        url = "https://www.boxofficemojo.com/year/2020/?sortDir=asc&sort=rank&grossesOption=totalGrosses"
        res = req.get(url)
        parent_content = soup(res.content, 'html.parser')

        #parent_content = SoupStrainer('td') #optimize speed slightly? ?

        parent_link = parent_content.find_all('td', class_='a-text-right mojo-header-column mojo-truncate mojo-field-type-rank mojo-sort-column')

        #lazy way of grabbing titles and links
        raw_parent = parent_content.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
        parent_name, parent_link = [], []
        for name in raw_parent:
            panret_name.append(name.find('a').getText())
            parent_link.append(name.find('a')['href'])

        #lazy way of getting how much money a movie made

        raw_gross = parent_content.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
        gross = []
        for movie in raw_gross:
            gross.append(movie)

        genres, release_dates = [], []

        #iterate through parent_links and grab genre, release date
        for i in parent_link:
            #这个语句： 检测 能 链接网站
            #可以：
            try:
                #child （孩子） 就是每一个电影
                child_url = '' + i
                child_req = req.get(child_url)
                child_content = soup(child_req.content, 'html.parser')

                elm, genres, release_date = [], [], []
                #每一个电影的 genre, supply tuple list of things we want to find
                for elm in child_content.find_all('span', text=lambda value: value and value.startswith("Genre", "Release Date")):

                    #掉不要的换行
                    elms = re.sub("\s{1,}", " ", elm.nextSibling.text.replace('\n', ''))

                genres = [this_elm for this_elm in elms if elms.index(this_elm) %2==0]
                release_date = [this_elm for this_elm in elms if elms.index(this_elm) %2 != 0]

                time.sleep(1)
            #不可以 你就停下来了
            except Exception as req.exceptions.ConnectionError:
                r.status_code = 'Connection refused by boxoficemojo, likely due to too many attempts to connect. Try importing time and using time.sleep between requests to url.'


        #import timeit
        #%timeit for i in l: get_central() #doesn't work

        #have to avoid arrays of differing lengths,
        movies = {'title': titles, 'gross': gross, 'genre': genres, 'release date': release_date}
        #take movies and construct df from dict of array-like titles, genres
        #psas index as orientation
        df = pd.DataFrame.from_dict(movies, orient='index')
        df = df.transpose()
        return df

#log runtime?



#run first: pip install scrapy
#import library
import scrapy

                    #spider inherits from base
class RedditSpider(scrapy.Spider): #class to put logic for data extraction
    name = 'reddit'
    start_urls = ["https://www.reddit.com/r/cats"] #only scrape first page
    #specified the website
    #define logic of data extraction

    #how to tell reddit spider that it's found img?

    #correspond to spider object and its response respectively
    def parse(self, response):
        #imgs located in img tag
        #search through img tag and specify extension type of jpg, gif etc.

        #get href by using xpath selector
        links = response.xpath("//img/@src")

        #to build new html page, build it incrementally as we counter img
        #build html as a string, use string comprehension to append html to string

        #instantiate html
        html =""

        #iterate through links

        for link in links:
            #get url as a string
            url = link.get()
            #compare if contains img by comparing extension type

            #use condition any statement

            if any(extension in url for extension in [".jpg", ".gif", ".png"]):
                html += """<a href="{url}"
                target = "_blank">
                <img src="{url}" height = "33%" width="33%"/>
                <a/>""".format(url=url)
                #use string formatting to build dynamically
                #open existing file or create new one to save output

                #with statement to perform write operation on file
                with open("frontpage.html", "a") as page:
                    #append new data to frontpage.html and manipulate as variable page
                    page.write(html) #writes string built from within loop
                    #close file to commit changes
                    page.close()
