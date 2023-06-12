# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 02:29:01 2023

@author: Chahoo414
"""

# text 분석용 파일 만드는 코드

import pandas as pd
from konlpy.tag import Kkma # KoNLPy 코엔엘파이
kkma = Kkma()
from konlpy.tag import Okt
okt = Okt()
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 리뷰 데이터 불러오기
while True :
    tag = int(input('분석하고자 하는 상품의 tag를 입력하세요 > '))
    try :
        file_name = f'(스크래이핑 파일 경로)/scraping_file_{tag}.csv'
        df = pd.read_csv(file_name, encoding='cp949')
        break
    except :
        print('scraping_file이 존재하지 않습니다. 다른 상품의 tag를 입력해주세요.')


# 제목 분석
# 제목 리뷰를 텍스트화
title = df['review_title']
title.to_csv(f"(원하는 파일 경로)/{tag}_review_title.txt", index=False)

# text 읽기
file = open(f"(위에서 생성한 제목 text 파일 경로)/{tag}_review_title.txt", mode='r', encoding='utf-8')
doc = file.read()
file.close()


# 컬럼인 'review_title'까지 가져와버려서 삭제
doc = doc[13:]

# 개행문자(\n)을 제거
new_doc = doc.replace("\n", " ")


# 명사만 분리
ex_sent = kkma.sentences(new_doc)

from re import match  # 전처리 위해서 정규표현식 관련 re 패키지 import
nouns = []
for sent in ex_sent : 
    for noun in okt.nouns(sent) :
        # 단어 전처리 : 2음절 이상, 수사 제외
        if len(str(noun)) >= 2 and not(match('^[0-9]', noun)) :
            nouns.append(noun)


# 단어 갯수 세기 및 단어와 카운트
word_count = {} # 빈 set
for noun in nouns :
    word_count[noun] = word_count.get(noun, 0) + 1

from collections import Counter

counter = Counter(word_count)

top50 = counter.most_common(50)
print (top50)


# 제한 단어 입력받고 없애기
while True :
    stopwords = list(input('제거하고 싶은 단어를 띄어쓰기를 기준으로 입력해주세요 >\n').split())
    words = [word for word in nouns if word not in stopwords]

    # 단어 없앴으니 다시 count하기
    word_count = {} # 빈 set
    for noun in words :
        word_count[noun] = word_count.get(noun, 0) + 1
        
    counter = Counter(word_count)
    
    top50 = counter.most_common(50)
    print (top50)
    
    # 다시 바꿀지 말지 확인
    repeat_key = input('추가로 제거하고 싶은 단어가 있을 경우 "1", 없는 경우 "2"를 입력해주세요. > ')
    if repeat_key == '2' :
        break


# 수정하고 싶은 단어 있으면 바꾸기
while True :
    modify_word = list(input('수정을 원하는 단어는 띄어쓰기를 기준으로 입력해주세요 >\n').split())
    replaced_word = list(input('수정되었으면 하는 단어를 띄어쓰기 기준으로 입력해주세요 >\n').split())
    if len(modify_word) != len(replaced_word):
        print('수정하고자 하는 단어의 갯수가 다릅니다. 다시 입력해주세요')
        continue
    
    # 원하는 단어 있으면 바꾸기
    for i in range(len(words)):
        for j in range(len(modify_word)) :
            if words[i] == modify_word[j] :
                words[i] = replaced_word[j]

    # 단어 바꿨으면 다시 count하기
    word_count = {} # 빈 set
    for noun in words :
        word_count[noun] = word_count.get(noun, 0) + 1
        
    counter = Counter(word_count)
    
    top50 = counter.most_common(50)
    print (top50)
    
    # 다시 바꿀지 말지 확인
    repeat_key = input('추가로 바꾸고 싶은 단어가 있을 경우 "1", 없는 경우 "2"를 입력해주세요. > ')
    if repeat_key == '2' :
        break


# 파일화
temp_df = pd.DataFrame(counter, index=['count'])
temp_df = temp_df.T
temp_df.reset_index(drop=False, inplace=True)
temp_df= temp_df.rename(columns={'index':'word'})
temp_df.to_csv(f"(원하는 파일 경로)/{tag}_review_title.csv", encoding='cp949', index=True)




# 본문 분석
# 본문 리뷰를 텍스트화
review_text = df['review_text']
review_text.to_csv(f"(원하는 파일 경로)/{tag}_review_text.txt", index=False)

# text 읽기
file = open(f"(위에서 생성한 본문 txt 파일 경로)/{tag}_review_text.txt", mode='r', encoding='utf-8')
doc = file.read()
file.close()


# 컬럼인 'review_text'까지 가져와버려서 삭제
doc = doc[13:]

# 개행문자(\n)을 제거
new_doc = doc.replace("\n", " ")


# 명사만 분리
ex_sent = kkma.sentences(new_doc)

from re import match  # 전처리 위해서 정규표현식 관련 re 패키지 import
nouns = []
for sent in ex_sent : 
    for noun in okt.nouns(sent) :
        # 단어 전처리 : 2음절 이상, 수사 제외
        if len(str(noun)) >= 2 and not(match('^[0-9]', noun)) :
            nouns.append(noun)


# 단어 갯수 세기 및 단어와 카운트
word_count = {} # 빈 set
for noun in nouns :
    word_count[noun] = word_count.get(noun, 0) + 1

from collections import Counter

counter = Counter(word_count)

top50 = counter.most_common(50)
print (top50)


# 제한 단어 입력받고 없애기
while True :
    stopwords = list(input('제거하고 싶은 단어를 띄어쓰기를 기준으로 입력해주세요 >\n').split())
    words = [word for word in nouns if word not in stopwords]

    # 단어 없앴으니 다시 count하기
    word_count = {} # 빈 set
    for noun in words :
        word_count[noun] = word_count.get(noun, 0) + 1
        
    counter = Counter(word_count)
    
    top50 = counter.most_common(50)
    print (top50)
    
    # 다시 바꿀지 말지 확인
    repeat_key = input('추가로 제거하고 싶은 단어가 있을 경우 "1", 없는 경우 "2"를 입력해주세요. > ')
    if repeat_key == '2' :
        break


# 수정하고 싶은 단어 있으면 바꾸기
while True :
    modify_word = list(input('수정을 원하는 단어는 띄어쓰기를 기준으로 입력해주세요 >\n').split())
    replaced_word = list(input('수정되었으면 하는 단어를 띄어쓰기 기준으로 입력해주세요 >\n').split())
    if len(modify_word) != len(replaced_word):
        print('수정하고자 하는 단어의 갯수가 다릅니다. 다시 입력해주세요')
        continue
    
    # 원하는 단어 있으면 바꾸기
    for i in range(len(words)):
        for j in range(len(modify_word)) :
            if words[i] == modify_word[j] :
                words[i] = replaced_word[j]

    # 단어 바꿨으면 다시 count하기
    word_count = {} # 빈 set
    for noun in words :
        word_count[noun] = word_count.get(noun, 0) + 1
        
    counter = Counter(word_count)
    
    top50 = counter.most_common(50)
    print (top50)
    
    # 다시 바꿀지 말지 확인
    repeat_key = input('추가로 바꾸고 싶은 단어가 있을 경우 "1", 없는 경우 "2"를 입력해주세요. > ')
    if repeat_key == '2' :
        break


# 파일화
temp_df = pd.DataFrame(counter, index=['count'])
temp_df = temp_df.T
temp_df.reset_index(drop=False, inplace=True)
temp_df= temp_df.rename(columns={'index':'word'})
temp_df.to_csv(f"(원하는 경로)/{tag}_review_text.csv", encoding='cp949', index=True)



