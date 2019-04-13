from bs4 import BeautifulSoup 
import lxml 
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
from pytube import YouTube

#저장된 링크에서 영상을 다운받는 부분이다. 나는 현재 링크만 담긴 파일을 열어서 그것만 다운로드 받기를 원하기에 current_link라는 파일을 열어서 가져온다.

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\current_link.txt','r', encoding='utf-8')
link_str = f.read()
print(link_str)
f.close()

#다운로드하는 도중에 regex정규표현식 오류가 뜨기 때문에 성공한 링크와 오류가 뜬 링크를 따로 담는 변수를 만든다.
#또한 \n으로 split을 하면 각 링크들이 구분된다.

suc_link = []
error_link =  []
link_split = link_str.split("\n")
print(len(link_split))

# 밑에 yt부분이 youtube에서 링크를 가지고와서 다운로드 하는 라이브러리이다. 이걸 사용하여 자신이 원하는 곳에 파일을 저장할 수 있다.
# 이때 if 'h' in i: 이 부분을 왜 했냐하면 파일 형식을 보면 링크만 쫙 담긴 것이 아니라 크롤링 한 시점과 구분해주려고 한 개행이 들어가 있기에 링크와 링크 아닌 것을 구분해주기 위하여 이런 코드를 작성해보았다. h는 링크에는 http:에 h가 꼭 들어가 있기 때문에..

for i in link_split:
    try:
        if 'h' in i:
            yt = YouTube('{}'.format(i)) 
            yt.streams.filter(progressive=True, file_extension='mp4').first().download('G:\\팀 드라이브\\recommendation_project\\new2')
            print(i + " ")
            print("저장완료")
            suc_link.append(i)

            
    except Exception as e:
        print(i)
        error_link.append(i)
        print("저장 실패 : Regex PatternError ", e)
        continue

print("\n저장완료 : ",len(suc_link), "\n")
print("저장실패 : ",len(error_link), "\n")

# Suc_link를 저장하는 파일을 따로 만들어준다.
f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\suc_link.txt','a', encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()

for i in suc_link:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\suc_link.txt','a',encoding='utf-8')
        f.write(str(i)+"\n")
        f.close()


# Error_link를 저장하는 파일을 따로 만들어준다.
f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\error_link.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()


for i in error_link:
        f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\error_link.txt','a', encoding='utf-8')
        f.write(str(i)+"\n")
        f.close()


