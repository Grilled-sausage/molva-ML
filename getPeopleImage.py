import requests
import json
import pandas as pd
import csv
from tmdbv3api import TMDb, Search, Movie, Person

df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\peopleNmEn_list.txt',sep=",",header=None, encoding = 'utf8')
name_df = df[1]
enName_df = df[0]

image_list = []
tmdb = TMDb()
tmdb.api_key = "1c0dba51059826fd4c1b56cdf90cad0b"
tmdb.language = 'ko'
search = Search()

for i in range(1, len(name_df)):
    if enName_df[i]:
        query = enName_df[i]
    if len(enName_df[i]) == 1:
        query = name_df[i]
    
    
    results = search.people({"query": query})
    if not results:
        image_list.append(" ")
        print(name_df[i])

    a = 1
    for result in results:
        
        if(result.profile_path == None and len(results) == 1):
           image_list.append(" ")
           print(name_df[i])
           continue
        elif(result.profile_path == None and len(results) != a):
             a = a + 1
             continue
        elif(result.profile_path == None and len(results) == a):
            image_list.append(" ")
            print(name_df[i])

            continue
        
        image_list.append(result.profile_path)
        print(name_df[i])
        break
    
data = pd.DataFrame(image_list)
data.columns = ['image']
data['image'] = 'https://image.tmdb.org/t/p/original' + data['image']
data.to_csv("peopleimage_list.txt", mode='a', encoding='utf8', index=False, header=None)
