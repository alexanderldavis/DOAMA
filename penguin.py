from bs4 import BeautifulSoup
import requests as req
import json

# t=requests.get('http://www.theyshootpictures.com/gf1000_a-b.htm')
t = req.get('http://www.theyshootpictures.com/gf1000_all1000films_table.php')
soup=BeautifulSoup(t.text)
soup.prettify()
file = open("text.casm", "w")
file.write(t.text)
data=soup.find_all("td", { "class" : "csv_column_3" })
dataDict={}
columns=data[0].get_text().split('\n')
for i in range(1,len(columns)-1):
    dataDict[columns[i]]=[]
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
    print(movieName)
    movieName = movieName.replace(" ", "+")
    res = req.get("http://www.omdbapi.com/?t={}".format(movieName))
    
    print(res.text)



    # x=data[i].find_all("td")
    # dataDict['Rank'].append(x[0].get_text())
    # dataDict['College'].append(x[1].get_text())
    # dataDict['Freshman class'].append(x[2].get_text())
    # dataDict['Pell grad share'].append(x[3].get_text())
    # dataDict['Net price, middle- income'].append(x[4].get_text())
    # dataDict['College Access Index'].append(x[5].get_text())
    # dataDict['Endowment per student'].append(x[6].get_text())
# collegeData=pd.DataFrame(dataDict)
# collegeData=collegeData[['Rank','College','Freshman class','Pell grad share','Net price, middle- income','College Access Index','Endowment per student']]
# print(collegeData)
