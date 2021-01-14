"""
Retrieve & clean data.
"""


## WANT: title, genre, release date, gross_$
## SLOW: BeautifulSoup

from bs4 import BeautifulSoup as soup
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


        print("Loading...")
        #lazy way of grabbing titles and links
        raw_parent = parent_content.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
        parent_name, parent_link = [], []
        for name in raw_parent:
            parent_name.append(name.find('a').getText())
            parent_link.append(name.find('a')['href'])

        parent_link = parent_link[:2]
        print(parent_link)

        #lazy way of getting how much money a movie made

        raw_gross = parent_content.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
        gross = []
        for movie in raw_gross:
            movie = raw_gross[raw_gross.index(movie)].get_text()
            gross.append(movie)

        genres, release_dates = [], []

        #iterate through parent_links and grab genre, release date
        for i in parent_link:
            try:
                child_url = 'https://www.boxofficemojo.com' + i
                child_req = req.get(child_url)
                child_content = soup(child_req.content, 'html.parser')
                print(child_content)

                elm, genres, release_date = [], [], []
                for elm in child_content.find_all('span', text=lambda value: value and value.startswith("Genre", "Release Date")):

                    elms = re.sub("\s{1,}", " ", elm.nextSibling.text.replace('\n', ''))

                genres = [this_elm for this_elm in elms if elms.index(this_elm) %2==0]
                release_date = [this_elm for this_elm in elms if elms.index(this_elm) %2 != 0]

                time.sleep(1)
            except Exception as req.exceptions.ConnectionError:
                req.status_code = 'Connection refused by boxoficemojo'

        print(genres)
        movies = {'title': parent_name, 'gross': gross, 'genre': genres, 'release date': release_date}

        #need to build dict from array-like objects
        df = pd.DataFrame.from_dict(movies, orient='index')
        print(df)
        return df

    get_raw_data()
#log runtime?

webscrape_slower()
#
# #run first: pip install scrapy
# #import library
# import scrapy
#
#                     #spider inherits from base
# class RedditSpider(scrapy.Spider): #class to put logic for data extraction
#     name = 'reddit'
#     start_urls = ["https://www.reddit.com/r/cats"] #only scrape first page
#     #specified the website
#     #define logic of data extraction
#
#     #how to tell reddit spider that it's found img?
#
#     #correspond to spider object and its response respectively
#     def parse(self, response):
#         #imgs located in img tag
#         #search through img tag and specify extension type of jpg, gif etc.
#
#         #get href by using xpath selector
#         links = response.xpath("//img/@src")
#
#         #to build new html page, build it incrementally as we counter img
#         #build html as a string, use string comprehension to append html to string
#
#         #instantiate html
#         html =""
#
#         #iterate through links
#
#         for link in links:
#             #get url as a string
#             url = link.get()
#             #compare if contains img by comparing extension type
#
#             #use condition any statement
#
#             if any(extension in url for extension in [".jpg", ".gif", ".png"]):
#                 html += """<a href="{url}"
#                 target = "_blank">
#                 <img src="{url}" height = "33%" width="33%"/>
#                 <a/>""".format(url=url)
#                 #use string formatting to build dynamically
#                 #open existing file or create new one to save output
#
#                 #with statement to perform write operation on file
#                 with open("frontpage.html", "a") as page:
#                     #append new data to frontpage.html and manipulate as variable page
#                     page.write(html) #writes string built from within loop
#                     #close file to commit changes
#                     page.close()
