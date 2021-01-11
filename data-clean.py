"""
Retrieve & clean data.
要拿data，有data之后，要打扫打扫🧹

Start with movies (pracitce-r)
用movies来练习一点点
"""

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
