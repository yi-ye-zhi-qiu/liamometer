# BoxOfficeMojo, Metacritic, IMDB, RottenTomatoes, and the-numbers data

import pandas as pd
#5 data sources, summing up to hopefully ~3k for all movies 2016-2020

mojo_df = pd.read_csv('boxoffice_scrapy/mojo_macm1.csv', index_col=[0])
metacritic_df = pd.read_csv('boxoffice_scrapy/metacritic.csv', index_col=[0])
imdb_df = pd.read_csv('boxoffice_scrapy/imdb.csv', index_col=[0])
rottentomatoes_df = pd.read_csv('boxoffice_scrapy/heirloom.csv', index_col=[0])
budget_df = pd.read_csv('boxoffice_scrapy/budget.csv', index_col=[0])

# ----- IGNORING metacritic_df as imdb_df has metacritic scores, & it's currently broken -------

movies_df = pd.concat([mojo_df, imdb_df, rottentomatoes_df, budget_df], axis=1, join='inner').sort_index()

# ------ GENERATE 'standardized scores' column for movies
# Need to take binomial probability of each review and calculate it that way
movies_df['standardized_score'] = (movies_df['imdbscore'] + movies_df['audiencescore'] + movies_df['metafromimdb'])/3

#sorts movies by highest audiencescore
movies_df.sort_values(by=['standardized_score'], ascending=True, inplace=True)
