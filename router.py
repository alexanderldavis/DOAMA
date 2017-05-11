from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, jsonify
import json, os
from flask_wtf import Form
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from wtforms import StringField, SelectField
from json import dumps, loads
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import requests as req
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, create_engine, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)


app.config['SQLALCHEMY_DATABASE_URI']=os.environ["DATABASE_URL"]
# db = SQLAlchemy(app)
# engine = create_engine(os.environ["DATABASE_URL"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wtforms more like wtf forms'
db = SQLAlchemy(app)

Base = declarative_base()
movie_genre=Table('movie_genre',Base.metadata,Column('movie_id',Integer,ForeignKey('movie.id')),Column('genre_id',Integer,ForeignKey('genre.id')))
movie_actor=Table('movie_actor',Base.metadata,Column('movie_id',Integer,ForeignKey('movie.id')),Column('actor_id',Integer,ForeignKey('actor.id')))

class Movie(Base):
    __tablename__='movie'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    description=Column(String)
    year=Column(String)
    rated=Column(String)
    runtime=Column(String)
    poster = Column(String)
    rating = Column(Integer)
    genres=relationship("Genre", secondary=movie_genre,back_populates="inMovie")
    actors=relationship("Actor", secondary=movie_actor,back_populates="inMovie")

    def __repr__(self):
        return "Movie: ({})".format(self.title)
class Genre(Base):
    __tablename__="genre"
    id=Column(Integer,primary_key=True)
    genre=Column(String)
    inMovie=relationship("Movie", secondary=movie_genre, back_populates="genres")

    def __repr__(self):
        return "Genre({})".format(self.genre)

class Actor(Base):
    __tablename__="actor"
    id=Column(Integer, primary_key=True)
    actor=Column(String)
    inMovie=relationship("Movie", secondary=movie_actor, back_populates="actors")

class SearchForm(Form):
    options = SelectField('Search By:', [validators.Required()], choices=[('FamilyNight', 'Family Night'), ('DateNight', 'Date Night'),('GirlsNight', 'Girls Night'),('GuysNight', 'Guys Night'), ('NerdNight', 'Nerd Night'), ('CulturedNight', 'Cultured Movie Night'), ('SurpriseMe', 'Surprise Me')])

@app.route("/", methods=['GET'])
def index():
    form = SearchForm()
    res = db.session.execute("""SELECT id, genre from genre;""")
    res = res.fetchall()
    return render_template('welcome.html', genreList = res, form=form)


### SEARCH FOR RECCOMMENDATONS ###
@app.route("/search")
def search():
    form = SearchForm()
    activity=request.args['selected_activity']
    print(activity)
    # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
    if activity=="FamilyNight":
        # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
        # s = select([movie]).where(title == 'Avatar')
        # result = db.session.execute(s)
        # print(result)
        res = db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                    genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                    where (((genre.genre='Adventure') or (genre.genre='Comedy') or (genre.genre='Animation') or (genre.genre='Mistery') or (genre.genre='Fantasy')) and ((movie.rated='PG13') or (movie.rated='PG')))\
                                    group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(), movie.rating limit 12;""")
        activity="Family Night"
    if activity=="DateNight":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  where ((genre.genre='Romance') or ((genre.genre='Animation')))\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(), movie.rating  limit 12;""")
        activity="Date Night"
    if activity=="GirlsNight":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  where ((genre.genre='Romance') or (genre.genre='Animation') or (genre.genre='Comedy'))\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(),movie.rating  limit 12;""")
        activity="Girls Night"
    if activity=="NerdNight":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  where ((genre.genre='Sci-Fi') or (genre.genre='Mistery'))\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(),movie.rating  limit 12;""")
        activity="Nerd Night"
    if activity=="GuysNight":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  where ((genre.genre='Comedy') and (movie.rated='R'))\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(),movie.rating  limit 12;""")
        activity="Guys Night"
    if activity=="CulturedNight":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  where ((genre.genre='Western') or (genre.genre='War'))\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(),movie.rating  limit 12;""")
        activity="Cultured Night"
    if activity=="SurpriseMe":
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from \
                                  genre join movie_genre on (genre.id=movie_genre.genre_id) join movie on (movie_genre.movie_id=movie.id)\
                                  group by movie.id, movie.title, movie.poster,movie.rated, movie.rating order by random(),movie.rating  limit 12;""")

        activity="Surprise Me"
    res = res.fetchall()
    return render_template('searchresults.html', movieList = res, activity=activity, form= form)

@app.route("/searchMovie")
def searchMovie():
    movie=request.args['movietitle']
    movie=movie.title()
    res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from movie where movie.title like'%%%s%%' order by random() limit 12;"""%movie)
    res=res.fetchall()
    return render_template('searchresults.html',movieList=res,activity=movie)

