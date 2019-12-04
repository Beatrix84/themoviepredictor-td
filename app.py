#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

#Import all librairies

import mysql.connector
import sys
import argparse
import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#import locale

#Import all classes
from movie import Movie
from person import Person
from tmdb import TheMoviedb
from omdb import Omdb

#locale.setlocale(locale.LC_ALL, 'fr_FR')

#Connect to MYSQL database for our table on Adminer
def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='database',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

#Query: find in our tables (people and movies) depending on id
def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {} LIMIT 1".format(table, id))

#Query: find all in our tables
def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

#Query: insert person in the people table with all columns requested (call the class person)
def insert_people_query(person):
    return (f"INSERT INTO `people` (`firstname`, `lastname`) VALUES ('{person.firstname}', '{person.lastname}');")

#Query: insert a movie in the movies table with all columns requested (call the class movie)
def insert_movie_query(movie):
    add_movie = ("INSERT INTO movies "
                "(imdb_id, title, original_title, duration, release_date, rating) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    new_movie = (movie.imdb_id, movie.title, movie.original_title, movie.duration, movie.release_date, movie.rating)
    return (add_movie, new_movie)


def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()

    entity = None
    if (cursor.rowcount == 1):
        row = results[0]
        
        if (table == "movies"):
            entity = Movie(row['title'], row['original_title'], row['duration'], row['release_date'], row['rating'])
            entity.id = row['id']
        if (table == "people"):
            entity = Person(row['firstname'], row['lastname'])
            entity.id = row['id']

    closeCursor(cursor)
    disconnectDatabase(cnx)

    return entity

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall() # liste de dictionnaires contenant des valeurs scalaires
    closeCursor(cursor)
    disconnectDatabase(cnx)

    if (table == "movies"):
        movies = []
        for result in results: # result: dictionnaire avec id, title, ...
            movie = Movie(
                title=result['title'],
                original_title=result['original_title'],
                duration=result['duration'],
                release_date=result['release_date'],
                rating=result['rating']
            )
            movie.id = result['id']
            movies.append(movie)
        return movies
    
    if (table == "people"):
        people = []
        for result in results: # result: dictionary avec id, title, ...
            person = Person(
                firstname=result['firstname'],
                lastname=result['lastname']
            )
            person.id = result['id']
            people.append(person)
        return people


def insert_people(person):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insert_people_query(person))
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id
 
def insert_movie(movie):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    (add_movie, new_movie) = insert_movie_query(movie)
    cursor.execute(add_movie, params=new_movie)
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id

def printPerson(person):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=('people', 'movies'), help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètre')
find_parser.add_argument('id' , help='Identifant à rechercher')

import_parser = action_subparser.add_parser('import', help='Importer un fichier CSV')
import_parser.add_argument('--file', help='Chemin vers le fichier à importer', required=False) #before introudcing api it was =true
import_parser.add_argument('--api', help='Path to the API for movies', required=False) #Add import parser for apis and imdb_id movies
import_parser.add_argument('--imdb_id', help='Path to the imdb_id of the movie', required=False)

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')

known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname' , help='Prénom de la nouvelle personne', required=True)
    insert_parser.add_argument('--lastname' , help='Nom de la nouvelle personne', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title' , help='Titre en France', required=True)
    insert_parser.add_argument('--duration' , help='Durée du film', type=int, required=True)
    insert_parser.add_argument('--original-title' , help='Titre original', required=True)
    insert_parser.add_argument('--release-date' , help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating' , help='Classification du film', choices=('TP', '-12', '-16'), required=True)

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        person = find("people", peopleId)
        if (person == None):
            print(f"Aucune personne avec l'id {peopleId} n'a été trouvé ! Try Again!")
        else:
            printPerson(person)
    
    if args.action == "insert":
        print(f"Insertion d'une nouvelle personne: {args.firstname} {args.lastname}")
        person = Person(firstname=args.firstname, lastname=args.lastname)
        people_id = insert_people(person)
        print(f"Nouvelle personne insérée avec l'id '{people_id}'")

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = find("movies", movieId)
        if (movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé ! Try Again!")
        else:
            printMovie(movie)
    if args.action == "insert":
        print(f"Insertion d'un nouveau film: {args.title}")
        movie = Movie(args.title, args.original_title, args.duration, args.release_date, args.rating)
        movie_id = insert_movie(movie)
        print(f"Nouveau film inséré avec l'id '{movie_id}'")
    if args.action == "import": # Import from a csv file 
        if args.file:
            with open(args.file, 'r', encoding='utf-8', newline='\n') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    movie = Movie(
                        imdb_id=row['imdb_id'],
                        title=row['title'],
                        original_title=row['original_title'],
                        duration=row['duration'],
                        rating=row['rating'],
                        release_date=row['release_date'])
                    movie_id = insert_movie(movie)

            print(f"Nouveau film inséré avec l'id '{movie_id}'")

        if args.api == 'themoviedb': #Import from api movie tmdb
            if args.imdb_id :
                movie = TheMoviedb().tmdb_get_movie(args.imdb_id)
                insert_movie(movie)
                print("insert")
        
        if args.api == 'omdb': #Import from api movie omdb
            if args.imdb_id :
                movie = Omdb().omdb_get_movie(args.imdb_id)
                insert_movie(movie)
                print("insert")


