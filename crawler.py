from bs4 import BeautifulSoup
import requests
import re

t=requests.get("http://www.theyshootpictures.com/gf1000_a-b.htm")
panda=BeautifulSoup(t.text,"lxml")
panda.prettify()
divs1=panda.find_all('div',{'class':"jwresp_col jwresp2_col1"})
for div in divs1:
    dic={}
    title=div.find('h3').find('span').contents[0]
    dic['title']=title
    director1=div.find('span',style=re.compile(r'font-size:24px'))
    director2=div.find('span',style=re.compile(r'font-size:22px'))
    if director1==None:
        director=director2.find('a').contents[0]
    else:
        director=director1.find('a').contents[0]
    dic['director']=director
    rankings=div.find_all('span',style=re.compile(r'font-size:18px'))
    for ranking in rankings:
        if ranking.find('a')!=None:
            ranking=ranking.find('a').contents[0]
            dic['ranking']=ranking
    text=div.find_all('div',{'class':'text_stack'})
    print(text[1])
    if text[1].find('strong')==None:
        text=text[3].contents[0]
        print(text)
    else:
        text=text[4].contents[0]
# movies=[]
# headers=panda.find_all('h3')
# spans=panda.find_all('span',style=re.compile(r'font-size:24px'))
# spans2=panda.find_all('span',style=re.compile(r'font-size:18px'))
# n=0
# for span in spans2:
#     a=span.find_all('a')
#     if a!=[]:
#         n=n+1
# print(n)
# for i in range(0,len(headers)-1):
#     title=headers[i].find_all('span')[0].contents[0]
#     # director=spans[i].contents[0]
#     dic={}
#     dic['title']=title
#     # dic['director']=director
#     movies.append(dic)
# print(len(movies))
# print(len(spans))
# # print(headers[1].find_all('span')[0].contents[0])
