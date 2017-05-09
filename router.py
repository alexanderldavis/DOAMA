import psycopg2
from flask import Flask, render_template, request
import os
import urllib.parse
import json

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)


app = Flask(__name__)

### WELCOME ###
@app.route("/")
def index():
    cur = conn.cursor()
    # cur.execute("""SELECT id, title, description, year, rated, runtime from movies where title = 'Avatar';""")
    # cur.execute("""SELECT id, title, poster, rated FROM movies where title = 'Avatar';""")
    cur.execute("""SELECT * from genres;""")
    genreList = cur.fetchall()
    # cur.execute("""SELECT * from services;""")
    # serviceList=cur.fetchall()
    cur.execute("""SELECT * from activities;""")
    activityList=cur.fetchall()
    return render_template('welcome.html', genreList = genreList,activityList=activityList)

# @app.route("/activitysearch")
# def activity():
#     return render_template('searchresults.html', movieList = res)

### SEARCH FOR RECCOMMENDATONS ###
@app.route("/search")
def search():
    cur = conn.cursor()
    activity=request.args['selected_activity']
    goodfor=request.args['group']
    genre=request.args['genre']
    starring=request.args['actor']
    # cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
    if activity!="":
        # cur.execute("""SELECT movies.id, movies.title, movies.poster, movies.rated, movies.rating from movies join activities_movies on (activities_movies.movie_id=movies.id) join activity on (activities_movies.activity_id=acitvities.id) WHERE activities.name='%s' limit 5;"""%activity)
        cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar';""")
    res = cur.fetchall()
    return render_template('searchresults.html', movieList = res)

### SEARCH FOR KNOWN MOVIE ###
@app.route("/searchMovie")
def searchMovie():
    args = request.url.split('?')[1]
    title = args.split("=")[1]
    title = title.title()
    title = title.replace("+", " ")
    cur = conn.cursor()
    cur.execute("""SELECT id, title, poster, rated FROM movies where title like '%"""+title+"""%' LIMIT 5;""")
    res = cur.fetchall()
    return render_template('searchresults.html', movieList = res)

### SHOW MOVIE INFORMATION ###
@app.route("/movieInfo/<id>")
def showMovieInfo(id):
    cur = conn.cursor()
    cur.execute("""SELECT id, title, poster, rated FROM movies where id = %s""", (str(id),))
    res = cur.fetchall()
    return render_template('getmovieinfo.html', movieInformation = res)


if __name__=='__main__':
    app.run(debug=True)
