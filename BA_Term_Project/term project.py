# -*- coding: utf-8 -*-
"""
Created on Fri May 26 13:06:38 2023

@author: Chahoo414
"""

# 네이버쇼핑 상품 리뷰 스크레이핑

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# 상품코드 파일 불러와서 출력
product_list = pd.read_csv("(상품코드 파일 경로)", encoding='cp949')
print(product_list)
print()
tag = input('스크레이핑 할 상품의 코드를 입력해주세요. ')

# 웹페이지 열기
options = webdriver.ChromeOptions()     # 정상적으로 크롤링을 하기 위해서 사용자의 정보가 필요한데, 그 중 하나로 사용자의 브라우저 환경이 필요해서 옵션으로 추가해서 넣은 것
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36")  # add_argu는 부가적인 정보를 포함한다는 의미
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# 웹페이지를 펴고 사이트를 불러오기 전에 잠시 로딩 기다리기
time.sleep(2)

# 웹페이지 불러오기
url = f'https://search.shopping.naver.com/catalog/{tag}'
driver.get(url)


# 전체 리뷰 데이터를 저장할 리스트
total_review_data = []

# 리뷰를 최신순으로 보기 위해 "최신순" 버튼 클릭
recent_button = driver.find_element_by_xpath('//*[@id="section_review"]/div[2]/div[1]/div[1]/a[2]')
recent_button.click()
time.sleep(1)

# 스크레이핑 코드 
scraping_repeat_key = True
page_num = 1
while scraping_repeat_key :
    
    review_page_repeat_num = True
    review_num = 1
    while review_page_repeat_num :
        try :
            # 리뷰 펼치기 클릭
            url_path = f'//*[@id="section_review"]/ul/li[{review_num}]/div[3]/a'
            driver.find_element_by_xpath(url_path).click()
            
            # 리뷰 영역 지정
            review_element = driver.find_element_by_xpath(f'//*[@id="section_review"]/ul/li[{review_num}]')

            # 별점, 구매사이트, 작성자, 작성일자, 제목, 텍스트 긁어오기
            review_stars = review_element.find_element_by_class_name("reviewItems_average__0kLWX")
            reveiw_buy_site = review_element.find_element_by_xpath(f'//*[@id="section_review"]/ul/li[{review_num}]/div[1]/span[2]')
            review_name = review_element.find_element_by_xpath(f'//*[@id="section_review"]/ul/li[{review_num}]/div[1]/span[3]')
            review_date = review_element.find_element_by_xpath(f'//*[@id="section_review"]/ul/li[{review_num}]/div[1]/span[4]')
            review_title = review_element.find_element_by_class_name("reviewItems_title__AwHcz")
            review_text = review_element.find_element_by_class_name("reviewItems_text__XrSSf")

            # 리뷰 데이터를 전체 리뷰 리스트에 저장
            temp_data = [review_stars.text, reveiw_buy_site.text, review_name.text, review_date.text, review_title.text, review_text.text]
            total_review_data.append(temp_data)

            # 다음 리뷰 선택
            review_num += 1
    
        except :     # 펼칠 수 있는 페이지가 없을 경우의 예외처리
            review_page_repeat_num = False
            
    # !몇 번째 페이지를 긁었는지 확인용
    print(f'{page_num}번째 페이지 완료')

    # 다음 페이지 클릭 준비
    page_num += 1
    
    try :
        # 버튼 영역 한정
        button_element = driver.find_element_by_xpath('//*[@id="section_review"]/div[3]')
        # 다음 페이지 버튼 영역 지정
        next_page_button = button_element.find_element_by_css_selector(f'[data-nclick="N=a:rev.page,r:{page_num}"]')
        next_page_button.click()    # 버튼 클릭
        # 봇 인식을 피하기 위해 다음 리뷰 페이지 클릭 후 1~2초 사이 랜덤 대기
        time.sleep(random.uniform(1,2))
        
    except :    # 해당 페이지가 마지막일 수 있으니 예외 처리
        scraping_repeat_key = False

# 웹페이지 닫기
driver.quit()

# !네이버상품리뷰 페이지는 리뷰를 2000개까지만 표시하도록 되어 있으며, 그 이상의 리뷰는 필터를 통해 확인할 수 있도록 되어 있다.


# df화 시키기
df = pd.DataFrame(total_review_data, columns=['review_stars', 'reveiw_buy_site', 'review_name', 'review_date', 'review_title', 'review_text'])
print(df.info())

# 파일로 내보내기(!한글깨짐 현상 처리 필요 => errors='replace' 추가)
df.to_csv(f"(원하는 파일 경로)/scraping_file_{tag}.csv", encoding='cp949', index=True,  errors='replace')





