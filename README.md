# PROJECT DOAMA
Decide On A Movie Already

## INTRO
This project uses an API call from http://www.omdbapi.com/ to get information about movies in init.py, as well as information about movies when adding individual movies to a database. 

### Functionalities
The app allows users to search for movies and relevant information that are: (1) ideal for common movie-watching situations, (2) by genres, (3) or by specific movie title. The app also allows users to submit movie titles that are not in the database. If searching for a specific movie yields no results, or does not yield the movie that the user is looking for, a user is prompted with the opportunity to add it to the database.

##### Add movie test case
Visit http://www.projectdoama.com/searchMovie?movietitle=La+La+Land. Since La La Land is not in the database, you are provided a textfield and button populated with the search query. Simply press "Add Movie" and the movie will be added to the database, with its information retrieved from http://www.omdbapi.com/.

#### API
Information about the AJAX API provided by DOAMA can be found here: http://www.projectdoama.com/api. This API call returns JSON text about specific movies, genres, and actors, as well as provides the option to see the entire database of movie information.

#### Plugins
Bootstrap was used, as was SQLAlchemy, and WTForms to get this working properly on Heroku. Additionally, there are 5 controllers in router.py and there are more than three views in template form.

## SETUP INFO
This project uses three tables to contain movie, genre, and movie_genres information.

This is a visualization of the tables in the database:

### movies
id | title | description
--- | --- | ---
1 | Vertigo | "A San Francisco detective suffering from acrophobia investigates the strange activities of an old friend's wife, all the while becoming dangerously obsessed with her."
2 | 2001: A Space Odyssey | "Humanity finds a mysterious, obviously artificial object buried beneath the Lunar surface and, with the intelligent computer H.A.L. 9000, sets off on a quest."

↑
### genres_movies
movieid | genreid
--- | ---
1 | 1
1 | 2
1 | 3
2 | 4
2 | 5

↓
### genres
id | name
--- | ---
1 | Mystery
2 | Romance
3 | Thriller
4 | Adventure
5 | Sci-Fi



