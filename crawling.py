from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def crawling():
    browser = webdriver.Chrome()
    browser.maximize_window()

    url = "https://playboard.co/search?q=%EC%9E%AC%ED%85%8C%ED%81%AC&subscribers=10000%3A&sortTypeId=1"
    browser.get(url)
    prev_height = browser.execute_script("return document.body.scrollHeight")

    # 웹페이지 맨 아래까지 무한 스크롤
    while True:
        # 스크롤을 화면 가장 아래로 내린다
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        # 페이지 로딩 대기
        time.sleep(5)

        # 현재 문서 높이를 가져와서 저장
        curr_height = browser.execute_script("return document.body.scrollHeight")

        if (curr_height == prev_height):
            time.sleep(3)
            if (curr_height == prev_height):
                break
        else:
            prev_height = browser.execute_script("return document.body.scrollHeight")
    bs = BeautifulSoup(browser.page_source, "html.parser")
    titleList = []
    contentList = []
    subscribersList = []
    mediaNumList = []
    viewNumList = []
    likeNumList = []
    updateList = []

    tags2 = bs.select("div.meta")
    for tags in tags2:
        titleList.append(tags.select("h2.name")[0].string)
        contentList.append('')
        content=tags.select("div.desc")
        if content !=[]:
            contentList[len(contentList)-1]=content[0].string
        tags3=tags.select("ul.simple-scores")
        for tag in tags3:
            t=tag.select('li')
            subscribersList.append(t[0].string)
            mediaNumList.append(t[1].string)

    tags = bs.select("div.scores > table > tbody")

    for tag in tags:
        t=tag.select('tr.item > td.item__value')
        num=len(viewNumList)
        viewNumList.append('')
        likeNumList.append('')
        updateList.append('')
        if(len(t) >= 1):
            viewNumList[num-1]=(t[0].string)
        if(len(t) >= 2):
            likeNumList[num-1]=(t[1].string)
        if (len(t) == 3):
            updateList[num-1]=(t[2].string)

    data = {'제목': titleList, '내용': contentList, '구독자수': subscribersList, '영상수': mediaNumList, '7일 조회': viewNumList,
            '좋아요 비율': likeNumList, '마지막 업데이트': updateList}

    df = pd.DataFrame(data)  ## 데이터프래임 생성
    df.to_csv('financial.csv', index=False,encoding='utf-8-sig')
    print('complete')