from bs4 import BeautifulSoup 
import requests
import math
import os
import time
import csv
import calendar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import pymysql
from urllib.request import urlopen
import requests
from selenium.webdriver.common.keys import Keys 

#이 파일은 selenium을 사용하여 유튜브 채널의 영상의 정보를 가지고 오는 코드이다.
#좋은 점은 채널 안의 모든 동영상을 가지고 올 수 있다는 점이다.
#안 좋은 점은 도중에 스크롤이 중단되면 정보가 완전히 가져올 수 없으며 채널의 영상이 크롤링하고자 하는 수보다 많을 경우 어쩔 수 없이 다 가지고 와야한다는 것이다.
#그러나 단점을 보완할 수 있는 아이디어는 모두가 이 코드를 보며 떠올릴 수 있으며 나 또한 여유가 된다면 만들어볼 것이다.  

# 이 링크는 유튜브 채널에서 동영상 부분을 누른 곳이다.
main_url = "https://www.youtube.com/user/esoundtraxmusic/videos"
driver = webdriver.Chrome("C:/driver_crawling/chromedriver.exe")
driver.get(main_url)
time.sleep(10)

# youtube는 body부분을 스크롤로 내려야하기 때문에 이런 스크롤 내리는 코드가 필요하다.
body = driver.find_element_by_tag_name('body')
num_of_pagedowns = 500 # 500번 page_down
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN) # body에 적용시킨다.
    time.sleep(0.3)
    num_of_pagedowns -= 1

time.sleep(50)

# 이 부분은 스크롤 내린 후 영상들의 정보가 한번에 box에 담긴다. 그렇기에 한 영상의 정보를 쪼개어 하나의 리스트로 만들어 주어야 한다. 예컨대 [a,b,c,d,e,f,g,h]라 한다면 한 영상의 정보는 a~d 즉 4개씩이다.

box = driver.find_elements_by_xpath('//*[@id="items"]') 
content=box[0].text
content_split=content.split("\n")
content_list=list(content_split)


# 리스트에서 4개씩 쪼개서 한 리스트에 담는다. 밑의 함수는 필요없다.
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

#이 부분이 정말 핵심인데 파이썬의 장점이라고 할 수 있겠다. 이 부분이 리스트의 정보를 4개씩 쪼개어 vd_info에 하나씩 담아주는 것이다.
vd_info=[]
[vd_info.append(content_list[i:i+4]) for i in range(0, len(content_list), 4)]
# print(len(vd_info))

#이 부분도 핵심이다. 유튜브의 소스가 많이 혼잡하고 불편하기에 규칙성을 찾기 어렵다. 그러나 정보가 담긴 길이와 thumbnail의 길이가 같다는 점을 파악하여 거기에서 소스를 찾아내어 보았다.
# 내가 가장 원하는 정보가 링크였는데 이로써 가장 필요한 부분을 크롤링 할 수 있었다.
link=[]
elems= driver.find_elements_by_id("thumbnail")
for i in elems:
    link.append(i.get_attribute("href"))

# print(type(link))
# print(len(link))
# print(link)

# print(type(vd_info))
# print(len(link))
# print(vd_info)


#위에 4개씩 쪼갠 부분에 링크를 하나씩 추가해주는 부분이다. enumerate라는 기능이 정말 유용했다.
for idx, i in enumerate(link):
    vd_info[idx].append(i)

print(vd_info,"\n")

#밑의 방식은 전의 크롤링과 동일하여 설명을 생략한다.

vd_link=[]
vd_title=[]
vd_pt=[]
vd_origin=[]
vd_main_url=[]


for i in vd_info:
    vd_pt.append(i[0])
    vd_title.append(i[1])
    vd_link.append(i[4])
    vd_origin.append(i)


print(vd_link)
print(vd_title)
print(vd_pt)
print(vd_origin)

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\vd_origin\\vd_resource.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.write(str(main_url + "\n"))
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\vd_origin\\vd_origin.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\origin_link.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\current_link.txt','w',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\vd_main_link.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.write(main_url + "\n")
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\title\\title.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()

f= open('C:\\Users\\user1\\Desktop\\final_crawler\\playtime\\playtime.txt','a',encoding='utf-8')
f.write("\nDATE{}\n\n".format(datetime.datetime.now()))
f.close()



for a in vd_origin:
    
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\vd_origin\\vd_origin.txt','a',encoding='utf-8')
    f.write(str(a)+"\n")
    f.close()

for b in vd_link:
    
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\origin_link.txt','a',encoding='utf-8')
    f.write(str(b)+"\n")
    f.close()

for b1 in vd_link:
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\link\\current_link.txt','a',encoding='utf-8')
    f.write(str(b1)+"\n")
    f.close()

for c in vd_title:
    
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\title\\title.txt','a',encoding='utf-8')
    f.write(str(c)+"\n")
    f.close()

for d in vd_pt:
    f= open('C:\\Users\\user1\\Desktop\\final_crawler\\playtime\\playtime.txt','a',encoding='utf-8')
    f.write(str(d)+"\n")
    f.close()

time.sleep(100)
driver.close()


# start_pos = 0
# end_pos = len(content_list)
# div = 4

# for idx in content_list):
#     out = content_list[start_pos:end_pos+ div]
#     if out != []:
#         vd_info.append(out)
#     start_pos = start_pos + div

# pprint.pprint(list(chunks(range(0, len(content_list)), 4)))



# print(vd_info)