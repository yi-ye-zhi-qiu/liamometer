from flask import *
import pandas as pd
from functools import reduce

app = Flask(__name__)

def get_data():


    return df
    # ------ GENERATE 'standardized scores' column for movies
    # Need to take binomial probability of each review and calculate it that way

def get_image(df):
    return df['imdbpicture']

@app.route('/')
def home():
    mojo_df = pd.read_csv('data/mojo.csv', index_col=[0])
    metacritic_df = pd.read_csv('data/metacritic.csv', index_col=[0])
    imdb_df = pd.read_csv('data/imdb.csv', index_col=[0])
    rottentomatoes_df = pd.read_csv('data/rotten_tomatoes.csv', index_col=[0])

    # ----- Fix metacritic and imdb ----- #
    # ----- Error in code has been fixed, but these were initially off by 1 row ---- #

    #metacritic_df = metacritic_df.shift(-1)
    #imdb_df = imdb_df.shift(-1)

    dfs = [mojo_df, metacritic_df, imdb_df, rottentomatoes_df]
    df = reduce(lambda left,right: pd.merge(left,right,on='mojo_title'), dfs)
    df.drop_duplicates(subset=['tomato_title'], inplace=True)
    #1791 rows for 2016-2020 data
    #html_data = df.head(15)
    name = df['tomato_title']

    df['domestic_revenue'] = df['domestic_revenue'].str.replace(',', '')
    df['domestic_revenue'] = df['domestic_revenue'].str.replace('$', '')
    df['domestic_revenue'] = pd.to_numeric(df['domestic_revenue'])
    df = df.sort_values(by=['domestic_revenue'], ascending=False)
    html_data = df
    return render_template('index.html', name = name, html_data = html_data)
#5 data sources, summing up to hopefully ~3k for all movies 2016-2020


if __name__ == '__main__':
   app.run(debug = True)
