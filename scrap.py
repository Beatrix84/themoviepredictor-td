#!/usr/bin/python
# -*- coding: utf-8 -*-



#took all the time the parent to put the get_text
#/see why the span remove doesn't work
#  see the time PT..M


import mysql.connector
import sys
import argparse
import csv
import requests
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import locale
import isodate

locale.setlocale(locale.LC_ALL, 'en_US')

r = requests.get('https://www.imdb.com/title/tt2527338/?ref_=nv_sr_2?ref_=nv_sr_2')
soup = BeautifulSoup(r.text, 'html.parser')
#find the div title
title_wrapper = soup.find('div', class_='title_wrapper')
#find the title h1 children
title = title_wrapper.find('h1', class_="").get_text()
#print(title)

#remove the year (span)
span_tag = soup.find('span', id='titleYear')
span_tag.replace_with('')
#print(title)

#Find the original_title (div) sibling to h1
original_title = title_wrapper.find('div', class_='originalTitle').get_text().strip()
#remove the span tag
span_tag = title_wrapper.find('span', class_="description")
span_tag.replace_with('')
#print(original_title)

#Find the rating
rating_tag = title_wrapper.find('div', class_='subtext')
if rating_tag.find('12') != -1:
    rating = '-12'
#print(rating)

#Find the duration
time_tag = isodate.parse_duration(title_wrapper.find('time').get('datetime'))
duration = (int(time_tag.total_seconds()/60))
#print(duration)

#Find release date
release_date_tag = title_wrapper.find('a', attrs={'title':'See more release dates'}).get_text().split("(")[0]
release_date_as_string = release_date_tag.strip()
release_date_object = datetime.strptime(release_date_as_string, '%d %B %Y')
release_date_sql_string = release_date_object.strftime('%Y-%m-%d')
release_date_soup = release_date_sql_string
#print(release_date_soup)

print('title = ', title)
print('original_title = ', original_title)
print('rating = ', rating)
print('duration =', duration)
print('release_date = ', release_date_soup)

exit()
