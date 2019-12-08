import requests
import json
from movie import Movie
from person import Person
import datetime as datetime
import os
import locale
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY']
omdb_api_key = os.environ['OMDB_API_KEY']

# Set the timeline (1 week)
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
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=fr"
        #print(url)
        r = requests.get(url)
        data = r.json()
        #print(data)
        imdb_id = data.get('imdb_id', None)
        title = data.get('title', None)
        original_title = data.get('original_title', None)
        release_date = data['release_date']
        duration = data['runtime']
        synopsis = data['overview'].replace("'", "''")
        production_budget = data['budget']

        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={omdb_api_key}"
        #print(url)
        r = requests.get(url)
        data_omdb = r.json()
        #print(data_omdb)
        score = data_omdb.get('imdbRating', None)
        rating = data_omdb.get('Rated', None)
        if rating == "PG-13":
            rating = "-12"
        if rating == "R":
            rating = "-18"
        elif rating in ["PG", "G"]:
            rating = "TP"

        print(imdb_id)
        print(title)
        print(original_title)
        print(release_date)
        print(duration)
        print(score)
        print(rating)
        print(production_budget)

        movie = Movie(title, original_title, duration, release_date)
        movie.imdb_id = imdb_id
        movie.score = score
        movie.synopsis = synopsis
        movie.production_budget = production_budget
        movie.rating = rating
        return movie
        
#Part II find movies from last week
    def tmdb_discover_movie(self):
        keep_going = True
        page = 1
        nbpage = ''
        movies=[]
        while keep_going:
            r = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&language=fr-FR&page=1&primary_release__year=2019&page="+str(page))
            data_results = r.json() #Take the Results sublcass
            nbpage = data_results['total_pages']
            #print(nbpage)
            data_results = data_results['results']
            for element in data_results: # For every element in the results subclass, apply the get_movie function
                id = element['id']
                #print(id)
                movie = self.tmdb_get_movie(id)
                movies.append(movie)
            if int(page) <= int(nbpage):
                page += 1
                time.sleep(0.25)
            else:
                keep_going = False
        return movies



TheMoviedb().tmdb_discover_movie()
#TheMoviedb().tmdb_get_movie('tt1560220')

