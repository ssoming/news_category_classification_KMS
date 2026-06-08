from bs4 import BeautifulSoup
import requests
import pandas as pd
import re           # 내장 라이브러리
import datetime     # 내장 라이브러리


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT_Science']
df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)
    # print(resp)
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)
    title_tag = soup.select('.sa_text_strong')  # class = sa_text_strong 인 것 만 부르기.
    print(title_tag)

    titles = []
    for title in title_tag:
        titles.append(title.text)
    print(titles)
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

print(df_titles.head())
df_titles.info()
df_titles.to_csv('./data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
