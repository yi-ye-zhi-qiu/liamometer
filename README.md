## The Liam-o-meter 🥭 ![Python version](https://img.shields.io/badge/python-%E2%89%A53.6-blue.svg?style=flat-square&logo=python&logoColor=white)

### Linear regression analysis of IMDb Movie Ratings as an interpretive model for audience score based on genre & distributor

![Metis logo](images/metis.png) Metis data-science bootcamp project 2, **Jan. 11-22 2021**

- [See the final product](http://liamisaacs.com/liamometer)
- [Read the blog post](https://yeqiuu.medium.com/movie-ratings-for-fans-of-small-internationally-successful-studios-2b296ed179ec)
- Project was presented, [slides](final_presentation.pdf)

**Summary:**  FlaskApp of movies rated using a k- (5-) fold cross-validation lasso multiple linear regression model of IMDB scores (n=2316) scraped off the web, where we chose to use three features: genre (Action, Adventure, etc.), genre-genre interactions (Horror Thriller, for example), and movie distributor (Disney, Paramount, Other defined as <=5 movies/year, etc.) to analyze timeframe. This model is interpretive and the use case is: "Can we train a critic to think about movie ratings as if they are a fan of small, internationally-successful studios?"

----

Contributors:
- Liam
- Liam's Dad (helped run code after I got IP-banned from RottenTomatoes)

----

Requirements to run locally:

The scrapy spider & data analysis:

- `Python 3.6` or greater
- `jupyter notebook`
- `scrapy` `(pip3 install scrapy)`
- `scikit-learn==v0.22.0<=0.23.2` (necessary for yellowbrick `utils._safe_indexing` dependency)
- other modules: `pandas` `matplotlib` `seaborn` `numpy` `json` `regex` `fuzzywuzzy` `pprint` `yellowbrick`
- ~8 hours of time start to finish
- Strong willingness to get IP-banned from RottenTomatoes (just for a few days)

The web-scraping:

For a tutorial on web-scraping using Scrapy you can see my blogpost [here](https://yeqiuu.medium.com/tutorial-scraping-boxofficemojo-with-scrapy-299e7b35254e).

The WebApp:

- The FlaskApp is running on Ubuntu on an AWS AmazonLightsail server.

*Note:* we do not focus here on or include the code for deployment of a FlaskApp onto AWS, let alone the html/css/javascript used to display the data. This is because the FlaskApp is a part of my personal portfolio, and including all of the code for that here seems tangential to the point at hand: web scraping and linear regression. If you are interested, to view the code used to create the app see [here](https://github.com/yi-ye-zhi-qiu/personalwebsite).

----

How to run locally:
- follow directions in `spider.py` to change a few lines of code to match your local path, not mine

In your terminal:
- `cd boxoffice_scrapy`
- `scrapy crawl mojo_spider -L WARN`
- `scrapy crawl tomato_spider -L WARN`
- `scrapy crawl imdb_spider -L WARN`
- `scrapy crawl heirloom_spider -L WARN`
- `scrapy crawl metacritic_spider -L WARN`

Output
- in "boxoffice_scrapy": `heirloom.csv`, `imdb.csv`, `metacritic.csv`, `mojo.csv`, `tomatoes.csv`

----

### How it works

To follow along you can see the five notebooks. They are:
- Step I: EDA (exploring review sources)
- Step II: Data cleaning (removing MPAA Rating, Budget)
- Step III: Data modeling (one-hot encoding genre, genre-genre interactions, distributor) in the form of linear regression and degree 2 polynomial regression; metric used: R^2
- Step IV: Comparing our regularized and non-regularized linear and polynomial models via residual plots and Q-Q plots
- Step V: Making an html dataframe to use in a flask webapp (see `liamometer.py`, `app.py` and `/templates`)

----
