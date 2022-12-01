import requests
import json
import pandas as pd


for i in range(51,61) :
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=c721d3c3e72b7bbe39ae4e7e42012e1a&curPage={0}&itemPerPage=100'.format(i)
    res = requests.get(url)
    text= res.text
    d = json.loads(text)
    
    actor_list = []
    
    for b in d['peopleListResult']['peopleList']:
        actor_list.append([b['peopleCd'],b['peopleNm'],b['repRoleNm']])
    data = pd.DataFrame(actor_list)
    data.columns = ['peopleCd','peopleNm','repRoleNm']

    data.to_csv("actor_list.txt", mode='a', encoding='utf-8', index=False, header = None)
