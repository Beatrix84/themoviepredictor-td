# The Movie predictor

## Objectif: fill the 'The Movie Preictor database' with new movies and people from different sources

### Setup:

* Create a docker-compose.yml document with all informations :
  - services, network and volumes
  - enviroments variable link called env_file (reference to the .env file)
* Create a .env document with all keys requested for the applications (tmdb_key, omdb_key and MYSQL_key)
* Create a .gitignore document where we put all the informations we wont show (add the .env file in it)
* Create a .dockerignore document (the same as .gitignore)
* Create a dockerfile containing all informations to create the image

### Start:

* In the commander line:
  $ docker-compose up
* In a new commander window:
  $ winpty docker-compose exec app sh

### Code:

* Import all usefull libraries
* Create classes for differents objects: movies.py, person.py, apis (tmdb.py, omdb.py)
* Call the classes using functions in the main app.py
* Create arguments for differents actions(find, list, insert, import) depending on the different context (movie, people)

### Commands:

* Use differents command to show, find, insert, import informations from and into the database:
  - $ python app.py people list
  - $ python app.py movies list
  - $ python app.py people insert --firstname "John" --lastname "Doe"
  - $ python app.py movies insert --title "Star Wars, épisode VIII : Les Derniers Jedi" --duration 152 --original-title "Star Wars: Episode VIII – The Last Jedi" --origin-country US
  - $ python app.py movies import --file new_movies.csv
  - $ python app.py import --api themoviedb --imdbld tt340493
  - $ python app.py movies import --api themoviedb --year 2018
  - $ python app.py movies import --api themoviedb --imdb_id tt420809
  - $ python app.py movies import --api omdb --imdb_id tt3896198