@app.route("/getMovieInfo/<id>")
def getMovieInfo(id):
    res = db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating, movie.description from movie where movie.id = %s"""%str(id))
    res = res.fetchall()
    genres = db.session.execute("""SELECT genre.genre from movie join movie_genre on (movie.id = movie_genre.movie_id) join genre on (movie_genre.genre_id = genre.id) where movie.id = %s;"""%str(id))
    genrelist = genres.fetchall()
    genrestring = ""
    for (genre,) in genrelist:
        genrestring += genre +",  "
    genrestring = genrestring[:-3]
    actors = db.session.execute("""SELECT actor.actor from actor join movie_actor on (actor.id = movie_actor.actor_id) WHERE movie_actor.movie_id = %s;"""%str(id))
    actorlist = actors.fetchall()
    actorstring = ""
    for (actor,) in actorlist:
        actorstring += actor+ ",  "
    actorstring = actorstring[:-3]
    return render_template('getmovieinfo.html', movie = res, genres = genrestring, actors = actorstring)

@app.route("/goodFor")
def goodFor():
    group=request.args['group']
    genre=request.args['genre']
    rating = ''
    if group == "Family":
        rating = 'PG-13'
    elif group == "Children":
        rating = 'PG'
    if rating != '':
        rating = "'"+rating+"'"
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from movie JOIN movie_genre ON (movie.id = movie_genre.movie_id) where movie_genre.genre_id = %s and movie.rated = %s  order by random() limit 12;"""%(genre, rating))
    else:
        res=db.session.execute("""SELECT movie.id, movie.title, movie.poster, movie.rated, movie.rating from movie JOIN movie_genre ON (movie.id = movie_genre.movie_id) where movie_genre.genre_id = %s order by random() limit 12;"""%genre)
    res=res.fetchall()
    return render_template('searchresults.html',movieList=res,activity="")

@app.route("/addMovie")
def addMovieToDb():
    movieName=request.args['movieTitleAdd']
    res=db.session.execute("""SELECT count(*) from movie where title='%s'"""%movieName)
    returnList=res.fetchall()
    res=db.session.execute("""SELECT actor from actor""")
    actorList=res.fetchall()
    writeTo=open("FINLIST.txt",'w')
    print(returnList)
    if returnList==[(0,)]:
        moviename = movieName.replace(" ", "+")
        res = req.get("http://www.omdbapi.com/?t={}".format(moviename))
        dataParsed = json.loads(res.text)
        print(moviename)
        if dataParsed['Response']!='False':
            # db.session.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster) VALUES (%s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"]))
            # db.session.commit()
            genresOfMovie = dataParsed["Genre"]
            genresOfMovie = genresOfMovie.split(", ")
            ## ADD ACTORS SUPPORT ##
            actorsOfMovie = dataParsed["Actors"]
            actorsOfMovie = actorsOfMovie.split(", ")
            for actor in actorsOfMovie:
                if actor not in actorList:
                    newactor = Actor(actor = actor)
                    db.session.add(newactor)
                    db.session.commit()
            # try:
            #     if dataParsed["Ratings"] != []:
            #         for source in dataParsed["Ratings"]:
            #             if source["Source"] == "Rotten Tomatoes":
            #                 rating = int(source["Value"][:len(source['Value'])-1])
            #     print(rating)
            #     newmovie = Movie(title = dataParsed["Title"], description = dataParsed["Plot"], year = dataParsed["Year"], rated = dataParsed["Rated"], runtime = dataParsed["Runtime"], poster = dataParsed["Poster"], rating=rating, genres = [g for g in genresOfMovie], actors = [a for a in actorsOfMovie])
            #     print("Added: ", dataParsed["Title"])
            #     db.session.add(newmovie)
            #     db.session.commit()
            # except:
            #     print("Failed to add "+dataParsed["Title"]+". Sigh-Oh well! Moving on!")
            if dataParsed["Ratings"] != []:
                rating=0
                for source in dataParsed["Ratings"]:
                    if source["Source"] == "Rotten Tomatoes":
                        rating = int(source["Value"][:len(source['Value'])-1])
            print(rating)
            print([g for g in genresOfMovie])
            print([a for a in actorsOfMovie])
            newmovie = Movie(title = dataParsed["Title"], description = dataParsed["Plot"], year = dataParsed["Year"], rated = dataParsed["Rated"], runtime = dataParsed["Runtime"], poster = dataParsed["Poster"], rating=rating, genres = [g for g in genresOfMovie], actors = [a for a in actorsOfMovie])
            print("Added: ", dataParsed["Title"])
            db.session.add(newmovie)
            db.session.commit()
            writeTo.write(dataParsed['Title'])
        writeTo.close()
    return render_template('dataAdded.html',movie=movieName)

