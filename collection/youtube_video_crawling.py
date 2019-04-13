from bs4 import BeautifulSoup 
import requests
import math
import os
import time
import csv
import calendar
import codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
from urllib.request import urlopen
import lxml
import requests
from selenium.webdriver.common.keys import Keys 
import datetime

# 비디오의 정보를 담을 딕션을 만들어준다.
video_info = {
    'title':'',
    'video_link':'',
    'play_time':'',
}

# 필요한 변수를 선언한다.
link=[]
vd_link=[]


# 페이지의 영상의 정보를 받아오는 함수
def get_video_link(target_url):
    # beautiful soup를 사용하여 item이 담긴 곳을 lis에 담는다.
    response = requests.get(target_url) 
    soup = BeautifulSoup(response.text, "lxml")
    lis = soup.find_all('li', {'class' : 'channels-content-item yt-shelf-grid-item'}) 
    
    #lis에는 하나의 컨텐츠가 들어가 있으니 하나씩 들어가서 정보를 뽑아보자.
    for li in lis :
        #<a class="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2" dir="ltr" title="Eminem - Phenomenal (Behind The Scenes)" href="/watch?v=NEGjmd_RzLU">Eminem - Phenomenal (Behind The Scenes)</a>
        title = li.find('a', {'title' : True})['title'] 
        video_link = 'https://www.youtube.com' + li.find('a', {'href' : True})['href'] 
        #<span class="video-time" aria-hidden="true"><span aria-label="8분, 55초">8:55</span></span> 
        play_time = li.find('span', {'class' : 'video-time'}).text #<ul class="yt-lockup-meta-info"><li>조회수 2,902,617회</li><li>6개월 전</li></ul> #hits_and_
        
        #한 컨텐츠에서 나온 정보를 위에서 만든 딕션에 넣는다.
        video_info = {
            'title' : title,
            'video_link' : video_link,
            'play_time' : play_time,
            }

        # 딕션에 담긴 key와 value 중에 우리가 사용해야할 것은 value이기 때문에 
        # value만 뽑아서 link라는 곳에 담는다.
        link.append(list(video_info.values()))
        
        #link 에는 3가지 정보가 들어가 있고 그것을 따로 담을 변수를 선언한다.
        vd_link=[]
        vd_title=[]
        vd_pt=[]
        vd_origin=[]

        # 각 변수에 정보를 넣는 for문을 만든다.
        for i in link:
            vd_title.append(i[0])
            vd_link.append(i[1])
            vd_pt.append(i[2])
            vd_origin.append(i)
            

    print(link)

    #각 변수에 담긴 정보를 파일로 만들어 저장한다. 'a'모드는 추가저장 즉 history를 만들 수 있으며 'w'모드로 한다면 매번 새롭게 정보가 갱신되는 것
    # 우선 받은 날짜를 넣어주기 위해 이런 식으로 저장한 것이다.

    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\vd_origin\\vd_origin.txt','a')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.close()

    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\origin_link.txt','a')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.close()

    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\current_link.txt','w')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.close()
    
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\vd_main_link.txt','a')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.write(target_url + "\n")
    f.close()

    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\title\\title.txt','a')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.close()

    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\playtime\\playtime.txt','a')
    f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
    f.close()

    #for문을 돌면서 각 변수에 담긴 정보를 하나씩 해당되는 파일에 차근차근 저장한다.
    for a in vd_origin:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\vd_origin\\vd_origin.txt','a', encoding='utf-8')
        f.write(str(a)+"\n")
        f.close()

    for b in vd_link:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\origin_link.txt','a', encoding='utf-8')
        f.write(str(b)+"\n")
        f.close()

    for b1 in vd_link:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\current_link.txt','a', encoding='utf-8')
        f.write(str(b1)+"\n")
        f.close()

    for c in vd_title:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\title\\title.txt','a', encoding='utf-8')
        f.write(str(c)+"\n")
        f.close()

    for d in vd_pt:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\playtime\\playtime.txt','a', encoding='utf-8')
        f.write(str(d)+"\n")
        f.close()

    return video_info 

#위에까지가 get_video_link라는 함수를 만든 것이고 위에 두줄이 그 함수를 실행시킬 코드이다.
target_url = 'https://www.youtube.com/channel/UCk6ShwTnpY28A6ijvv4Pmgw/videos'
get_video_link(target_url)  



