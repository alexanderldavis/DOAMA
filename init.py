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
#################### DELETE AND CREATE TABLES / HEROKU ####################
cur = conn.cursor()

# DROP ALL TABLES, CREATE ALL TABLES
cur.execute("""drop table if exists activities_movies; drop table if exists services_movies;drop table if exists genres_movies; drop table if exists actors_movies;""")
print("TABLES DELETED")
cur.execute("""drop table if exists movies; CREATE table movies (id serial unique, title varchar(100), description text, year varchar(40), rated varchar(50), runtime varchar(50), poster varchar(200), rating int);""")
cur.execute("""drop table if exists genres; CREATE table genres (id serial unique, name varchar(20)); CREATE table genres_movies (movieid int, genreid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (genreid) references genres(id), primary key (movieid, genreid));""")
cur.execute("""drop table if exists actors; CREATE table actors (id serial unique, name varchar(99)); CREATE table actors_movies (movieid int, actorid int, FOREIGN KEY (movieid) references movies(id), FOREIGN KEY (actorid) references actors(id), primary key (movieid, actorid));""")
cur.execute("""drop table if exists services; CREATE table services (id serial unique, name text);""")
cur.execute("""drop table if exists activities; CREATE table activities (id serial unique, name text);""")
cur.execute(""" CREATE table services_movies (movie_id int, FOREIGN key(movie_id) references movies(id), service_id int, FOREIGN key(service_id) references services(id));""")
cur.execute("""CREATE table activities_movies (movie_id int, FOREIGN key (movie_id) references movies(id), activity_id int, FOREIGN key(activity_id) references activities(id));""")
print("TABLES CREATED")
conn.commit()

# POPULATE TABLE services
watchingOptions=['netflix_instant','amazon_prime_instant_video','hulu_movies','crackle','youtube_free','epix','streampix','snagfilms','fandor_streaming','amazon_video_rental','apple_itunes_rental','android_rental','vudu_rental','youtube_rental','sony_rental','vimeo_vod_rental','amazon_video_purchase','apple_itunes_purchase','android_purchase','vudu_purchase','xbox_purchase','sony_purchase','vimeo_vod_purchase','amazon_dvd','amazon_bluray','netflix_dvd','redbox','hbo','showtime','cinemax','starz','encore','xfinity_free']
for option in watchingOptions:
    cur.execute("""INSERT INTO services(name) VALUES (%s);""",(option,))

# POPULATE TABLE activities
activityList=['Family night','Girls night','Date night','Nerd night','Guys party','Cultured movie night','Surprise me']
for activity in activityList:
    cur.execute("""INSERT into activities(name) VALUES (%s);""",(activity,))

