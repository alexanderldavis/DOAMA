from json import load
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import urllib.parse
import requests as req
import json

Base = declarative_base()

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

class movies(Base):
    __tablename__='movie'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    description = Column(String)
    year = Column(String)
    rated = Column(String)
    runtime = Column(String)
    poster = Column(String)

    def __repr__(self):
        return "Movie: ({})".format(self.title)

class genres(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Genre: ({})".format(self.name)

class genres_movies(Base):
    __tablename__ = 'genres_movies'
    movieid = Column(Integer, ForeignKey('movie.id'))
    genreid = Column(Integer, ForeignKey('genre.id'))

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)
db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

t = req.get('https://raw.githubusercontent.com/alexanderldavis/DOAMA/master/finalMovieList.txt')
print("LIST SCRAPED FROM SOURCE")
data = t.text
data = data.split("\n")
idNum = 0
for movie in data:

    db.add(newmovie)
    res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
    dataParsed = json.loads(res.text)
    if dataParsed["Response"] != "False":
        rated = dataParsed["Rated"]
        newmovie = movies(title = dataParsed["Title"], description = dataParsed["Plot"], year = dataParsed["Year"], rated = dataParsed["Rated"], runtime = dataParsed["Runtime"], poster = dataParsed["Poster"])
        print("Added: ", dataParsed["Title"])

    db.commit()
    #     dataParsed = json.loads(res.text)
    #
    #     if dataParsed["Response"] != "False":
    #         rated = dataParsed["Rated"]
    #         cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster) VALUES (%s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"]))
    #         print("Added: ", dataParsed["Title"])
    #         # if dataParsed['Ratings']!=[]:
    #         #     for source in dataParsed['Ratings']:
    #         #         if source['Source']=="Rotten Tomatoes":
    #         #             rating=int(source['Value'][:len(source['Value'])-1])
    #         #         else:
    #         #             rating=None
    #         #         print(rating)
    #         genres = dataParsed["Genre"]
    #         genres = genres.split(", ")
    #         for genre in genres:
    #             if genre not in genreList:
    #                 cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
    #                 genreList.append(genre)
    #             cur.execute("""INSERT INTO genres_movies (movieid, genreid) VALUES (%s, (SELECT id FROM genres WHERE name = %s))""", (str(totalnumoffilms), genre))
    #         # actors = dataParsed["Actors"]
    #         # actors = actors.split(", ")
    #     #     for actor in actors:
    #     #         if actor not in actorList:
    #     #             cur.execute("""INSERT INTO actors (name) VALUES (%s)""", (actor,))
    #     #             actorList.append(actor)
    #     #         cur.execute("""INSERT INTO actors_movies (movieid, actorid) VALUES (%s, (SELECT id from actors WHERE name = %s))""", (str(totalnumoffilms), actor))
    #     conn.commit()
    # print("TABLE POPULATED")
    # print("===============================INFO===============================")
    # print("All Genres:", genreList)
    # print("Total Num of Films:", totalnumoffilms-1)
# db.commit()




# from flask import Flask, render_template, request, flash
# from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
# from flask_wtf import Form
# from flask_sqlalchemy import SQLAlchemy
# import requests as req
#
# app = Flask(__name__)
# app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
# app.secret_key = 'development key'
#
# class movies(db.Model):
#     __tablename__ = 'movies'
#     movieid = db.Column(db.Integer, primary_key= True)
#     title = db.Column(db.String)
#
#     def __init__(self, movieid, title):
#         self.movieid = movieid
#         self.title = title
#
#     def __repr__(self):
#         return '<id {}>'.format(self.title)
#
# t = req.get('https://raw.githubusercontent.com/alexanderldavis/DOAMA/master/finalMovieList.txt')
# print("LIST SCRAPED FROM SOURCE")
# data = t.text
# data = data.split("\n")
# idNum = 0
# for movie in data:
#     print(movie)
#     newmovie = movies(movieid = idNum, title=movie)
#     db.session.add(newmovie)
#     db.session.commit()

