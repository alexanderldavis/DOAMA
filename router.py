import psycopg2
from flask import Flask, render_template, request
import os
import urllib.parse
import json

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)


app = Flask(__name__)

@app.route("/")
def index():
    cur = conn.cursor()
    # cur.execute("""SELECT id, title, description, year, rated, runtime from movies where title = 'Avatar';""")
    # cur.execute("""SELECT id, title, poster, rated FROM movies where title = 'Avatar';""")
    cur.execute("""SELECT * from genres;""")
    genreList = cur.fetchall()
    cur.execute("""SELECT * from services;""")
    serviceList=cur.fetchall()
    return render_template('welcome.html', genreList = genreList,serviceList=serviceList)

@app.route("/search")
def search():
    cur = conn.cursor()
    cur.execute("""SELECT id, title, poster, rated from movies where title = 'Avatar'""")
    res = cur.fetchall()
    return render_template('searchresults.html', movieList = res)

@app.route("/searchMovie")
def searchMovie():
    args = request.url.split('?')[1]
    title = args.split("=")[1]
    title = title.title()
    title = title.replace("+", " ")
    cur = conn.cursor()
    cur.execute("""SELECT id, title, poster, rated FROM movies where title like '%"""+title+"""%'""")
    res = cur.fetchall()
    return render_template('searchresults.html', movieList = res)

if __name__=='__main__':
    app.run(debug=True)
