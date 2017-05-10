import json
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests as req
Base=declarative_base()

movie_genre=Table('movie_genre',Base.metadata,Column('movie_id',Integer,ForeignKey('movie.id')),Column('genre_id',Integer,ForeignKey('genre.id')))

class Movie(Base):
    __tablename__='movie'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    rating=Column(Integer)
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

engine=create_engine('postgresql://nguyli03:@localhost:2345')
Session = sessionmaker(bind=engine)
db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with open('movies_info.json', 'r') as mf:
    movies = json.load(mf)

genreset=set()
genres={}
#get all the gened in the gened database
for movie in movies:
    if movie['Response']!="False":
        genreList=movie['Genre'].split(", ")
        for genre in genreList:
            genreset.add(genre)

for genre in genreset:
    newgenre=Genre(genre=genre)
    db.add(newgenre)
    genres[genre]=newgenre

for movie in movies:
    if movie['Response']!="False":
        genreList=movie['Genre'].split(", ")
        if movie['Ratings']!=[]:
            rating=0
            for source in movie['Ratings']:
                if source["Source"]=="Rotten Tomatoes":
                    rating=int(source['Value'][:len(source['Value'])-1])
        newmovie=Movie(title=movie['Title'], genres=[genres[g] for g in genreList], rating=rating)
        db.add(newmovie)

db.commit()
# try some query:
movie=db.query(Movie).filter_by(title='Happy Feet').all()
print(movie)
