import json
import requests as req

f=open('finalMovieList.txt','r')
lines=f.readlines()
movies=[x.strip("\n") for x in lines]
wf=open("movies_info.json",'w')
wf.write("[")
for i in range(0,len(movies)):
    res = req.get("http://www.omdbapi.com/?t={}".format(movies[i]))
    dataParsed = json.loads(res.text)
    wf.write(json.dumps(dataParsed))
    if i<len(movies)-1:
        wf.write(",")
wf.write("]")
wf.close()
