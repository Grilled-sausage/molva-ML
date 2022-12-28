import requests
import json
import pandas as pd
import csv
from tmdbv3api import TMDb, Search, Movie

df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\movie_list.csv',sep=",",header=None, encoding = 'cp949')
movieNm_df = df[2]
prdfYear_df = df[3]
story_list = []
image_list = []

tmdb = TMDb()
movie = Movie()

tmdb.api_key = "1c0dba51059826fd4c1b56cdf90cad0b"
tmdb.language = 'ko'
search = Search()
for i in range(1, len(movieNm_df)):
    query = movieNm_df[i]
    year = prdfYear_df[i]
    results = search.movies({"query": query, "year": year})
    if not results:
        story_list.append(" ")
        image_list.append(" ")
    if results:    
        for result in results:
            story_list.append(result.overview)
            m = movie.details(result.id)
            image_list.append(m.poster_path)
            break

data = pd.DataFrame(story_list)
data.columns = ['story']
data['image']=image_list
data['image'] = 'https://image.tmdb.org/t/p/original' + data['image']
data.to_csv("story&image_list.txt", mode='w', encoding='utf8', index=False, header=None)