file = """
Captain America: Civil War
Rogue One
The Jungle Book
Batman v Superman: Dawn of Justice
Fantastic Beasts and Where to Find Them
Deadpool
Suicide Squad
Doctor Strange
X-Men: Apocalypse
Warcraft
Jason Bourne
Independence Day: Resurgence
The Legend of Tarzan
Star Trek Beyond
Now You See Me 2
Passengers
Teenage Mutant Ninja Turtles: Out of the Shadows
Assassin's Creed
Ghostbusters
Inferno
Arrival
Allegiant
The Huntsman: Winter's War
The Magnificent Seven
Jack Reacher: Never Go Back
Gods of Egypt
Mechanic: Resurrection
The Shallows
The Purge: Election Year
Office Christmas Party
The 5th Wave
Ben-Hur
Train to Busan
Bad Santa 2
Morgan
Star Wars: Episode VII - The Force Awakens
Jurassic World
Furious 7
Avengers: Age of Ultron
Spectre
Mission: Impossible - Rogue Nation
The Hunger Games: Mockingjay - Part 2
The Martian
Ant-Man
San Andreas
Terminator Genisys
Kingsman: The Secret Service
Mad Max: Fury Road
Taken 3
Maze Runner: The Scorch Trials
Insurgent
Pixels
Ted 2
Tomorrowland
Jupiter Ascending
Creed
Fantastic Four
The Hateful Eight
Goosebumps
The Last Witch Hunter
Point Break
The Big Short
Seventh Son
Chappie
In the Heart of the Sea
Hitman: Agent 47
Ex Machina
Self/less
Scouts Guide to the Zombie Apocalypse
Knock Knock
Extinction
Transformers: Age of Extinction
The Hobbit: The Battle of the Five Armies
Guardians of the Galaxy
Maleficent
The Hunger Games: Mockingjay - Part 1
X-Men: Days of Future Past
Captain America: The Winter Soldier
The Amazing Spider-Man 2
Interstellar
Godzilla
Teenage Mutant Ninja Turtles
Lucy
Edge of Tomorrow
Noah
Night at the Museum: Secret of the Tomb
The Maze Runner
300: Rise of an Empire
Divergent
Exodus: Gods and Kings
Hercules
RoboCop
Non-Stop
Dracula Untold
Fury
The Expendables 3
Need for Speed
Dumb and Dumber To
Pompeii
The Purge: Anarchy
Transcendence
Snowpiercer
A Million Ways to Die in the West
John Wick
I, Frankenstein
The Giver
Iron Man 3
The Hobbit: The Desolation of Smaug
The Hunger Games: Catching Fire
Fast & Furious 6
Man of Steel
Thor: The Dark World
World War Z
Star Trek Into Darkness
The Wolverine
Pacific Rim
The Wolf of Wall Street
G.I. Joe: Retaliation
The Hangover Part III
Now You See Me
Oblivion
Elysium
The Lone Ranger
Grown Ups 2
After Earth
Hansel & Gretel: Witch Hunters
White House Down
Percy Jackson: Sea of Monsters
Olympus Has Fallen
RED 2
47 Ronin
Escape Plan
Last Vegas
Ender's Game
Warm Bodies
Evil Dead
The Purge
Carrie
Scary Movie 5
R.I.P.D.
The Call
The Family
Parker
Homefront
Grudge Match
The Incredible Burt Wonderstone
Machete Kills
Stand Up Guys
Redemption
The Avengers
Skyfall
The Dark Knight Rises
The Hobbit: An Unexpected Journey
The Twilight Saga: Breaking Dawn - Part 2
The Amazing Spider-Man
The Hunger Games
Men in Black 3
Life of Pi
Ted
Prometheus
Snow White and the Huntsman
Journey 2: The Mysterious Island
Battleship
Wrath of the Titans
The Expendables 2
John Carter
Dark Shadows
Resident Evil: Retribution
Jack Reacher
Total Recall
Underworld Awakening
Ghost Rider: Spirit of Vengeance
Cloud Atlas
Abraham Lincoln: Vampire Hunter
The Cabin in the Woods
Red Dawn
Safe
Dredd
Lockout
A Thousand Words
The Man with the Iron Fists
Solomon Kane
Piranha 3DD
Seeking Justice
Red Lights
The Grey
Django Unchained
The Watch
Taken 2
Iron Sky
Death Race: Inferno
Astérix and Obélix: God Save Britannia
Harry Potter and the Deathly Hallows: Part 2
Transformers: Dark of the Moon
Pirates of the Caribbean: On Stranger Tides
The Twilight Saga: Breaking Dawn - Part 1
Mission: Impossible - Ghost Protocol
Fast Five
The Hangover Part II
Rise of the Planet of the Apes
Thor
Captain America: The First Avenger
X-Men: First Class
Real Steel
Super 8
Green Lantern
Battle Los Angeles
Cowboys & Aliens
In Time
Limitless
Johnny English Reborn
Final Destination 5
Tower Heist
Source Code
Contagion
The Adjustment Bureau
Sanctum
Paul
Scream 4
The Rite
Season of the Witch
Sucker Punch
Red Riding Hood
Priest
The Darkest Hour
Killer Elite
The Mechanic
Conan the Barbarian
A Very Harold & Kumar 3D Christmas
Sherlock Holmes: A Game of Shadows
The Green Hornet
Drive Angry
The Thing
The Eagle
Trespass
Harry Potter and the Deathly Hallows: Part 1
The Twilight Saga: Eclipse
Iron Man 2
Clash of the Titans
TRON: Legacy
The Karate Kid
Prince of Persia: The Sands of Time
Resident Evil: Afterlife
Salt
The Tourist
The Expendables
Knight and Day
Percy Jackson & the Olympians: The Lightning Thief
The Sorcerer's Apprentice
RED
The A-Team
Unstoppable
The Book of Eli
The Wolfman
Predators
Piranha 3D
Legion
Hot Tub Time Machine
The Crazies
Daybreakers
Machete
Splice
Saw 3D: The Final Chapter
A Nightmare on Elm Street
Undisputed 3: Redemption
Inception
Shutter Island
Stone
Death Race 2
The Experiment
Grown Ups
Avatar
Harry Potter and the Half-Blood Prince
Transformers: Revenge of the Fallen
2012
The Twilight Saga: New Moon
Angels & Demons
The Hangover
Night at the Museum: Battle of the Smithsonian
Star Trek
X-Men Origins: Wolverine
Terminator Salvation
Fast & Furious
Inglourious Basterds
G.I. Joe: The Rise of Cobra
The Final Destination
Watchmen
The Taking of Pelham 123
Surrogates
Race to Witch Mountain
Zombieland
Friday the 13th
Underworld: Rise of the Lycans
Ninja Assassin
Halloween II
Cirque du Freak: The Vampire's Assistant
Crank: High Voltage
The Box
Jennifer's Body
Armored
Outlander
The Tournament
Saw VI
Sherlock Holmes
Bad Lieutenant: Port of Call New Orleans
Knowing
Exam
Taken
The Dark Knight
Indiana Jones and the Kingdom of the Crystal Skull
Hancock
Quantum of Solace
Iron Man
The Mummy: Tomb of the Dragon Emperor
Twilight
Wanted
The Incredible Hulk
Journey to the Center of the Earth
The Day the Earth Stood Still
Jumper
Tropic Thunder
The Happening
The Forbidden Kingdom
Rambo
Transporter 3
Death Race
Babylon A.D.
Superhero Movie
The X Files: I Want to Believe
The Bank Job
Meet Dave
Harold & Kumar Escape from Guantanamo Bay
Doomsday
21
Hellboy II: The Golden Army
Saw V
Yes Man
Righteous Kill
The Eye
Punisher: War Zone
Asterix at the Olympic Games
Pirates of the Caribbean: At World's End
Harry Potter and the Order of the Phoenix
Spider-Man 3
Transformers
I Am Legend
National Treasure: Book of Secrets
300
Live Free or Die Hard
Ocean's Thirteen
Fantastic Four: Rise of the Silver Surfer
Mr. Bean's Holiday
Ghost Rider
Evan Almighty
Resident Evil: Extinction
1408
Aliens vs. Predator: Requiem
Hannibal Rising
Halloween
30 Days of Night
Mr. Magorium's Wonder Emporium
28 Weeks Later
The Reaping
The Mist
War
The Invasion
The Hills Have Eyes II
Shoot 'Em Up
DOA: Dead or Alive
Planet Terror
Saw IV
Hostel: Part II
Next
The Bourne Ultimatum
The Bucket List
Pirates of the Caribbean: Dead Man's Chest
The Da Vinci Code
Casino Royale
Night at the Museum
X-Men: The Last Stand
Mission: Impossible III
Superman Returns
Click
Poseidon
Scary Movie 4
The Fast and the Furious: Tokyo Drift
Rocky Balboa
V for Vendetta
The Omen
Final Destination 3
Underworld: Evolution
Children of Men
Fearless
Snakes on a Plane
Crank
Thank You for Smoking
The Covenant
Ultraviolet
Slither
Saw III
The Prestige
Hostel
Undisputed 2: Last Man Standing
Miami Vice
World Trade Center
Lucky Number Slevin
Harry Potter and the Goblet of Fire
Star Wars: Episode III - Revenge of the Sith
War of the Worlds
King Kong
Mr. & Mrs. Smith
Batman Begins
Fantastic Four
Constantine
Kingdom of Heaven
The 40-Year-Old Virgin
The Island
Kung Fu Hustle
Transporter 2
Lord of War
Elektra
Æon Flux
Unleashed
Land of the Dead
Two for the Money
Domino
Saw II
Chaos
The Weather Man
London
Revolver
Stealth
Jarhead
Harry Potter and the Prisoner of Azkaban
Spider-Man
The Passion of the Christ
The Day After Tomorrow
Troy
Ocean's Twelve
National Treasure
I, Robot
Van Helsing
The Terminal
Hero
AVP: Alien vs. Predator
Alexander
Kill Bill: Vol. 2
Resident Evil: Apocalypse
Mean Girls
Blade: Trinity
The Forgotten
Saw
Dawn of the Dead
The Stepford Wives
Hellboy
Secret Window
House of Flying Daggers
Catwoman
Around the World in 80 Days
Anacondas: The Hunt for the Blood Orchid
Taxi
Taking Lives
Sky Captain and the World of Tomorrow
Cellular
The Punisher
Godsend
Shaun of the Dead
Harold & Kumar Go to White Castle
Envy
Collateral
Million Dollar Baby
The Bourne Supremacy
The Lord of the Rings: The Return of the King
The Matrix Reloaded
Pirates of the Caribbean: The Curse of the Black Pearl
Bruce Almighty
Terminator 3: Rise of the Machines
The Matrix Revolutions
X-Men 2
Hulk
2 Fast 2 Furious
Scary Movie 3
Master and Commander: The Far Side of the World
S.W.A.T.
The Haunted Mansion
Kill Bill: Vol. 1
The League of Extraordinary Gentlemen
Daredevil
The Italian Job
Johnny English
Lara Croft Tomb Raider: The Cradle of Life
Gothika
Freddy vs. Jason
The Recruit
Underworld
Final Destination 2
Identity
28 Days Later...
Bad Santa
Dreamcatcher
The A-Team
Unstoppable
The Book of Eli
The Wolfman
Predators
Piranha 3D
Legion
Hot Tub Time Machine
The Crazies
Daybreakers
Machete
Splice
Saw 3D: The Final Chapter
A Nightmare on Elm Street
Undisputed 3: Redemption
Inception
Shutter Island
Stone
Death Race 2
The Experiment
Grown Ups
Avatar
Harry Potter and the Half-Blood Prince
Transformers: Revenge of the Fallen
2012
The Twilight Saga: New Moon
Angels & Demons
The Hangover
Night at the Museum: Battle of the Smithsonian
Star Trek
X-Men Origins: Wolverine
Terminator Salvation
Fast & Furious
Inglourious Basterds
G.I. Joe: The Rise of Cobra
The Final Destination
Watchmen
The Taking of Pelham 123
Surrogates
Race to Witch Mountain
Zombieland
Friday the 13th
Underworld: Rise of the Lycans
Ninja Assassin
Halloween II
Cirque du Freak: The Vampire's Assistant
Crank: High Voltage
The Box
Jennifer's Body
Armored
Outlander
The Tournament
Saw VI
Sherlock Holmes
Bad Lieutenant: Port of Call New Orleans
Knowing
Exam
Taken
The Dark Knight
Indiana Jones and the Kingdom of the Crystal Skull
Hancock
Quantum of Solace
Iron Man
The Mummy: Tomb of the Dragon Emperor
Twilight
Wanted
The Incredible Hulk
Journey to the Center of the Earth
The Day the Earth Stood Still
Jumper
Tropic Thunder
The Happening
The Forbidden Kingdom
Rambo
Transporter 3
Death Race
Babylon A.D.
Superhero Movie
The X Files: I Want to Believe
The Bank Job
Meet Dave
Harold & Kumar Escape from Guantanamo Bay
Doomsday
21
Hellboy II: The Golden Army
Saw V
Yes Man
Righteous Kill
The Eye
Punisher: War Zone
Asterix at the Olympic Games
Pirates of the Caribbean: At World's End
Harry Potter and the Order of the Phoenix
Spider-Man 3
Transformers
I Am Legend
National Treasure: Book of Secrets
300
Live Free or Die Hard
Ocean's Thirteen
Fantastic Four: Rise of the Silver Surfer
Mr. Bean's Holiday
Ghost Rider
Evan Almighty
Resident Evil: Extinction
1408
Aliens vs. Predator: Requiem
Hannibal Rising
Halloween
30 Days of Night
Mr. Magorium's Wonder Emporium
28 Weeks Later
The Reaping
The Mist
War
The Invasion
The Hills Have Eyes II
Shoot 'Em Up
DOA: Dead or Alive
Planet Terror
Saw IV
Hostel: Part II
Next
The Bourne Ultimatum
The Bucket List
Pirates of the Caribbean: Dead Man's Chest
The Da Vinci Code
Casino Royale
Night at the Museum
X-Men: The Last Stand
Mission: Impossible III
Superman Returns
Click
Poseidon
Scary Movie 4
The Fast and the Furious: Tokyo Drift
Rocky Balboa
V for Vendetta
The Omen
Final Destination 3
Underworld: Evolution
Children of Men
Fearless
Snakes on a Plane
Crank
Thank You for Smoking
The Covenant
Ultraviolet
Slither
Saw III
The Prestige
Hostel
Undisputed 2: Last Man Standing
Miami Vice
World Trade Center
Lucky Number Slevin
Harry Potter and the Goblet of Fire
Star Wars: Episode III - Revenge of the Sith
War of the Worlds
King Kong
Mr. & Mrs. Smith
Batman Begins
Fantastic Four
Constantine
Kingdom of Heaven
The 40-Year-Old Virgin
The Island
Kung Fu Hustle
Transporter 2
Lord of War
Elektra
Æon Flux
Unleashed
Land of the Dead
Two for the Money
Domino
Saw II
Chaos
The Weather Man
London
Revolver
Stealth
Jarhead
Harry Potter and the Prisoner of Azkaban
Spider-Man
The Passion of the Christ
The Day After Tomorrow
Troy
Ocean's Twelve
National Treasure
I, Robot
Van Helsing
The Terminal
Hero
AVP: Alien vs. Predator
Alexander
Kill Bill: Vol. 2
Resident Evil: Apocalypse
Mean Girls
Blade: Trinity
The Forgotten
Saw
Dawn of the Dead
The Stepford Wives
Hellboy
Secret Window
House of Flying Daggers
Catwoman
Around the World in 80 Days
Anacondas: The Hunt for the Blood Orchid
Taxi
Taking Lives
Sky Captain and the World of Tomorrow
Cellular
The Punisher
Godsend
Shaun of the Dead
Harold & Kumar Go to White Castle
Envy
Collateral
Million Dollar Baby
The Bourne Supremacy
The Lord of the Rings: The Return of the King
The Matrix Reloaded
Pirates of the Caribbean: The Curse of the Black Pearl
Bruce Almighty
Terminator 3: Rise of the Machines
The Matrix Revolutions
X-Men 2
Hulk
2 Fast 2 Furious
Scary Movie 3
Master and Commander: The Far Side of the World
S.W.A.T.
The Haunted Mansion
Kill Bill: Vol. 1
The League of Extraordinary Gentlemen
Daredevil
The Italian Job
Johnny English
Lara Croft Tomb Raider: The Cradle of Life
Gothika
Freddy vs. Jason
The Recruit
Underworld
Final Destination 2
Identity
28 Days Later...
Bad Santa
Dreamcatcher
Happy Feet
"""
data = file.readlines()
genreList = []
actorList = []
totalnumoffilms=0
for i in range(1, len(data)):
    movieName = data[i].replace("\n","")
    movieName = movieName.replace(" ", "+")
    res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
    dataParsed = json.loads(res.text)

    if dataParsed["Response"] != "False":
        rated = dataParsed["Rated"]
        cur.execute("""INSERT INTO movies (title, description, year, rated, runtime, poster, rating) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (dataParsed["Title"],dataParsed["Plot"],dataParsed["Year"],dataParsed["Rated"], dataParsed["Runtime"],dataParsed["Poster"],rating))
        print("Added: ", dataParsed["Title"])

        genres = dataParsed["Genre"]
        genres = genres.split(", ")
        for genre in genres:
            if genre not in genreList:
                cur.execute("""INSERT INTO genres (name) VALUES (%s)""", (genre,))
                genreList.append(genre)
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
