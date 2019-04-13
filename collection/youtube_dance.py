import pymysql
import time
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 유투브 오디오 라이브러리 접속
main_url = "https://www.youtube.com/audiolibrary/music"
driver = webdriver.Chrome("C:/driver/chromedriver.exe")
driver.get(main_url)
time.sleep(3)

gid = 'audiocrawling'
gpw = 'encore7276'

# 아이디 입력
idlog = driver.find_element_by_id("identifierId")
idlog.clear()
idlog.send_keys(gid)
idlog.submit()
time.sleep(1)

# 다음 버튼 클릭
next_btn1 = driver.find_element_by_id("identifierNext")
next_btn1.click()
time.sleep(5)

# 페스워드 입력
pwlog = driver.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
pwlog.clear()
pwlog.send_keys(gpw)
pwlog.submit()
time.sleep(1)

# 다음 버튼 클릭
next_btn2 = driver.find_element_by_id("passwordNext")
next_btn2.click()
time.sleep(6)

# 장르 버튼 클릭
gr_btn = driver.find_elements_by_css_selector("div.multi-filters.right-menu > div:nth-child(1) > div > button")
gr_btn[0].click()
time.sleep(3)

# 클래식 항목 클릭 (class_name이 겹쳐서 총 개수 중에 39번째가 댄스)
cs_btns = driver.find_elements_by_class_name('yt-uix-menu-close-on-select')
cs_btns[39].click()
time.sleep(3)

# 리스트박스로 이동
in_listboxes = driver.find_elements_by_css_selector('div.audiolibrary-track-head > div.audiolibrary-column.audiolibrary-column-duration')
in_listboxes[0].click()
time.sleep(2)
in_listboxes[0].click()
time.sleep(3)

# 스크롤 내리기
body = driver.find_element_by_tag_name('body')
num_of_pagedowns = 80
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
    num_of_pagedowns -= 1

# 총 노래 갯수 구하기
munum_list = []
soup = BeautifulSoup(driver.page_source, "lxml")
for link in soup.find_all(class_='track'):
    munum = link.get('audiolibrary-track-head')
    munum_list.append(munum)
allmunum = len(munum_list)

# 다운받기
# for i in range(5):
# for i in range(allmunum-1):
#     dw_btns = driver.find_elements_by_css_selector('div.audiolibrary-column.audiolibrary-column-download > a')
#     dw_btns[i].click()
#     time.sleep(1)

# 음악정보 리스트
title_list = []
length_list = []
writer_list = []
genre_list = []
mood_list = []

# 위치 설정
titles = driver.find_elements_by_css_selector("div.audiolibrary-track-head > div.audiolibrary-column.audiolibrary-column-title")
lengths = driver.find_elements_by_css_selector("div.audiolibrary-track-head > div.audiolibrary-column.audiolibrary-column-duration")
writers = driver.find_elements_by_css_selector("div.audiolibrary-track-head > div.audiolibrary-column.audiolibrary-column-artist")
genres = driver.find_elements_by_css_selector("div.audiolibrary-column.audiolibrary-column-genre-and-mood > a:nth-child(1)")
moods = driver.find_elements_by_css_selector("div.audiolibrary-column.audiolibrary-column-genre-and-mood > a:nth-child(3)")

# 음악정보 찾기
# for i in range(5):
for i in range(allmunum-2):

    # 타이틀
    str_title = titles[i].text
    title_list.append(str_title)

    # 길이    
    str_length = lengths[i].text
    length_list.append(str_length)

    # 작곡가    
    str_writer = writers[i].text
    writer_list.append(str_writer)

    # 장르
    str_genre = genres[i].text
    genre_list.append(str_genre)

    # 분위기    
    str_mood = moods[i].text
    mood_list.append(str_mood)

# DB에 접속
conn = pymysql.connect(host= 'localhost', user='root', password = '7276', db= 'audiolib', charset='utf8')
cur =conn.cursor()

# DB 초기화
cur.execute("truncate audiolib;")
sql = "INSERT INTO audiolib(num, title, lengths, writer, genre, mood) VALUES(%s,%s,%s,%s,%s,%s)"

# DB에 넣기
for i in range(allmunum-2):
    cur.execute(sql, (i+1, title_list[i], length_list[i], writer_list[i], genre_list[i], mood_list[i]))
conn.commit()

# 종료
# time.sleep(50)
# driver.close()


'''
create table audiolib(
   num int not null,
	title varchar(200),
   lengths varchar(50),
   writer varchar(100),
   genre varchar(50),
   mood varchar(50),
   primary key(num)
);
'''