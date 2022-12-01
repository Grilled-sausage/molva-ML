import requests
import json
import pandas as pd


for i in range(1,11) :
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=383db8629ed31d128685490012d6539b&curPage={0}&itemPerPage=100'.format(i)
    res = requests.get(url)
    text= res.text
    d = json.loads(text)
    
    movie_list = []
    list = []
    for b in d['movieListResult']['movieList']:
        movie_list.append([b['movieCd'],b['movieNm'],b['movieNmEn'],b['prdtYear'],b['repNationNm'],b['repGenreNm'],b['genreAlt']])
    data = pd.DataFrame(movie_list)
    data.columns = ['movieCd','movieNm','movieNmEn','prdtYear','repNationNm','repGenreNm','genreAlt']
    for j in range(0,100):
        if '성인물(에로)' in data['genreAlt'][j]:
            list.append(j)
    data.drop(list, inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    index_length = len(data.index)
    showTm_list = []
    for k in range(0, index_length) :
        detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=383db8629ed31d128685490012d6539b&movieCd={0}'.format(data['movieCd'][k])
        detail_res = requests.get(detail_url)
        
        detail_text = detail_res.text
        detail_d = json.loads(detail_text)
        showTm_list.append(detail_d['movieInfoResult']['movieInfo']['showTm'])
    data['showTm']=showTm_list
 
    data.to_csv("movie_list.txt", mode='a', encoding='utf-8', index=False, header = None)
