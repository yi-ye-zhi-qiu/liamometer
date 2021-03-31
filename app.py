#Import flask
from flask import *
from flask import Flask, render_template, request, jsonify, make_response

#import models
from models.liamometer import _movie_data

app = Flask(__name__)

#Liamometer page
@app.route('/')
def show_liamometer():
    """
    Performs linear regression on scraped databases (IMDB, BoxOfficeMojo).
    Returns 500 rows, just because I do not want to overload the page (currently working on lazy-load in javascript, or loading as you scroll.)
    """
    max, liams_favorite, html_data = _movie_data()

    return render_template('liamometer.html', max=max, liams_favorite_movie_image = '',
                            liams_favorite=liams_favorite, html_data = html_data)

if __name__ == '__main__':
    app.run()
