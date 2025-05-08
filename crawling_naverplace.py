import requests
import re
from bs4 import BeautifulSoup
 
import pandas as pd
from datetime import datetime
import time
 
# selenium import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions() 
# options.add_argument('headless') 
options.add_argument("window-size=1920x1080") 
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox') 
# YW Driver Path
chrome_driver_path = r"C:\Users\ywj\Desktop\crawling\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# SH Driver Path
# chrome_driver_path = r"C:\Users\shcho\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service = service, options=options)
# wait seconds...
driver.implicitly_wait(3)

############### MODIFY HERE #################
driver.get('https://m.place.naver.com/place/21617530/review/visitor') 
time.sleep(10)

# driver.find_element(By.CSS_SELECTOR,'#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a').click()
# time.sleep(3)

# driver.find_element(By.CSS_SELECTOR,'#REVIEW > div > div._2LvIMaBiIO > div._3aC7jlfVdk > div._1txuie7UTH > ul > li:nth-child(2) > a').click()

time.sleep(3)

write_dt_lst = []
item_nm_lst = []
content_lst = []

# 현재 페이지
page_num = 1
# page_ctl = 3
# 날짜 
date_cut = (datetime.now() - timedelta(days = 365)).strftime('%Y%m%d')
while True :
    print(f'start : {page_num} page 수집 중...')
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)

    reviews = soup.findAll('li', {'class': 'place_apply_pui'})
    if not reviews:
        print("리뷰 없음 — 종료")
        break
    for review in range(len(reviews)):
        # <span class="pui__blind">2025년 5월 5일 월요일</span>
        
        write_dt_raw = reviews[review].find('div', {'class': 'pui__QKE5Pr'}).findAll('span' ,{'class' : 'pui__blind'})[1].get_text()
        print("write_dt_raw", write_dt_raw)
        write_dt_clean = write_dt_raw.rsplit(' ', 1)[0]
        print("write_dt_clean", write_dt_clean)
        write_dt = datetime.strptime(write_dt_clean, '%Y년 %m월 %d일').strftime('%Y%m%d')

        # item_nm_info_raw = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].get_text()

        # item_nm_info_for_del = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].find('dl', {'class' : 'XbGQRlzveO'}).get_text()

        # item_nm_info= re.sub(item_nm_info_for_del, '', item_nm_info_raw)

        # str_start_idx = re.sub(item_nm_info_for_del, '', item_nm_info_raw).find('제품 선택: ')

        # item_nm = item_nm_info[str_start_idx + 6:].strip()
        # <div class="pui__vn15t2"><a href="#" role="button" data-pui-click-code="rvshowmore" style="line-height: 2.4rem; word-break: break-all; display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-box-orient: vertical; -webkit-line-clamp: 3;">줄을 서서 들어가야 하는 서점이 있다면 믿으시겠습니까…? 여기가 바로 그런 곳입니다… 최근에 책에 관심이 생겨서 짧은 대전 여행 와중에 들렀다 간 곳인데 서점 앞에 사람들이 주루룩 줄을 서 있었습니다. 한번에 스무 명 남짓만 들어가서 쾌적하게 구경을 할 수 있도록 운영하고 있었는데 기다리는 건 조금 힘들었지만 들어가서는 여유롭게 책방의 분위기에 젖어 구경할 수 있었습니다. 책도 사고 영수증을 받았는데 기다란 영수증에 책방직원들이 적은 책 추천글도 있었습니다. 직원도 여섯명이나 된다던데 독립 서점이 이렇게 성황하다니 직원들이 이 공간을 무척 아끼고 사랑하는 느낌이 들었네요</a></div>
        # review_content_raw = reviews[review].findAll('div', {'class' : 'pui__vn15t2'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
        
        review_content_raw = reviews[review] \
            .find('div', {'class': 'pui__vn15t2'}) \
            .find('a', {'role': 'button', 'data-pui-click-code': 'rvshowmore'}) \
            .get_text(strip=True)
        
        review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))

        print(write_dt)
        # print(item_nm)
        print(review_content)
        write_dt_lst.append(write_dt)
        # item_nm_lst.append(item_nm)
        content_lst.append(review_content)
 
    if write_dt_lst[-1] < date_cut :
        break
        
    driver.find_element(By.CSS_SELECTOR,f'#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.k1QQ5 > div.NSTUp > div > a').click()    
    
    time.sleep(3)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)
 
    page_num += 1
    # page_ctl += 1
 
    # if page_num % 10 == 1 :
    #     page_ctl = 3
print('done')    

result_df = pd.DataFrame({
              'RD_CONTENT' : content_lst,
              'RD_WRITE_DT' : write_dt_lst })

result_df.to_csv('./output.csv', index = None, encoding = 'utf-8-sig')