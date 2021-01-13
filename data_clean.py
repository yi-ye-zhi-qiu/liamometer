"""
Retrieve & clean data.
要拿data，有data之后，要打扫打扫🧹

Start with movies (pracitce-r)
用movies来练习一点点
asd
"""


## WANT: title, genre, release date, gross_$
## SLOW: BeautifulSoup

from bs4 import BeautifulSoup as soup
import requests as req
import re
import pandas as pd
import numpy as np
import time


def get_df():

    #parent = top movies for 2020
    url = "https://www.boxofficemojo.com/year/2020/?sortDir=asc&sort=rank&grossesOption=totalGrosses"
    res = req.get(url)
    parent_content = soup(res.content, 'html.parser')
    parent_link = parent_content.find_all('td', class_='a-text-right mojo-header-column mojo-truncate mojo-field-type-rank mojo-sort-column')

    #lazy way of grabbing titles and links
    raw_parent = parent_content.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
    parent_name, parent_link = [], []
    for name in raw_parent:
        parent_name.append(name.find('a').getText())
        parent_link.append(name.find('a')['href'])

    #lazy way of getting gross income of a movie
    raw_gross = parent_content.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
    gross = []
    for movie in raw_gross:
        gross.append(movie)

    genres, release_dates, elms = [], [], []

    #just for now, to control data volume restricted tofirst 4 rows
    parent_link = parent_link[:4]

    #iterate through parent_links and grab genre, release date
    for i in parent_link:
        try:

            child_url = 'https://www.boxofficemojo.com' + i
            child_req = req.get(child_url)
            child_content = soup(child_req.content, 'html.parser')
            #supply tuple list of things we want to find
            for elm in child_content.find_all('span', text=lambda value: value and value.startswith(("Genre", "Release Date"))):
                elms.append(re.sub("\s{1,}", " ", elm.nextSibling.text.replace('\n', '')))

            genres = [e for e in elms if elms.index(e) %2==0]
            release_date = [e for e in elms if elms.index(e) %2 != 0]

            time.sleep(1)

        except req.exceptions.ConnectionError:
            child_req.status_code = 'Connection refused by boxoficemojo, likely due to too many attempts to connect. Try importing time and using time.sleep between requests to url.'

    #have to avoid arrays of differing lengths,
    movies = {'title': parent_name, 'gross': gross, 'genre': genres, 'release date': release_date}
    #take movies and construct df from dict of array-like titles, genres
    df = pd.DataFrame.from_dict(movies, orient='index')
    df = df.transpose()
    print(df)
    return df

get_df()