#####################################################################
############### OLD #####################
#####################################################################
# import psycopg2
# from flask import Flask, render_template, request
# import os
# from bs4 import BeautifulSoup
# import urllib.parse
# import requests as req
# import json
#
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
#
# conn = db
# #################### DELETE AND CREATE TABLES / HEROKU ####################
# cur = conn.cursor()
#
# # DROP ALL TABLES, CREATE ALL TABLES
# print("TABLES DELETED")
# cur.execute("""drop table movies CASCADE; CREATE table movies (id serial unique, title varchar(100), description text, year varchar(40), rated varchar(50), runtime varchar(50), poster varchar(200));""")
# cur.execute("""drop table genres CASCADE; drop table genres_movies CASCADE; CREATE table genres (id serial unique, name varchar(20)); CREATE table genres_movies (movieid int, genreid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (genreid) references genres(id), primary key (movieid, genreid));""")
# # cur.execute("""drop table if exists actors; CREATE table actors (id serial unique, name varchar(99)); CREATE table actors_movies (movieid int, actorid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (actorid) references actors(id), primary key (movieid, actorid));""")
# # cur.execute("""CREATE table services_movies (movie_id int, FOREIGN key(movie_id) references movies(id), service_id int, FOREIGN key(service_id) references services(id));""")
# # cur.execute("""CREATE table activities_movies (movie_id int, FOREIGN key (movie_id) references movies(id), activity_id int, FOREIGN key(activity_id) references activities(id));""")
# print("TABLES CREATED")
# conn.commit()
#
# # # POPULATE TABLE services
# # watchingOptions=['netflix_instant','amazon_prime_instant_video','hulu_movies','crackle','youtube_free','epix','streampix','snagfilms','fandor_streaming','amazon_video_rental','apple_itunes_rental','android_rental','vudu_rental','youtube_rental','sony_rental','vimeo_vod_rental','amazon_video_purchase','apple_itunes_purchase','android_purchase','vudu_purchase','xbox_purchase','sony_purchase','vimeo_vod_purchase','amazon_dvd','amazon_bluray','netflix_dvd','redbox','hbo','showtime','cinemax','starz','encore','xfinity_free']
# # for option in watchingOptions:
# #     cur.execute("""INSERT INTO services(name) VALUES (%s);""",(option,))
#
# # # POPULATE TABLE activities
# # activityList=['Family night','Girls night','Date night','Nerd night','Guys party','Cultured movie night','Surprise me']
# # for activity in activityList:
# #     cur.execute("""INSERT into activities(name) VALUES (%s);""",(activity,))
#
# t = req.get('https://raw.githubusercontent.com/alexanderldavis/DOAMA/master/finalMovieList.txt')
# print("LIST SCRAPED FROM SOURCE")
# data = t.text
# data = data.split("\n")
# genreList = []
# actorList = []
# totalnumoffilms=0
# for movie in data:
#     totalnumoffilms += 1
#     movieName = movie.replace(" ", "+")
#     res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
#     dataParsed = json.loads(res.text)
#
#     if dataParsed["Response"] != "False":
#         rated = dataParsed["Rated"]
#         cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster) VALUES (%s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"]))
#         print("Added: ", dataParsed["Title"])
#         # if dataParsed['Ratings']!=[]:
#         #     for source in dataParsed['Ratings']:
#         #         if source['Source']=="Rotten Tomatoes":
#         #             rating=int(source['Value'][:len(source['Value'])-1])
#         #         else:
#         #             rating=None
#         #         print(rating)
#         genres = dataParsed["Genre"]
#         genres = genres.split(", ")
#         for genre in genres:
#             if genre not in genreList:
#                 cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
#                 genreList.append(genre)
#             cur.execute("""INSERT INTO genres_movies (movieid, genreid) VALUES (%s, (SELECT id FROM genres WHERE name = %s))""", (str(totalnumoffilms), genre))
#         # actors = dataParsed["Actors"]
#         # actors = actors.split(", ")
#     #     for actor in actors:
#     #         if actor not in actorList:
#     #             cur.execute("""INSERT INTO actors (name) VALUES (%s)""", (actor,))
#     #             actorList.append(actor)
#     #         cur.execute("""INSERT INTO actors_movies (movieid, actorid) VALUES (%s, (SELECT id from actors WHERE name = %s))""", (str(totalnumoffilms), actor))
#     conn.commit()
# print("TABLE POPULATED")
# print("===============================INFO===============================")
# print("All Genres:", genreList)
# print("Total Num of Films:", totalnumoffilms-1)
#


