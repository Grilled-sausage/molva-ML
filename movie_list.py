import requests
import json
import pandas as pd

for i in range(1,7) :
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=c721d3c3e72b7bbe39ae4e7e42012e1a&curPage={0}&itemPerPage=100&openStartDt=2022&openEndDt=2022'.format(i)
    res = requests.get(url)
    text= res.text
    d = json.loads(text)
    
    movie_list = []
    delete_list = []
    
    for b in d['movieListResult']['movieList']:
        movie_list.append([b['movieCd'],b['movieNm'],b['movieNmEn'],b['prdtYear'],b['repNationNm'],b['repGenreNm'],b['genreAlt']])
    data = pd.DataFrame(movie_list)
    data.columns = ['movieCd','movieNm','movieNmEn','prdtYear','repNationNm','repGenreNm','genreAlt']
    
    for j in range(0,len(data.index)):
        if '성인물(에로)' in data['genreAlt'][j]:
            delete_list.append(j)
    data.drop(delete_list, inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    index_length = len(data.index)
    showTm_list = []
    actors_list = []
    directors_list = []
    people_list = []
    x = data['movieCd'][0]
    for k in range(0, index_length) :
        detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=c721d3c3e72b7bbe39ae4e7e42012e1a&movieCd={0}'.format(data['movieCd'][k])
        detail_res = requests.get(detail_url)
        
        detail_text = detail_res.text
        detail_d = json.loads(detail_text)
        
        showTm_list.append(detail_d['movieInfoResult']['movieInfo']['showTm'])

        for l in detail_d['movieInfoResult']['movieInfo']['actors']:
            actors_list.append(l['peopleNm'])
            
        for m in detail_d['movieInfoResult']['movieInfo']['directors']:
            directors_list.append(m['peopleNm'])
        
        people_list = actors_list + directors_list
        people_df = pd.DataFrame({'movieCd' : data['movieCd'][k],'movieNm' : data['movieNm'][k],'people' : people_list})
        if x == data['movieCd'][k] :
            tmp = people_df
        else:
            tmp = pd.concat([tmp,people_df])
        actors_list.clear()
        directors_list.clear()
        tmp.reset_index(drop=True, inplace=True)

    people_data = tmp
    tmp = data
    tmp['showTm']=showTm_list
    data.to_csv("movie_list.txt", mode='a', encoding='utf-8', index=False, header=None)
    people_data.to_csv("participation_base.txt", mode='a', encoding='utf-8', index=False, header=None)    

