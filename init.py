#heroku run python3 init.py
import psycopg2
from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import urllib.parse
import requests as req
import json

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
db = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

conn = db
#################### CREATE TABLES / KNUTH ####################
cur = conn.cursor()
cur.execute("DROP table movies CASCADE; DROP table genres CASCADE; DROP table genres_movies CASCADE;")
print("TABLES DELETED")
cur.execute("CREATE table movies (id serial unique, title varchar(100), description text); CREATE table genres (id serial unique, name varchar(20)); CREATE table genres_movies (movieid int, genreid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (genreid) references genres(id), primary key (movieid, genreid));")
print("TABLES CREATED")
conn.commit()
t = req.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
print("LIST SCRAPED FROM SOURCE")
soup=BeautifulSoup(t.text)
soup.prettify()
data=soup.find_all("td", { "class" : "csv_column_3" })
totalnumoffilms=0
genreList = []
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
        totalnumoffilms+=1
        cur.execute("""INSERT INTO movies (title, description) VALUES (%s, %s);""", (dataParsed["Title"],dataParsed["Plot"]))

        print(dataParsed["Title"])
        genres = dataParsed["Genre"]
        genres = genres.split(", ")
        for genre in genres:
            if genre not in genreList:
                cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
                genreList.append(genre)
            # TODO: ASK ABOUT USING RETURNING IN SQL TO GET THE MOVIEID
            cur.execute("""INSERT INTO genres_movies (movieid, genreid) VALUES (%s,(SELECT id FROM genres WHERE name = %s))""", (str(totalnumoffilms), genre))
    conn.commit()

print("TABLE POPULATED")
print("===============================INFO===============================")
print("All Genres:", genreList)
print("Total Num of Films:", totalnumoffilms-1)


#NOTE: SOME FYI INFO:
# ALL GENRES: ['Mystery', 'Romance', 'Thriller', 'Adventure', 'Sci-Fi', 'Comedy', 'Drama', 'Short', 'Crime', 'Western', 'War', 'History', 'Biography', 'Documentary', 'Music', 'Sport', 'Horror', 'Film-Noir', 'Fantasy', 'Action', 'Family', 'Animation', 'Musical', 'N/A']
# 932 MOVIES COMPILE CORRECTLY / ASSOCIATE WITH THE API