@app.route("/about")
def getAbout():
    return render_template("about.html")

@app.route("/api", methods=["GET"])
def apiMainPage():
    return render_template('api.html')

@app.route("/api/v1/getMovieInfo", methods=["GET"])
def apiMovie():
    res = db.session.execute("""SELECT * from movie;""")
    movielist = res.fetchall()
    res = Response(dumps(movielist))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type'] = 'application/json'
    return res


@app.route("/api/v1/getMovieInfo/<movie>", methods=["GET"])
def apiMovieName(movie):
    movieName = movie.replace("+"," ")
    movieName = movieName.replace("%20", " ")
    res = db.session.execute("""SELECT * from movie where title like'%%%s%%';"""%movieName)
    movielist = res.fetchall()
    res = Response(dumps(movielist))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type'] = 'application/json'
    return res

@app.route("/api/v2/getGenreInfo/<movie>", methods=["GET"])
def apiGenreInfo(movie):
    movieName = movie.replace("+"," ")
    movieName = movieName.replace("%20", " ")
    res = db.session.execute("""SELECT movie.title, genre.genre from movie join movie_genre on (movie.id = movie_genre.movie_id) join genre on (movie_genre.genre_id = genre.id) where movie.title like '%%%s%%';"""%movieName)
    movielist = res.fetchall()
    res = Response(dumps(movielist))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type'] = 'application/json'
    return res

@app.route("/api/v3/getActorInfo/<actor>", methods=["GET"])
def apiActorInfo(actor):
    actorName = actor.replace("+"," ")
    actor = actorName.replace("%20", " ")
    res = db.session.execute("""SELECT title from movie join movie_actor ON (movie.id = movie_actor.movie_id) join actor on (movie_actor.actor_id = actor.id) where actor.actor = %s;"""%actor)
    actorlist = res.fetchall()
    res = Response(dumps(actorlist))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type'] = 'application/json'
    return res

if __name__=='__main__':
    app.run(debug=True)

# from flask.ext.sqlalchemy import SQLAlchemy
# import json
# from json import load
# import os
# from bs4 import BeautifulSoup
# import urllib.parse
# import requests as req
# from flask import Flask, render_template, request
# from flask_wtf import Form
# from flask_sqlalchemy import SQLAlchemy
# from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
# from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy.sql import select
# import init
# import psycopg2
# from flask import Flask, render_template, request
# import os
# import urllib.parse
# import json
#
# urllib.parse.uses_netloc.append("postgres")
# url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
# conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
#
#
# app = Flask(__name__)
#
# ### WELCOME ###
# @app.route("/")
# def index():
#     cur = conn.cursor()
#     # cur.execute("""SELECT id, title, description, year, rated, runtime from movies where title = 'Avatar';""")
#     # cur.execute("""SELECT id, title, poster, rated FROM movies where title = 'Avatar';""")
#     cur.execute("""SELECT * from genres;""")
#     genreList = cur.fetchall()
#     # cur.execute("""SELECT * from services;""")
#     # serviceList=cur.fetchall()
#     cur.execute("""SELECT * from activities;""")
#     activityList=cur.fetchall()
#     return render_template('welcome.html', genreList = genreList,activityList=activityList)
#
# # @app.route("/activitysearch")
# # def activity():
# #     return render_template('searchresults.html', movieList = res)
#
# ### SEARCH FOR RECCOMMENDATONS ###
# @app.route("/search")
# def search():
#     cur = conn.cursor()
#     activity=request.args['selected_activity']
#     goodfor=request.args['group']
#     genre=request.args['genre']
#     starring=request.args['actor']
#     # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
#     if activity!="":
#         # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
#         cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
#     res = cur.fetchall()
#     return render_template('searchresults.html', movieList = res)
#
# ### SEARCH FOR KNOWN MOVIE ###
# @app.route("/searchMovie")
# def searchMovie():
#     args = request.url.split('?')[1]
#     title = args.split("=")[1]
#     title = title.title()
#     title = title.replace("+", " ")
#     cur = conn.cursor()
#     cur.execute("""SELECT id, title, poster, rated FROM movies where title like '%"""+title+"""%' LIMIT 5;""")
#     res = cur.fetchall()
#     return render_template('searchresults.html', movieList = res)
#
# ### SHOW MOVIE INFORMATION ###
# @app.route("/movieInfo/<id>")
# def showMovieInfo(id):
#     cur = conn.cursor()
#     cur.execute("""SELECT id, title, poster, rated FROM movies where id = %s""", (str(id),))
#     res = cur.fetchall()
#     return render_template('getmovieinfo.html', movieInformation = res)
#
#
