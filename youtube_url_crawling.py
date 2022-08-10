from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import sys
def youtubeUrlCrawling():
    browser = webdriver.Chrome()
    browser.maximize_window()

    url = 'https://www.youtube.com/'
    browser.get(url)
    titleList = []
    dataList=[]
    s = []
    for i in range(18):
        t = sys.stdin.readline()
        if i % 2 == 0:
            s.append(t.rstrip()[1:])
    for i in s:
        url = 'https://www.youtube.com/'
        browser.get(url)
        titleList.append(i)
        search = browser.find_element_by_name('search_query')
        time.sleep(2)
        search.send_keys(i)
        search.submit()
        time.sleep(2)
        bs = BeautifulSoup(browser.page_source, 'html.parser')

        aa=bs.find('a',id='main-link')['href']
        dataList.append('https://www.youtube.com'+aa)
    print(titleList)
    print(dataList)

    data = {'제목': titleList,'링크': dataList}
    df = pd.DataFrame(data)  ## 데이터프래임 생성
    df.to_csv('smallmoney461.csv', index=False,encoding='utf-8-sig')
    print('complete')