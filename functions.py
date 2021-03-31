#EDA was done to decide which datasets to use: mojo and IMDB
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

from prettytable import PrettyTable

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
    for i in range(3, len(df.columns)-1):
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

def give_regression(df):

    #Train-test split
    X, y = df, df['imdbscore']

    #Drop target
    X.drop(columns=['imdbscore'], inplace=True)

    #Add in domestic international ratio
    X['domestic_international_ratio'] = X['domestic_revenue'] / X['international_revenue']
    #Fill NA as 0 since this means there was no international release
    X['domestic_international_ratio'].fillna(value=0, inplace=True)
    #Fill NA as 0 as this means there was no opening relesase
    X['opening_revenue'].fillna(value=0, inplace=True)
    #Drop un-needed columns
    X.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue'], inplace=True)

    #Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state =10)

    #Baseline ...
    X_TrainBaseline = X_train.copy()
    X_TestBaseline = X_test.copy()
    X_TrainBaseline = X_TrainBaseline.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue',
                                 'opening_revenue', 'distributor'], axis=1)
    X_TestBaseline = X_TestBaseline.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue',
                                 'opening_revenue', 'distributor'], axis=1)
    print("Baseline got!")

    #Baseline w/ interactions ...
    X_TrainBaselineInteractions = create_interactions(X_TrainBaseline)
    X_TestBaselineInteractions = create_interactions(X_TestBaseline)
    print("Interactions between genres done!")

    X_TrainBaselineInteractions = X_TrainBaselineInteractions.drop(columns=['imdbscore'])
    X_TestBaselineInteractions = X_TestBaselineInteractions.drop(columns=['imdbscore'])

    print("Merge back in interactions to X_trian")
    X_train = X_train.merge(X_TrainBaselineInteractions.iloc[:, 26:380], how='inner', left_index=True, right_index=True)
    X_test = X_test.merge(X_TestBaselineInteractions.iloc[:, 26:380], how='inner', left_index=True, right_index=True)


    print("Remove un-necessary columns")
    X_train.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue'], inplace=True)
    X_test.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue'], inplace=True)



    #Baseline w/ interactions w/ one hot encoded distributor
    X_TrainBaselinev2 = one_hot_encode('distributor', X_train)
    X_TestBaselinev2 = one_hot_encode('distributor', X_test)
    print("Distributor is one-hot-encoded")

    X_TrainBaselinev2 = X_TrainBaselinev2.drop(columns=['imdbscore'])
    X_TestBaselinev2 = X_TestBaselinev2.drop(columns=['imdbscore'])

    X_TrainBaselinev2 = X_TrainBaselinev2.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue',
                                 'opening_revenue'], axis=1)
    X_TestBaselinev2 = X_TestBaselinev2.drop(columns=['mojo_title', 'international_revenue', 'domestic_revenue',
                                 'opening_revenue'], axis=1)

    scaler = preprocessing.StandardScaler()
    X_TrainBaselinev2Scaled = scaler.fit_transform(X_TrainBaselinev2.iloc[:, 2:])
    X_TestBaselinev2Scaled = scaler.fit_transform(X_TestBaselinev2.iloc[:, 2:])

    lm = LinearRegression()
    lm.fit(X_TrainBaselinev2, y_train)
    print(f'Linear regression (on TRAINING DATA) with genre-genre interaction terms AND OHE of distributor val R^2: {lm.score(X_TrainBaselinev2, y_train):.3f}')
    lm.fit(X_TestBaselinev2, y_test)
    print(f'Linear regression (on TEST DATA) with genre-genre interaction terms AND OHE of distributor val R^2: {lm.score(X_TestBaselinev2, y_test):.3f}')

    return X_TrainBaselinev2Scaled, X_TestBaselinev2Scaled, y_train, y_test
