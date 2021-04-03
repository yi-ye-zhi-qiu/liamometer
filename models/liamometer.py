from models.liamometer_helpers import *

import pandas as pd

mojo = pd.read_csv('/Users/liamisaacs/Desktop/github repositories/metis-project2/data/mojo.csv')
imdb = pd.read_csv('/Users/liamisaacs/Desktop/github repositories/metis-project2/data/imdb.csv')
movie_images = pd.read_csv('/Users/liamisaacs/Desktop/github repositories/metis-project2/data/movie_images.csv')

html_ = give_html(mojo, imdb, movie_images)
#Ignore the first row because I just can't handle admitting that Sunset Blvd., a re-release from 1950, is my favorite movie it's too much
html_ = html_.iloc[1:, :]

def _movie_data():



    max = html_['pred'].max()
    highest_rated = html_[html_['pred'] == max]['mojo_title']

    hR_values = highest_rated.values

    return max, highest_rated, html_
