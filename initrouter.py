import psycopg2
import json
from json import load
import os
from bs4 import BeautifulSoup
import urllib.parse
import requests as req
from flask import Flask, render_template, request
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import select

Base = declarative_base()

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
app = Flask(__name__)
sqldb = SQLAlchemy(app)
app.secret_key = 'wtforms more like wtf forms'

movie_genre=Table('movie_genre',Base.metadata,Column('movie_id',Integer,ForeignKey('movie.id')),Column('genre_id',Integer,ForeignKey('genre.id')))

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
    genres=relationship("Genre",
                            secondary=movie_genre,
                            back_populates="inMovie")

    def __repr__(self):
        return "Movie: ({})".format(self.title)

class Genre(Base):
    __tablename__="genre"
    id=Column(Integer,primary_key=True)
    genre=Column(String)
    inMovie=relationship("Movie", secondary=movie_genre, back_populates="genres")

    def __repr__(self):
        return "Genre({})".format(self.genre)

# engine = create_engine(os.environ["DATABASE_URL"])
# Session = sessionmaker(bind=engine)
# db = Session()
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

t = req.get('https://raw.githubusercontent.com/alexanderldavis/DOAMA/master/finalMovieList.txt')
print("LIST SCRAPED FROM SOURCE")


data = t.text
movies = data.split("\n")
genreList = []
allGenres = {}
for movie in movies:
    moviename = movie.title()
    movieName = moviename.replace(" ", "+")
    res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
    dataParsed = json.loads(res.text)
    if dataParsed["Response"] != "False":
        genresOfMovie = dataParsed["Genre"]
        genresOfMovie = genresOfMovie.split(", ")
        for genre in genresOfMovie:
            if genre not in genreList:
                newgenre = Genre(genre = genre)
                db.add(newgenre)
                genreList.append(genre)
                allGenres[genre] = newgenre
        try:
            if dataParsed["Ratings"] != []:
                for source in dataParsed["Ratings"]:
                    if source["Source"] == "Rotten Tomatoes":
                        rating = int(source["Value"][:len(source['Value'])-1])
            newmovie = Movie(title = dataParsed["Title"], description = dataParsed["Plot"], year = dataParsed["Year"], rated = dataParsed["Rated"], runtime = dataParsed["Runtime"], poster = dataParsed["Poster"], rating=rating, genres = [allGenres[g] for g in genresOfMovie])
            print("Added: ", dataParsed["Title"])
            db.add(newmovie)
        except:
            print("Failed to add "+dataParsed["Title"]+". Sigh-Oh well! Moving on!")

    db.commit()

class SearchForm(Form):
    options = SelectField('Search By:', [validators.Required()], choices=[('FamilyNight', 'Family Night'), ('DateNight', 'Date Night'),('GirlsNight', 'Girls Night'),('GuysNight', 'Guys Night'), ('NerdNight', 'Nerd Night'), ('CulturedNight', 'Cultured Movie Night'), ('SurpriseMe', 'Surprise Me')])

@app.route("/", methods=['GET'])
def index():
    form = SearchForm()
    return render_template('welcome.html', form=form)


### SEARCH FOR RECCOMMENDATONS ###
@app.route("/search")
def search():
    cur = db.cursor()
    activity=request.args['selected_activity']
    print(activity)
    # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
    if activity!="":
        # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
        # s = select([movie]).where(title == 'Avatar')
        # result = db.execute(s)
        # print(result)
        cur.execute("""SELECT id, title, poster, rated from movie where title = 'Avatar';""")
    res = cur.fetchall()
    return render_template('searchresults.html', movieList = res)
