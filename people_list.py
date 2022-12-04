import requests
import json
import pandas as pd

part_df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\part_base.txt',sep=",",header=None)
part_df.columns = ['movieCd','movieNm','people']

peopleCd_list = []
for i in range(0, len(part_df['people'])):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=383db8629ed31d128685490012d6539b&&itemPerPage=30&peopleNm={0}'.format(part_df['people'][i])
    res = requests.get(url)
    text= res.text
    
    d = json.loads(text)
    
    for j in d['peopleListResult']['peopleList']:
        if (j['repRoleNm'] == '배우' or j['repRoleNm'] == '감독' or j['repRoleNm'] == '촬영') and part_df['movieNm'][i] in j['filmoNames']:
            peopleCd_list.append(j['peopleCd'])

part_df['peopleCd'] = peopleCd_list
part_df.to_csv("people_list.txt", mode='a', encoding='utf-8', index=False, header = None)
