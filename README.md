## The Liam-o-meter 🥭 ![Python version](https://img.shields.io/badge/python-%E2%89%A53.6-blue.svg?style=flat-square&logo=python&logoColor=white)

![Metis logo](metis.png) Metis data-science bootcamp project 2, **Jan. 11-22 2021**

** [See the final product](http://34.212.100.77/liamometer) **


**Abstract:**  FlaskApp of movies rated using a k- (5-) fold cross-validation lasso multiple linear regression model of IMDb scores (n=2316) scraped off the web, where we chose to use two features: genre (Action, Adventure, etc.) and movie distributor (Disney, Paramount, Other defined as <=7 movies/year) to analyze for a 2016-2020 timeframe. This model is interpretive and the use case is: "I can see how well a movie did on IMDb, how does that rating compare to if I were to *only* care about a categorical subset of variables, if I were to only consider that it's a Disney Animation, for instance?"

- Want graphs & written analysis, not just a flimsy jupyter notebook? 🤔️ Check "download more stats" - there's a report there. Alternatively, see Linear Regression of IMDb ratings (pdf).

----

Contributors:
- Liam
- Liam's Dad (helped run code after I got IP-banned from RottenTomatoes)

----

Requirements to run locally:

You can run the Scrapy spider (data collection) to grab similar data using:

- `Python 3.6` or greater
- Scrapy `(pip3 install scrapy)`
- numpy, json, regex, fuzzywuzzy
- ~10 hours of time
- Strong willingness to get IP-banned from RottenTomatoes (potentially)

To run an entire webapp, you need to configure an AWS server:

- The FlaskApp is running on Ubuntu on an AWS AmazonLightsail server.

*Note:* we do not focus here on deployment of a FlaskApp onto AWS, or even on the html/css used to display the data. This is because the FlaskApp is a part of my personal portfolio, and including all of the code for that here seems tangential to the point at hand: web scraping and linear regression. If you are interested, to view the code used to create the app see [here](https://github.com/yi-ye-zhi-qiu/personalwebsite).

----

Project Map   

This project is split into data collection, exploratory data analysis (EDA), data cleaning,

###Data collection
