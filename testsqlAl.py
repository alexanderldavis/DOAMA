from json import load
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Movie(Base):
    __tablename__='movie'
    id=Column(Integer,primary_key=True)
    title=Column(String)

    def __repr__(self):
        return "Movie: ({})".format(self.title)
engine=create_engine('postgresql://nguyli03:@localhost:2345')
Session = sessionmaker(bind=engine)
db = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

f=open('finalMovieList.txt','r')
lines=f.readlines()
movie_info=[x.strip("\n") for x in lines]

rset=set()

for movie in movie_info:
    newmovie=Movie(title=movie)
    db.add(newmovie)
db.commit()
