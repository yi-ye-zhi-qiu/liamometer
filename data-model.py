"""
Use scikit-learn, google NLP API, to model the data.
"""

"""
Based on past behavior? Something your friends like?

Given a set of people -- match --> item

Content-based recommendation system.. similar genres or smth..
Collaborative Filtering

Recommend stores near you that sell ethical eggplants?

Tells you how ripe a fruit is depending on image.

RipeBanana

dropdown on portfolio changes color scheme to mango/peach
and draws banana in the top-left?

HikeWhere

Gives you nearby hiking trails using Google Earth, that you may not have seen yet? Or is it the exploration of these things that's compelling...

"""


from sklearn.feature_extraction.text import CountVectorizer
text = ["London Paris London Eggplant", "Paris Paris London"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(text)
print(X.toarray())

#find cosine similarity (distance between vectors)
from sklearn.metrics.pairwise import cosine_similarity
print(cosine_similarity(X))

# [[1.         0.73029674]
#  [0.73029674 1.        ]]
#first text similar to that of 2nd text by 100%, second text to 0.73029674, etc.

#Need to construct similarity matrix of movies to say which ones are most similar to others... by using the angular distance
