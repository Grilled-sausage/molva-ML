import requests
import json
import pandas as pd
import csv
from tmdbv3api import TMDb, Search, Movie, Person

df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\people_list.txt',sep=",",header=None, encoding = 'utf8')
people_df = df[1]
peopleNm_df = df[0]
nmEn_list = []
name_list = []
for i in range(1, len(people_df)):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?key=f995f4c53a9a1020a41785f09dca57db&&itemPerPage=30&peopleCd={0}'.format(people_df[i])
    res = requests.get(url)
    text= res.text
    
    d = json.loads(text)
    if not d['peopleInfoResult']['peopleInfo']['peopleNmEn']:
        nmEn_list.append(' ')
        name_list.append(peopleNm_df[i])
        continue
    nmEn_list.append(d['peopleInfoResult']['peopleInfo']['peopleNmEn'])
    name_list.append(peopleNm_df[i])
name_df = pd.DataFrame(nmEn_list)
name_df.columns = ['peopleNmEn']
name_df['people'] = name_list
name_df.to_csv("peopleNmEn_list.txt", mode='a', encoding='utf8', index=False, header=None)
