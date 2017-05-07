from bs4 import BeautifulSoup
import requests
document = open("finalMovieList.txt", "w")

page1 = requests.get("http://www.imdb.com/list/ls051503761/?start=1&view=compact&sort=listorian:asc&defaults=1&scb=0.1469641715527923") # where url is the above url
bsparse1 = BeautifulSoup(page1.text)

page2 = requests.get("http://www.imdb.com/list/ls051503761/?start=251&view=compact&sort=listorian:asc") # where url is the above url
bsparse2 = BeautifulSoup(page2.text)

page3 = requests.get("http://www.imdb.com/list/ls051503761/?start=501&view=compact&sort=listorian:asc") # where url is the above url
bsparse3 = BeautifulSoup(page2.text)

totalNumFilms = 0
for movie in bsparse1.findAll('td','title'):
    title = movie.find('a').contents[0]
    document.write(title+"\n")
    totalNumFilms += 1

for movie in bsparse2.findAll('td', 'title'):
    title = movie.find('a').contents[0]
    document.write(title+"\n")
    totalNumFilms += 1

for movie in bsparse3.findAll('td', 'title'):
    title = movie.find('a').contents[0]
    document.write(title+"\n")
    totalNumFilms += 1

print("LIST CREATION COMPLETE")
print("TOTAL NUM OF FILMS: ", totalNumFilms)
