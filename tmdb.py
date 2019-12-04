import requests
import json
from movie import Movie
import datetime as datetime
import os
import locale
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY']

today_date = datetime.date.today()
n = 7 
date_n_days_ago = today_date - datetime.timedelta(days=n)
#print(today_date)
#print(date_n_days_ago)

class TheMoviedb:
    def __init__(self):
        self.host = 'https://api.themoviedb.org/3'

    def tmdb_get_movie(self, id):
        movie_id = id
        r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=fr")
        data = r.json()
        imdb_id = data['imdb_id']
        title = data['title']
        original_title = data['original_title']
        release_date = data['release_date']
        duration = data['runtime']

        #print(imdb_id)
        #print(title)
        #print(original_title)
        #print(release_date)
        #print(duration)

        movie = Movie(title, original_title, duration, release_date)
        movie.imdb_id = imdb_id
        return movie
        
#Part II find movies from last week
    def tmdb_discover_movie(self):
        r = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=fr-FR&page=1&primary_release_date.gte={date_n_days_ago}&primary_release_date.lte={today_date}")
        data_results = r.json()['results'] #Take the Results sublcass
        for element in data_results: # For every element in the results subclass, apply the get_movie function
            element.tmdb_get_movie()

        

TheMoviedb().tmdb_get_movie('tt4777008')
