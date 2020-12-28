from math import log
from collections import Counter
from konlpy.tag import Mecab
from textrank import KeysentenceSummarizer
from textrank import KeywordSummarizer
from python_utils import logger
from wordcloud import WordCloud

import pandas as pd
import numpy as np                                                       
import os, re, time, csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import operator

%matplotlib inline
mecab = Mecab()



# 형태소 분석 전처리 함수
def change_sents(texts):
    mecab = Mecab()
    sents_new = []
    for i in range(len(texts)):
        a = mecab.pos( phrase=texts[i], flatten=True)
        result = []
        for j in range(len(a)):
            b = a[j][0] + '/' + a[j][1]
            if j == len(a)-1:
                result.append(b)
            else:
                result.append(b)
                result.append(' ')
        result1 = ''
        for i in result:
            result1 += i
        sents_new.append(result1)

    return sents_new


# keyword (textrank 기반)
def mecab_tokenize(sent):
    words = sent.split()
    words = [w for w in words if ('/NN' in w and list(w)[1]!='/' and '이랑' not in w)] 
    return words


def textrank_key_word(sent, n):
    keyword_extractor = KeywordSummarizer(
        tokenize = mecab_tokenize,
        window = -1,
        verbose = False
    )
    keywords = keyword_extractor.summarize(sents, topk=n)
    KEYWORD  = []
    RANK = []
    
    for word, rank in keywords:
        temp = list(word)
        del temp[-4:]
        temp = "".join(temp)
        KEYWORD.append(temp)
        RANK.append(rank)

    key_word = []
    rank = []
    for i in range(len(KEYWORD)):
        if KEYWORD[i] not in key_word:
            key_word.append(KEYWORD[i])
            rank.append(RANK[i])
    return key_word, rank


# 빈도기반 키워드 추출 함수
def prob_key_word(text,n):
    word_list_1 = []
    mecab = Mecab()
    for i in range(len(text)):
        a = mecab.nouns(phrase=text[i])
        for keyword in a:
            word_list_1.append(keyword)
    word_list_1 = list(filter(lambda x: len(x)>1, word_list_1))
    count = Counter(word_list_1)
    noun_list = count.most_common(n)
    keyword = []
    keyword_cnt = []
    for key, cnt in noun_list:
        keyword.append(key)
        keyword_cnt.append(cnt)
    return keyword, keyword_cnt


# 키워드 딕셔너리 생성 함수
def keyword_dic(keyword, text):
    dic = {}
    for k_word in keyword[0]:
        dic[k_word]=[]
    for k_word in keyword[0]:
        for sentence in text:
            if k_word in sentence:
                dic[k_word].append(sentence)    
    return dic


# 한 문장씩 분할 함수 ('.' 포함)
def split_sentence_dot(text):
    temp = text.split('.')
    del temp[-1]
    texts = []

    for sen in temp:
        sen = sen.strip()
        sen += '.'
        texts.append(sen)
    return texts


# 한 문장씩 분할 함수 ('.' 미포함)
def split_sentence(text):
    temp = text.split('.')
    del temp[-1]
    texts = []
    
    for sen in temp:
        sen = sen.strip()
        texts.append(sen)
    return texts


# 핵심 문장 추출
def mecab_tokenizer(sent):
    words = mecab.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w and list(w)[1]!='/')]
    return words


def summarizer_text(texts, n):
    summarizer = KeysentenceSummarizer(
        tokenize = mecab_tokenizer,
        min_sim = 0.3,
        verbose = False
    )
    sent = []
    keysents = summarizer.summarize(texts, topk=n)
    for _, _, a in keysents:
        sent.append(a)
    final_sent = []
    for i in texts:
        if i in sent:
            final_sent.append(i)
    return final_sent


# text 시간대별 분할 함수
def split_texts(text, n):
    split_texts = []
    len_texts = len(texts)

    if (len_texts % n) == 0:
        number = len_texts//n
    else:
        number = len_texts//n + 1

    for i in range(n):
        if i == n-1:
            split_texts.append(texts[(i*number):])
        else:
            split_texts.append(texts[(i*number):(i+1)*number])
    return split_texts


# 시간대별 키워드 추출 함수
def split_keyword(split_text, n):
    split_keyword = []
    
    for i in range(len(split_text)):
        split_keyword.append((prob_key_word(split_text[i], n)[0], prob_key_word(split_text[i], n)[1]))
    return split_keyword


# WordCloud 생성 함수
def wordcloud(texts):
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path, size=18)
    file_name = 'wordcloud'
    wc = WordCloud(font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
                  background_color = "white",
                  width=1000,
                  height=1000,
                  max_words=100,
                  max_font_size=300)
    
    mecab = Mecab()
    total_text = ' '.join(texts)

    noun = mecab.nouns(total_text)
    for i, v in enumerate(noun):
        if len(v)<2:
            noun.pop(i)
    count = Counter(noun)
    noun_list = count.most_common(100)
    
    wordcloud_words = wc.generate_from_frequencies(dict(noun_list))
    fig = plt.figure(figsize = (10,10))
    plt.imshow(wordcloud_words,interpolation='bilinear')
    plt.axis("off")
    plt.savefig(file_name)
    plt.show()

    
# chart 생성 함수
def chart(split_keyword):
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path, size=18)
    MAX = 0
    title = ['초반', '중반', '후반']
    
    for i in range(len(split_keyword)):
        max_value = max(split_keyword[i][1])
        if MAX < max_value:
            MAX = max_value
    
    for i in range(len(split_keyword)):
        x = np.arange(len(split_keyword[0][0]))
        keyword = split_keyword[i][0]
        cnt = split_keyword[i][1]
        name = 'chart' + str(i+1) + '.png'
        title_name = title[i]
        plt.bar(x, cnt)
        plt.xticks(x, keyword, fontproperties=fontprop)
        plt.xticks(size = 20)
        plt.yticks(size = 20)
        plt.ylim([0, MAX])
        plt.title(title_name, fontproperties=fontprop, size = 30)
        plt.savefig(name)
        plt.show()

        
