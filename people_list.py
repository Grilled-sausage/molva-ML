import requests
import json
import pandas as pd

df = pd.read_csv(r'C:\Users\ehdwl\AppData\Local\Programs\Python\Python310\participation.txt',sep=",",header=None)
df.columns = ['movieCd','movieNm','people','peopleCd','repRoleNm']

people_df = df.loc[:,['people','peopleCd','repRoleNm']]
people_df.drop_duplicates(['peopleCd'], keep='first', inplace=True, ignore_index=True)
people_df.sort_values('people', inplace=True)

people_df.to_csv("people_list.txt", mode='w', encoding='utf8', index=False)
