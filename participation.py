import requests
import json
import pandas as pd

participation_df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\participation_base.txt',sep=",",header=None)
participation_df.columns = ['movieCd','movieNm','people']

peopleCd_list = []
movieCd_list = []
movieNm_list = []
people_list = []
repRoleNm_list = []
for i in range(1, len(participation_df['people'])):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=eb596579415986f67019703308e115bf&&itemPerPage=30&peopleNm={0}'.format(participation_df['people'][i])
    res = requests.get(url)
    text= res.text
    
    d = json.loads(text)
    
    for j in d['peopleListResult']['peopleList']:
        if(j['filmoNames'] == None) :
            continue
        if (j['repRoleNm'] == '배우' or j['repRoleNm'] == '감독' or j['repRoleNm'] == '촬영') and participation_df['movieNm'][i] in j['filmoNames']:
            peopleCd_list.append(j['peopleCd'])
            repRoleNm_list.append(j['repRoleNm'])
            movieCd_list.append(participation_df['movieCd'][i])
            movieNm_list.append(participation_df['movieNm'][i])
            people_list.append(participation_df['people'][i])
            print(participation_df['people'][i])
people_df = pd.DataFrame({'movieCd' : movieCd_list,'movieNm' : movieNm_list,'people' : people_list})
people_df['peopleCd'] = peopleCd_list
people_df['repRoleNm'] = repRoleNm_list
people_df.to_csv("participation.txt", mode='a', encoding='utf-8', index=False, header=None)
