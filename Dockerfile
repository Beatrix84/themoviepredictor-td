FROM python:3.7-buster

RUN pip install argparse mysql-connector-python beautifulsoup4 requests

COPY . /usr/src/themoviepredictor

WORKDIR /usr/src/themoviepredictor 
#to remove the request cd /usr/src/themoviepredictor
CMD python /usr/src/themoviepredictor/app.py movies import --api themoviepredictor --imdbId tt1234567
#api.all --for 7 to show all the movies update during the latest 7 days