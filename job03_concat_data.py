from codecs import ignore_errors
import datetime     # 내장 라이브러리


import pandas as pd

df = pd.read_csv('data/news_titles.csv')
print(df.head())

df_temp = pd.read_csv('data/naver_news_Politics_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)

df_temp = pd.read_csv('data/naver_news_Economic_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)
print(df.head())

df_temp = pd.read_csv('data/naver_news_Social_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)
print(df.head())

df_temp = pd.read_csv('data/naver_news_Culture_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)

df_temp = pd.read_csv('data/naver_news_World_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)

df_temp = pd.read_csv('data/naver_news_IT_Science_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)

df_temp = pd.read_csv('data/naver_headline_news_20260608.csv')
df=pd.concat([df_temp, df],ignore_index=True)

df_temp = pd.read_csv('data/naver_headline_news_20260604.csv')
df=pd.concat([df_temp, df],ignore_index=True)
df = df.drop_duplicates()    # 중복제거

print(df.head())
print(df.category.value_counts())
print(df.isnull().sum())
# null값 생김

df['category'] = df['category'].replace({'Economics': 'Economic'})

df.info()
df.to_csv('./data/news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)

