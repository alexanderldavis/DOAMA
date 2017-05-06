#heroku run python3 init.py
import psycopg2
from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import urllib.parse
import requests as req
import json
from canistreamit import search, streaming, rental, purchase, dvd, xfinity

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

conn = db
#################### CREATE TABLES / KNUTH ####################
cur = conn.cursor()
cur.execute("DROP table movies CASCADE; DROP table genres CASCADE; DROP table genres_movies CASCADE; DROP table actors CASCADE; DROP table actors_movies CASCADE;")
print("TABLES DELETED")
cur.execute("""CREATE table movies (id serial unique, title varchar(100), description text, year varchar(40), rated varchar(50), runtime varchar(50), poster varchar(200));""")
cur.execute("""CREATE table genres (id serial unique, name varchar(20)); CREATE table genres_movies (movieid int, genreid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (genreid) references genres(id), primary key (movieid, genreid));""")
cur.execute("""CREATE table actors (id serial unique, name varchar(99)); CREATE table actors_movies (movieid int, actorid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (actorid) references actors(id), primary key (movieid, actorid));""")
cur.execute("""CREATE table services_movies (movie_id int, FOREIGN key(movie_id) references movies(id), service_id int, FOREIGN key(service_id) references services(id));""")
cur.execute("""CREATE table services (id serial unique, name text);""")
print("TABLES CREATED")
conn.commit()
watchingOptions=['netflix_instant','amazon_prime_instant_video','hulu_movies','crackle','youtube_free','epix','streampix','snagfilms','fandor_streaming','amazon_video_rental','apple_itunes_rental','android_rental','vudu_rental','youtube_rental','sony_rental','vimeo_vod_rental','amazon_video_purchase','apple_itunes_purchase','android_purchase','vudu_purchase','xbox_purchase','sony_purchase','vimeo_vod_purchase\
','amazon_dvd','amazon_bluray','netflix_dvd','redbox','hbo','showtime','cinemax','starz','encore','xfinity_free']
for option in watchingOptions:
    cur.execute("""INSERT INTO services(name) VALUES (%s);""",(option))
    print(option)
t = req.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
print("LIST SCRAPED FROM SOURCE")
soup=BeautifulSoup(t.text)
soup.prettify()
data=soup.find_all("td", { "class" : "csv_column_3" })
totalnumoffilms=0
genreList = []
actorList = []
for i in range(1,len(data)):
    movieName = data[i].get_text()
    finalString = ""
    if "," in movieName:
        s = movieName.split(", ")
        s.reverse()
        for i in s:
            finalString += i + " "
        movieName = finalString[:-1]
    if "' " in movieName:
        movieName = movieName.replace("' ", "'")
    movieName = movieName.replace(" ", "+")
    res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
    dataParsed = json.loads(res.text)
    if dataParsed["Response"] != "False":
        # search for availability in different gate
        movie=search(dataParsed['Title'])[0]
        streamingList=movie['_id'].keys()
        rentalList=movie['_id'].keys()
        purchaseList=movie['_id'].keys()
        dvdList=dvd(movie['_id'])
        cableList=xfinity(movie['_id'])
        for li in [streamingList,rentalList,purchaseList,dvdList,cableList]:
            if li!=[]:
                for key in li:
                    print(li[key])
                    # cur.execute("""INSERT INTO services(name) VALUES (%s);""",(li[key]))
                    cur.execute("""INSERT INTO services_movies(movie_id,service_id) VALUES ((select id from movies where title=%s),(select id from services where name=%s));""",(dataParsed['title'],li[key]))
        totalnumoffilms+=1
        if dataParsed["Poster"] != "N/A":
            cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster) VALUES (%s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"]))
        else:
            cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster) VALUES (%s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],"http://www.projectdoama.com/static/penguin.jpg"))
        print("Added: ",dataParsed["Title"])
        genres = dataParsed["Genre"]
        genres = genres.split(", ")
        for genre in genres:
            if genre not in genreList:
                cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
                genreList.append(genre)
            # TODO: ASK ABOUT USING RETURNING IN SQL TO GET THE MOVIEID
            cur.execute("""INSERT INTO genres_movies (movieid, genreid) VALUES (%s, (SELECT id FROM genres WHERE name = %s))""", (str(totalnumoffilms), genre))
        actors = dataParsed["Actors"]
        actors = actors.split(", ")
        for actor in actors:
            if actor not in actorList:
                cur.execute("""INSERT INTO actors (name) VALUES (%s)""", (actor,))
                actorList.append(actor)
            cur.execute("""INSERT INTO actors_movies (movieid, actorid) VALUES (%s, (SELECT id from actors WHERE name = %s))""", (str(totalnumoffilms), actor))
    conn.commit()

print("TABLE POPULATED")
print("===============================INFO===============================")
print("All Genres:", genreList)
print("Total Num of Films:", totalnumoffilms-1)


#NOTE: SOME FYI INFO:
# ALL GENRES: ['Mystery', 'Romance', 'Thriller', 'Adventure', 'Sci-Fi', 'Comedy', 'Drama', 'Short', 'Crime', 'Western', 'War', 'History', 'Biography', 'Documentary', 'Music', 'Sport', 'Horror', 'Film-Noir', 'Fantasy', 'Action', 'Family', 'Animation', 'Musical', 'N/A']
# 932 MOVIES COMPILE CORRECTLY / ASSOCIATE WITH THE API
