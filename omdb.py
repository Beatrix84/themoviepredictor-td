import requests
import json
from movie import Movie
from datetime import datetime
import os
import locale

#from dotenv import load_dotenv

#load_dotenv()

omdb_api_key = os.environ['OMDB_API_KEY']

class Omdb:
    def __init__(self):
        self.host = 'http://www.omdbapi.com'

    def omdb_get_movie(self, id):
        movie_id = id
        r = requests.get(f"http://www.omdbapi.com/?i={movie_id}&apikey={omdb_api_key}")
        data = r.json()
        imdb_id = data['imdbID']
        original_title = data['Title']
        title = data['Title']
        release_date = datetime.strptime(data['Released'], '%d %b %Y').date()
        duration = None
        rating = data['Rated']
        if rating == "PG-13":
            rating = "-12"
        elif rating in ["PG", "G"]:
            rating = "TP"
        
            
        
        #print(imdb_id)
        #print(title)
        #print(original_title)
        #print(release_date)
        #print(duration)
        #print(rating)

        movie = Movie(title, original_title, duration, release_date, rating)
        movie.imdb_id = imdb_id
        return movie

Omdb().omdb_get_movie('tt3896198')
