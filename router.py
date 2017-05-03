import psycopg2
from flask import Flask, render_template, request
import os
import urllib.parse
import json

app = Flask(__name__)

@app.route("/")
def index():
    res = []
    return render_template('welcome.html', courseList = res, title="Top 5 Gened-Fulfilling Courses")

if __name__=='__main__':
    app.run(debug=True)
