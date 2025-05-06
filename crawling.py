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

chrome_driver_path = r"C:\Users\shcho\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service = service, options=options)
# wait seconds...
driver.implicitly_wait(3)

############### MODIFY HERE #################
driver.get('SMARTSTORE URL') 
time.sleep(10)

driver.find_element(By.CSS_SELECTOR,'#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a').click()
time.sleep(3)

driver.find_element(By.CSS_SELECTOR,'#REVIEW > div > div._2LvIMaBiIO > div._3aC7jlfVdk > div._1txuie7UTH > ul > li:nth-child(2) > a').click()

time.sleep(3)

write_dt_lst = []
item_nm_lst = []
content_lst = []

# 현재 페이지
page_num = 1
page_ctl = 3
# 날짜 
date_cut = (datetime.now() - timedelta(days = 365)).strftime('%Y%m%d')
while True :
    print(f'start : {page_num} page 수집 중, page_ctl:{page_ctl}')
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)

    reviews = soup.findAll('li', {'class': 'BnwL_cs1av'})

    for review in range(len(reviews)):

        write_dt_raw = reviews[review].findAll('span' ,{'class' : '_2L3vDiadT9'})[0].get_text()
        write_dt = datetime.strptime(write_dt_raw, '%y.%m.%d.').strftime('%Y%m%d')

        item_nm_info_raw = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].get_text()

        item_nm_info_for_del = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].find('dl', {'class' : 'XbGQRlzveO'}).get_text()

        item_nm_info= re.sub(item_nm_info_for_del, '', item_nm_info_raw)

        str_start_idx = re.sub(item_nm_info_for_del, '', item_nm_info_raw).find('제품 선택: ')

        item_nm = item_nm_info[str_start_idx + 6:].strip()

        review_content_raw = reviews[review].findAll('div', {'class' : '_1kMfD5ErZ6'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
        review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))

        print(write_dt)
        print(item_nm)
        print(review_content)
        write_dt_lst.append(write_dt)
        item_nm_lst.append(item_nm)
        content_lst.append(review_content)
 
    if write_dt_lst[-1] < date_cut :
        break
        
    driver.find_element(By.CSS_SELECTOR,f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({page_ctl})').click()    
    time.sleep(3)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)
 
    page_num += 1
    page_ctl += 1
 
    if page_num % 10 == 1 :
        page_ctl = 3
print('done')    

result_df = pd.DataFrame({
              'RD_ITEM_NM' : item_nm_lst,
              'RD_CONTENT' : content_lst,
              'RD_WRITE_DT' : write_dt_lst })

result_df.to_csv('./output.csv', index = None, encoding = 'utf-8-sig')