#####################################################################
############### REALLY OLD #####################
#####################################################################
# #heroku run python3 init.py
# import psycopg2
# from flask import Flask, render_template, request
# import os
# from bs4 import BeautifulSoup
# import urllib.parse
# import requests as req
# import json
# # from canistreamit import search, streaming, rental, purchase, dvd, xfinity
#
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
#
# conn = db
# #################### CREATE TABLES / KNUTH ####################
# cur = conn.cursor()
# # cur.execute("DROP table services CASCADE; DROP table acitvities CASCADE; DROP table activities_movies CASCADE;DROP table services_movies CASCADE; DROP table movies CASCADE; DROP table genres CASCADE; DROP table genres_movies CASCADE; DROP table actors CASCADE; DROP table actors_movies CASCADE;")
# cur.execute("drop table if exists activities_movies; drop table if exists services_movies;drop table if exists genres_movies; drop table if exists actors_movies;")
# print("TABLES DELETED")
# cur.execute("""drop table if exists movies; CREATE table movies (id serial unique, title varchar(100), description text, year varchar(40), rated varchar(50), runtime varchar(50), poster varchar(200), rating int);""")
# cur.execute("""drop table if exists genres; CREATE table genres (id serial unique, name varchar(20)); CREATE table genres_movies (movieid int, genreid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (genreid) references genres(id), primary key (movieid, genreid));""")
# cur.execute("""drop table if exists actors; CREATE table actors (id serial unique, name varchar(99)); CREATE table actors_movies (movieid int, actorid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (actorid) references actors(id), primary key (movieid, actorid));""")
# cur.execute("""drop table if exists services; CREATE table services (id serial unique, name text);""")
# cur.execute("""drop table if exists activities; CREATE table activities (id serial unique, name text);""")
# cur.execute(""" CREATE table services_movies (movie_id int, FOREIGN key(movie_id) references movies(id), service_id int, FOREIGN key(service_id) references services(id));""")
# cur.execute("""CREATE table activities_movies (movie_id int, FOREIGN key (movie_id) references movies(id), activity_id int, FOREIGN key(activity_id) references activities(id));""")
# print("TABLES CREATED")
# conn.commit()
# # create table for streaming channels
# watchingOptions=['netflix_instant','amazon_prime_instant_video','hulu_movies','crackle','youtube_free','epix','streampix','snagfilms','fandor_streaming','amazon_video_rental','apple_itunes_rental','android_rental','vudu_rental','youtube_rental','sony_rental','vimeo_vod_rental','amazon_video_purchase','apple_itunes_purchase','android_purchase','vudu_purchase','xbox_purchase','sony_purchase','vimeo_vod_purchase\
# ','amazon_dvd','amazon_bluray','netflix_dvd','redbox','hbo','showtime','cinemax','starz','encore','xfinity_free']
# for option in watchingOptions:
#     cur.execute("""INSERT INTO services(name) VALUES (%s);""",(option,))
#
# # create tables for activity:
# activityList=['Family night','Girls night','Date night','Nerd night','Guys party','Cultured movie night','Surprise me']
# for activity in activityList:
#     cur.execute("""INSERT into activities(name) VALUES (%s);""",(activity,))
#
# # t = req.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
# # print("LIST SCRAPED FROM SOURCE")
# # soup=BeautifulSoup(t.text,"html.parser")
# # soup.prettify()
# # data=soup.find_all("td", { "class" : "csv_column_3" })
# file=open("finalMovieList.txt","r")
# data=file.readlines()
# totalnumoffilms=0
# genreList = []
# actorList = []
# for i in range(1,len(data)):
#     movieName = data[i].replace("\n","")
#     finalString = ""
#     if "," in movieName:
#         s = movieName.split(", ")
#         s.reverse()
#         for i in s:
#             finalString += i + " "
#         movieName = finalString[:-1]
#     if "' " in movieName:
#         movieName = movieName.replace("' ", "'")
#     movieName = movieName.replace(" ", "+")
#     res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
#     dataParsed = json.loads(res.text)
#
#     if dataParsed["Response"] != "False":
#         totalnumoffilms+=1
#         rottenTomatoes=dataParsed["Ratings"][1] #rating is taken from rotten tomatoes
#         rating=int(rottenTomatoes['Value'][:len(rottenTomatoes['Value'])-1])
#         print(rating)
#         if dataParsed["Poster"] != "N/A":
#             cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster, rating) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"],rating))
#         else:
#             cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster, rating) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],"http://www.projectdoama.com/static/penguin.jpg",rating))
#         print("Added: ",dataParsed["Title"])
#         # search for availability in different gate
#         # movie=search(dataParsed['Title'])[0]
#         # streamingList=streaming(movie['_id'])
#         # rentalList=rental(movie['_id'])
#         # purchaseList=purchase(movie['_id'])
#         # dvdList=dvd(movie['_id'])
#         # cableList=xfinity(movie['_id'])
#         # for li in [streamingList,rentalList,purchaseList,dvdList,cableList]:
#         #     if li!=[]:
#         #         keys=li.keys()
#         #         for key in keys:
#         #             # cur.execute("""INSERT INTO services(name) VALUES (%s);""",(li[key]))
#         #             cur.execute("""INSERT INTO services_movies(movie_id,service_id) VALUES ((select id from movies where title=%s),(select id from services where name=%s));""",(dataParsed['Title'],key))
#         genres = dataParsed["Genre"]
#         genres = genres.split(", ")
#         for genre in genres:
#             if genre not in genreList:
#                 cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
#                 genreList.append(genre)
#             # TODO: ASK ABOUT USING RETURNING IN SQL TO GET THE MOVIEID
#             cur.execute("""INSERT INTO genres_movies (movieid, genreid) VALUES (%s, (SELECT id FROM genres WHERE name = %s))""", (str(totalnumoffilms), genre))
#         # create entries for activities_movies table
#         if "Adventure" in genres or "Comedy" in genres or "Mistery" in genres or "Fantasy" in genres or "Animation" in genres:
#             if dataParsed['Rated']=="PG13" or dataParsed['Rated']=='PG':
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Family night'))""",(dataParsed['Title'],))
#         if "Romance" in genres or "Drama" in genres or "Comedy" in genres or "Fantasy" in genres or "Animation" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Girls night'))""",(dataParsed['Title'],))
#         if "Romance" in genres or "Horror" in genres or "Drama" in genres or "Thriller" in genres or "Fantasy" in genres or "Animation" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Date night'))""",(dataParsed['Title'],))
#         if "Mistery" in genres or "Sci-Fi" in genres or "Crime" in genres or "Comedy" in genres or "Adventure"in genres or "Documentary" in genres or "War" in genres or "Biography" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Nerd night'))""",(dataParsed['Title'],))
#         if "Comedy" in genres or "Horror" in genres or "Thriller" in genres or "Adventure" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Guy party'))""",(dataParsed['Title'],))
#         if "Western" in genres or "War" in genres or "Short" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Cultured movie night'))""",(dataParsed['Title'],))
#         if "Short" in genres or "Animation" in genres:
#                 cur.execute("""INSERT INTO activities_movies(movie_id,activity_id) VALUES ((SELECT id FROM movies WHERE title=%s),(SELECT id FROM activities WHERE name='Surprise me'))""",(dataParsed['Title'],))
#
#         actors = dataParsed["Actors"]
#         actors = actors.split(", ")
#         for actor in actors:
#             if actor not in actorList:
#                 cur.execute("""INSERT INTO actors (name) VALUES (%s)""", (actor,))
#                 actorList.append(actor)
#             cur.execute("""INSERT INTO actors_movies (movieid, actorid) VALUES (%s, (SELECT id from actors WHERE name = %s))""", (str(totalnumoffilms), actor))
#     conn.commit()
#
# print("TABLE POPULATED")
# print("===============================INFO===============================")
# print("All Genres:", genreList)
# print("Total Num of Films:", totalnumoffilms-1)
