# file name: naver_news_section.csv
# 컬럼 명은 titles, category
# 00: 정치, 경제 / 01: 사회, 문화 / 02: 세계, IT
# 다 되면 PR

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re           # 내장 라이브러리
import datetime     # 내장 라이브러리

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

options = ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_argument('headless')    # browser window off

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

df_titles = pd.DataFrame()
titles = []

url = 'https://news.naver.com/section/104'
driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'
# '//*[@id="newsct"]/div[4]/div/div[2]/a' # 뉴스 더보기에 대한 버튼에 대한 Xpath


for i in range(5):
    driver.find_element(By.XPATH, button_xpath).click()
    time.sleep(0.5)

for i in range(1, (5)):
    for j in range(1, 7):
        try:
            title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
            titles.append(title)
        except:
            print('error',i, j)

df_section_titles = pd.DataFrame(titles, columns=['title'])
df_section_titles['category'] = 'World'
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

df_titles.info()
df_titles.to_csv('./data/naver_news_world_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)