# chart2 생성 함수
def chart2(texts, keyword_list, n=5):
    split_text1 = split_texts(texts, n)
    cnt = 0
    ls = []
    final = []

    for key in keyword_list:
        for j in range(len(split_text1)):
            for i in split_text1[j]:
                if key in i:
                    cnt += 1
            ls.append(cnt)
            cnt = 0
        final.append(ls)
        ls = []
        
    k_dic = {}
    for i in range(len(keyword_list)):
        k_dic[keyword_list[i]] = final[i]
    
    df = pd.DataFrame(k_dic)
    df.index = ['초반', '초중반', '중반', '중후반', '후반']
    
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path, size=18)
    font_name = fm.FontProperties(fname=font_path, size=18).get_name()
    plt.rc('font', family = font_name)

    plt.rcParams['figure.figsize'] = [15, 8]
    plt.plot(df.index, df[keyword_list[0]], marker='o', color='r', )
    plt.plot(df.index, df[keyword_list[1]], marker='*', color='b')
    plt.plot(df.index, df[keyword_list[2]], marker='+', color='y')
    plt.xticks(size = 20)
    plt.yticks(size = 20)


    plt.title('시간대별 키워드', fontsize=30) 


    plt.legend(keyword_list, fontsize=18, loc='best')
    plt.savefig('chart4')
    plt.show()

    
# 화자 집중도 분석 함수
def total_text(texts):
    total_text = len(texts)
    return total_text

def speak_text(dataframe):
    speak_text = dataframe.groupby(by= ['username']).count()
    name_list = list(speak_text.index)
    val_list = list(speak_text['contents'])
    speak_text=list(zip(name_list, val_list))
    return speak_text

def total_keyword(texts, keyword):
    total_keyword = 0
    for i in texts:
        for j in keyword[0]: 
            if j in i:
                total_keyword += 1
    return total_keyword

def speak_keyword(dataframe, keyword):
    dic = {}
    speak_keyword = list(dataframe.groupby(by=['username']))
    for i in speak_keyword:
        dic[i[0]] = list(i[1]['contents'])
    cnt = 0
    name_list = []
    val_list = []
    for key, val in dic.items():
        name_list.append(key)
        for i in dic[key]:
            for j in keyword[0]:
                if j in i:
                    cnt +=1
        val_list.append(cnt)
        cnt = 0
    speak_keyword=list(zip(name_list, val_list))
    return speak_keyword

def concentration(total_text, speak_text, total_keyword, speak_keyword, w):
    speak_text.sort(key = lambda x : x[0])
    speak_keyword.sort(key = lambda x : x[0])
    best_member = {}
    
    for i in range(len(speak_text)):
        concentration = (w * (speak_text[i][1]/total_text) + (1-w) * (speak_keyword[i][1]/total_keyword))*100
        best_member[speak_text[i][0]] = concentration
    
    return best_member


# 불러오기
with open('test2.json') as datafile:
    data = json.load(datafile)
dataframe = pd.DataFrame(data)
dataframe.columns = ['roomid', 'time', 'username', 'contents']      # 이 부분 수정해야할 듯 


# 변수선언
texts = list(dataframe['contents'])
sents = change_sents(texts)
member = tuple(set(dataframe['username']))
keyword_textrank = textrank_key_word(sents, 3)
keyword_prob = prob_key_word(texts, 3)
keyword_list = keyword_textrank[0]
split_text = split_texts(texts, 3)
split_keywords = split_keyword(split_text, 3)


# keyword 별 요약
keyword_dict = keyword_dic(keyword_textrank, texts)

keyword1 = keyword_dict[keyword_textrank[0][0]]
keyword2 = keyword_dict[keyword_textrank[0][1]]
keyword3 = keyword_dict[keyword_textrank[0][2]]

keyword1 = summarizer_text(keyword1, 5)
keyword2 = summarizer_text(keyword2, 5)
keyword3 = summarizer_text(keyword3, 5)

keyword_dict[keyword_textrank[0][0]] = summarizer_text(keyword1, 10)
keyword_dict[keyword_textrank[0][1]] = summarizer_text(keyword2, 10)
keyword_dict[keyword_textrank[0][2]] = summarizer_text(keyword3, 10)


# 화자 잡중도
total_t = total_text(texts)
speak_t = speak_text(dataframe)
total_k = total_keyword(texts, keyword_prob)
speak_k = speak_keyword(dataframe, keyword_prob)
w = 0.5

best_member = concentration(total_t, speak_t, total_k, speak_k, w)
best_member = sorted(best_member.items(), key = lambda item: item[1], reverse=True)
best_member = dict(best_member)


# 시각자료
wordcloud(texts)
chart(split_keywords)
chart2(texts, keyword_list)


# json
sample = {
    "date": "2020.12.29",
    "author": "도담도담(https://dodamdodam.site)",
    "member": member,
    "keywords": keyword_list,
    "summary": keyword_dict,
    "grade": best_member,
    "record": [
            {
            "roomid": "6566259168927733",
            "time": "17:06:56",
            "userid": "bf226qv1qdp",
            "username": "배민진",
            "contents": "테스트 시작하겠습니다"
            },
           {
            "roomid": "6566259168927733",
            "time": "17:06:56",
            "userid": "bf226qv1qdp",
            "username": "오재열",
            "contents": "테스트 시작하겠습니다"
            },
    ]
}