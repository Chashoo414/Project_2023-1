
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 00:21:24 2023

@author: Chahoo414
"""

# 상품코드 스크레이핑 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36")  # add_argu는 부가적인 정보를 포함한다는 의미
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
time.sleep(1)

# 웹페이지 열기
url = f'https://search.shopping.naver.com/search/category/100010443?catId=50014540&frm=NVSHMDL&origQuery&pagingIndex=1&pagingSize=80&productSet=model&query&sort=rel&timestamp=&viewType=list'
driver.get(url)


# 전체 상품 코드 리스트
product_list = []

scraping_repeat_key = True
page_num = 1

while scraping_repeat_key :
    # 스크롤 끝까지 내리기
    scroll_location = driver.execute_script("return document.body.scrollHeight")
    while True:
        #현재 스크롤 아래로 내림
        for _ in range(10) :
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            driver.implicitly_wait(1)      
        #늘어난 스크롤 높이
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if scroll_location == scroll_height:
            break
        #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
        else:
            #스크롤 위치값을 수정
            scroll_location = driver.execute_script("return document.body.scrollHeight")
        # 종료까지 반복

    # 스크레이핑 코드    
    product_repeat_key = True
    product_num = 1
    while product_repeat_key :
        try :
            # 상품명 및 코드번호 하나씩 스크레이핑
            product_element = driver.find_element_by_xpath(f'//*[@id="content"]/div[1]/div[2]/div/div[{product_num}]')
            # 상품명 및 코드 가져오기
            product = product_element.find_element_by_class_name('product_title__Mmw2K')
            rink = product_element.find_element_by_xpath(f'//*[@id="content"]/div[1]/div[2]/div/div[{product_num}]/div/div/div[2]/div[1]/a')

            # 전체 상품 리스트에 추가
            temp_list = [product.text, rink.get_attribute('data-i')]
            product_list.append(temp_list)

            # 다음 상품 영역
            product_num += 1
        except :
            product_repeat_key = False
            
    # 다음 페이지 클릭
    page_num += 1
    
    try :
        # 버튼 영역 한정
        button_element = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div')
        # 다음 페이지 버튼 영역 지정
        next_page_button = button_element.find_element_by_css_selector(f'[data-nclick="N=a:pag.page,i:{page_num}"]')
        next_page_button.click()    # 버튼 클릭
        driver.implicitly_wait(5)   # 다음 리뷰 페이지 로딩까지 대기

    except :    # 해당 페이지가 마지막일 수 있으니 예외 처리
        scraping_repeat_key = False
      
# 웹페이지 닫기
driver.quit()


# 파일화
df = pd.DataFrame(product_list, columns=['제품명', '제품코드'])
df.info()


df.to_csv("(원하는 파일 경로)/product_code.csv", encoding='cp949', errors='replace', index=False)
