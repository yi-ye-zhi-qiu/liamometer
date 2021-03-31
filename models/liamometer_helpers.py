#EDA was done to decide which datasets to use: mojo and IMDB
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

import re

#Data cleaning
def get_clean_data(mojo, imdb):
    """
    Cleans data specific to needs of liamometer

    Parameters: mojo & imdb data sets
    """

    mojo.set_index(['mojo_title'])
    imdb.set_index(['mojo_title'])

    df = mojo.merge(imdb, on='mojo_title', how='left')

    df.drop(columns=['budget', 'MPAA', 'imdbpicture', 'imdbcount', 'imdb_metacritic', 'release_days', 'opening_theaters'], inplace=True)
    df = df.dropna(subset=['imdbscore'])

    money_cols = ['domestic_revenue', 'international_revenue', 'world_revenue', 'opening_revenue']

    for i in money_cols:
        df[i] = df[i].str.replace(',', '')
        df[i] = df[i].str.replace('$', '')
        df[i] = pd.to_numeric(df[i])

    #Drop any Link errors
    df = df[df['imdbscore'] != 'Link error']

    return df

#Data modeling

def one_hot_encode(x, df):
    """
    One hot encodes a column
    Parameters: x = column name, df = dataframe
    """
    df = df.dropna(subset=[x])
    l = np.unique(', '.join(df[x]).split(', '))
    l = np.delete(l, np.where(l == 'NA'))
    for option in l:
        df[option] = df[x].str.contains(option).astype('int')
    df.drop(x, axis=1, inplace=True)
    return df

def create_interactions(df):
    """
    Creates interaction terms in a df
    """
    df_int = df.copy()
    #range skips over things we do not want to interact with
    for i in range(2, len(df.columns)-1):
        for j in range(i+1, len(df.columns)):
            name = str(df.columns[i]) + ' * ' + str(df.columns[j])
            df_int.loc[:, name] = df[str(df.columns[i+1])] * df[str(df.columns[j])]
    return df_int

def mae(y_true, y_pred):
    return np.mean(np.abs(y_pred - y_true))

def replace_(df, col, threshold):
    """
    Replace df col if appears less than threshold times
    """
    find_replace = df[col].value_counts()
    other = list(find_replace[find_replace <= threshold].index)

    df[''.join(col)] = df[''.join(col)].replace(other, 'Other')
    return df

def run_linear(X, y):
    """
    Runs a linear regression by scaling data first
    """
    scaler = preprocessing.StandardScaler()
    X_ = scaler.fit_transform(X)
    lr = LinearRegression()
    lr.fit(X_, y)
    print(f'Linear regression val R^2: {lr.score(X_, y):.3f}')

def give_X_y(df):

    df = one_hot_encode('genres', df)
    df = replace_(df, 'distributor', 40)
    #df = one_hot_encode('distributor', df)

    #Train-test split
    X, y = df, df['imdbscore']
    y = pd.to_numeric(y)
    X.drop(columns=['imdbscore'], inplace=True)
    X['domestic_international_ratio'] = X['domestic_revenue'] / X['international_revenue']
    X['domestic_international_ratio'].fillna(value=0, inplace=True)
    X['opening_revenue'].fillna(value=0, inplace=True)
    #Division for ratio creates a float; opening revenue naturally is a float
    #We convert to integer like this
    for col in ['domestic_international_ratio', 'opening_revenue']:
        X[col] = X[col].astype(int)
    X.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue'], inplace=True)
    # shift column 'Name' to first position
    first_column = X.pop('domestic_international_ratio')
    # insert column using insert(position,column_name,
    # first_column) function
    X = X.iloc[:, 3:]

    X.insert(3, 'domestic_international_ratio', first_column)
    return X, y

def give_polynomialregression(mojo, imdb):
    """
    Gives regression model which is most optimal, as per Step III notebook
    The model is 2-degree polynomial regression
    """
    df = get_clean_data(mojo, imdb)
    X, y = give_X_y(df)


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state =10)

    poly = PolynomialFeatures(degree=2, interaction_only = True)
    X_train_poly = poly.fit_transform(X_train.values)
    X_test_poly = poly.fit_transform(X_test.values)

    # poly = PolynomialFeatures(degree=2, interaction_only = True)
    # X_train = poly.fit_transform(X_train.values)
    # X_test = poly.fit_transform(X_test.values)

    return X_train_poly, X_test_poly, y_train, y_test

def give_linearregression(mojo, imdb):
    """
    Gives regression model which is most optimal, as per Step III notebook
    The model is linear regression
    """
    df = get_clean_data(mojo, imdb)
    X, y = give_X_y(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state =10)

    scaler = preprocessing.StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    return X_train, X_test, y_train, y_test

def get_img_url(df):
    return re.findall('(?<=data-src).*$', df)[0][2:-2]

def give_html(mojo, imdb, movie_images):
    """
    Gives most optimal regression model, merges back in predictions to original dataframe, such that
    'Spirited Away' is now associated with both an IMDB and liamometer score.
    """
    df = get_clean_data(mojo, imdb)
    X, y = give_X_y(df)

    #Clean movie images to be clear src tags
    movie_images.set_index(['mojo_title'])
    movie_images.dropna(subset=['tomato_image'], inplace=True)
    movie_images.drop(columns=['url', 'tomato_criticcount', 'tomato_audiencecount'], inplace=True)
    movie_images['tomato_image'] = movie_images['tomato_image'].apply(get_img_url)

    #Fit 5-fold Lasso on entire X (no train-test-split), so we scale all of X
    scaler = preprocessing.StandardScaler()
    X_scaled = scaler.fit_transform(X)

    """
    You can choose not to use polynomial regression:
    In doing so, results vary basically none at all using regularization,
    If you want you can just run a non-regularized linear regression model:
    model = LinearRegression()
    model.fit(X_scaled, y)


    #The number of folds is also pretty irrelevant..
    model = LassoCV(cv=5)
    model.fit(X_scaled, y)
    #Create predictions array
    pred_ = model.predict(X_scaled)
    """

    """
    If you want to use polynomial reguression instead (which is a higher R^2, and results are better (more varied))
    """

    poly = PolynomialFeatures(degree=2, interaction_only = True)
    X_poly = poly.fit_transform(X.values)

    #no Lasso CV for polynomial:
    #lr = LinearRegression()
    #lr.fit(X_poly, y)

    #With Lasso CV:
    model = RidgeCV(cv=5)
    model.fit(X_poly, y)
    pred_ = model.predict(X_poly)

    #Make pandas series (new column called 'pred') equal to each # in predictions array
    X['pred'] = pred_

    df = df.merge(X, right_index=True, left_index=True)
    #Add in movie images, inner join to preserve only movies that have images
    df = df.merge(movie_images, on='mojo_title', how='inner')
    #Sort by liamometer score
    df = df.sort_values(by=['pred'], ascending=False)
    #Get rid of any images we don't have (sanity check)
    df = df.dropna(subset=['tomato_image'])
    #Round to just one decimal point
    df['pred'] = df['pred'].round(1)

    #Drop duplicate movies
    df.drop_duplicates(subset=['mojo_title'], inplace=True)

    html_ = df
    return html_
