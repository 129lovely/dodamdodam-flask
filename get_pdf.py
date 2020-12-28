from math import log
from collections import Counter
from konlpy.tag import Mecab
from textrank import KeysentenceSummarizer
from textrank import KeywordSummarizer
from python_utils import logger
from wordcloud import WordCloud
from keras.models import model_from_json
from tensorflow.keras.utils import to_categorical

from fpdf import FPDF
import matplotlib.pyplot as plt
import json
import pandas as pd
import pickle
import pandas as pd
import numpy as np                                                       
import os, re, time, csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import operator

mecab = Mecab()

class PDF(FPDF):
    def read_json(self,roomid):
        with open("meeting/"+roomid+'/json_file_mod.json', 'r') as f:
            self.data = json.load(f)
    #             print(json.dumps(self.data,indent="\t") )
    #         self.dataframe = pd.DataFrame(json_data)
    #         print(self.data)
        


    def main_page_static(self):
        #page 1 lines
    #         self.add_font('NanumGothic', 'Bold','./font/NanumGothicBold.ttf', uni=True)
    #         self.add_font('NanumGothic', '','./font/NanumGothic.ttf', uni=True)   
        self.add_font('NanumSqure', 'B','./font/NanumSquareB.ttf', uni=True)
        self.add_font('NanumSqure', 'EB','./font/NanumSquareEB.ttf', uni=True)
        self.add_font('NanumSqure', 'L','./font/NanumSquareL.ttf', uni=True)
        
        self.add_font('tvN', 'B','./font/tvN 즐거운이야기 Bold.ttf', uni=True)
        self.add_font('tvN', 'L','./font/tvN 즐거운이야기 Light.ttf', uni=True)
        self.add_font('tvN', 'M','./font/tvN 즐거운이야기 Medium.ttf', uni=True)
        self.add_page(first=True)


        #page 1 title 도담도담
        self.dodam='도담도담'
        self.set_xy(70.0,1)
        self.set_font('tvN', 'B', 52)
        self.set_text_color(255, 185, 0)
        self.multi_cell(w=50.0, h=12.0, align='C', txt=self.dodam[:2], border=0)
        self.set_xy(90,1)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=50.0, h=12.0, align='C', txt=self.dodam[2:], border=0)


        
    def main_page_dynamic(self,date='일시: 2020.01.01',participantsList=['김수경','김영욱','박성건','배민진','오재일','최인경']):
                                                         

        #일시
        self.date=self.data['date']
        st="일시: "+ self.date
        self.text(st,'NanumSqure','B',15,6,30)
        
        
        #작성자
        self.auth=self.data['author']
        st="작성자: " + self.auth
        self.text(st,'NanumSqure','B',15,6,50)
    #         self.partList=participantsList
        
        #참석자
        self.partList=self.data["member"]
        st="참석자: "
        for i in self.partList:
            st+=i+","
        st=st.rstrip(',')
        self.text(st,'NanumSqure','B',15,6,70)
        
        
        
        #00.00회의 키워드
        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        self.line(10,120,200,120) # top one
        self.line(10,250,200,250) # bottom one
        self.line(10,120,10,250) # left one
        self.line(200,120,200,250) # right one
        self.ddyy="< "+str(self.date)[:5]
        self.ddyy="< " + self.date[5:]
        self.text(self.ddyy,'NanumSqure','B',20,10,105)
        self.text('회의 핵심 키워드 > ','NanumSqure','B',20,40,105)

        
        
                #워드 클라우드
        
    #         self.keywordList=[]
        self.keywordList=self.data['keywords']
        self.keywords1=""
        for i in self.keywordList:
            self.keywords1+=i+","
        self.keywords1=self.keywords1.rstrip(',')
        
        self.text(' - 핵심키워드: ','NanumSqure','B',18,10,125)
        self.text(self.keywords1,'NanumSqure','B',18,50,125)
        self.text(' * Wordcloud','NanumSqure','L',18,10,135)
            
        self.keywords1.rstrip(',')
            

        
        #wc이미지
    #         self.wcpath='./image/wordcloud.png'
        self.wc_path=self.data['wordcloud']
        self.set_xy(50.0,140)
        self.image(self.wc_path,  link='', type='', w=1000/10, h=1000/10)
        



    #####################page2######################################
    def second_page(self):
        #키워드별 주요 내용
        self.add_page()
        self.dodam='□ 키워드 별 주요 내용'
        self.set_xy(6.,self.get_y())
        self.set_font('NanumSqure', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=100.0, h=20.0, align='ㅣ', txt=self.dodam)

        
        self.keywordList=self.data['summary']
    #         print(self.keywordList)
        self.i=0
        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        for keyword,list3 in self.keywordList.items():
    #             print(self.i)
            y1=self.get_y()
            self.line(10,self.get_y(),200,self.get_y()) # top one
            self.text('{}. keyword : {}'.format(self.i+1,keyword),'NanumSqure','B',18,self.get_x(),self.get_y())
            self.line(10,self.get_y(),200,self.get_y()) # bottom one
            st=""
            self.i+=1
            for idx,s in enumerate(list3):
                st+= str(idx+1)+"."+s+'\n'
            self.line(10,self.get_y(),200,self.get_y()) # top one
            self.text(st,'NanumSqure','L',12,10,self.get_y()+(self.i-1))
            self.line(10,self.get_y(),200,self.get_y()) # top one
            self.line(10,y1,10,self.get_y()) # left one
            self.line(200,y1,200,self.get_y()) # right one
            
        
        for idx,keyword in enumerate(self.keywordList):
            pass
        
        #시간대별 그래프
        self.dodam='＊ 시간대별 주요키워드'
        self.set_xy(6,self.get_y()+5)
        self.set_font('NanumSqure', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=100.0, h=0, align='ㅣ', txt=self.dodam, border=0)
        self.flow_chart=self.data['chart4']
        self.set_xy(6.0,self.get_y()+5)
        self.image(self.flow_chart,  link='', type='', w=1080/6, h=576/8)
        
        
        
    def third_page(self):
        self.add_page()
        #전체 회의록 요약
        self.dodam='□ 전체 회의록 요약'
        self.set_xy(6.0,self.get_y()+5)
        self.set_font('NanumSqure', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=100.0, h=20.0, align='ㅣ', txt=self.dodam)

        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        
        self.line(10,self.get_y(),200,self.get_y()) # top one
        strl=self.data['total_summary']
        st=""
        y1=self.get_y()
        for i in strl:
            st+=i+" "
            
        self.text(st,'NanumSqure','l',12,12,self.get_y())
        self.line(10,self.get_y(),200,self.get_y()) # bottom one
        self.line(10,y1,10,self.get_y()) # left one
        self.line(200,y1,200,self.get_y()) # right one
        
        st="*Ko-BART를 활용한 추상적(Abstractive) 요약"
        self.text(st,'NanumSqure','l',12,115,self.get_y())
        
        
        #회의 참여도
        self.dodam='□ 회의 참여도'
        self.set_xy(6.0,self.get_y()+5)
        self.set_font('NanumSqure', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=100.0, h=20.0, align='ㅣ', txt=self.dodam)
        
        #박스
        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        y=self.get_y()+5
        self.line(40,y,170,y) # top one

        
        #집중도
        self.grade=self.data['grade']
        y2=self.get_y()+5
        
        i=1
        s1= " 열정맨!!"
        s2= " 집중맨!!"
        s3= " 집중좀!!"
        s4= " 참여좀!!"
        
        for key,val in self.grade.items():
                if i ==1:
                    s=s1
                elif i == 2:
                    s=s2
                elif i == 3:
                    s=s3
                else:
                    s=s4
                        
                    
                self.text(key+": "+str(val)[:5]+"점,  당신은 "+s,'NanumSqure','l',18,43,y2+10)
                y2=self.get_y()
                i+=1

        
        
        
        
        
        self.line(40,y2+10,170,y2+10) # bottom one
        self.line(40,y,40,y2+10) # left one
        self.line(170,y,170,y2+10) # right one
        st="*참여도는 발화문장의 전체 횟수와 키워드 발화 횟수로 계산됩니다."
        self.text(st,'NanumSqure','l',12,80,y2+10)

    def final_page(self):
        self.add_page()
        #전체 회의록 요약
        self.dodam='□ 전체 회의록'
        self.set_xy(6,self.get_y()+5)
        self.set_font('NanumSqure', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=100.0, h=20.0, align='ㅣ', txt=self.dodam)

        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        
        self.line(10,self.get_y(),200,self.get_y()) # top one
        self.recd=self.data['record']
    #         print(self.recd)
        st=""
        y1=self.get_y()
        for s in self.recd:
            self.set_line_width(0)
            self.set_draw_color(0, 0, 0)
            st+="["+s['time']+"] "+s['username']+": "+s['contents']+"\n"             
        self.text(st,'NanumSqure','l',12,12,self.get_y())
        
        self.set_line_width(0)
        self.set_draw_color(0, 0, 0)
        self.line(10,self.get_y(),200,self.get_y()) # bottom one
    #         self.line(10,y1,10,self.get_y()) # left one
    #         self.line(200,y1,200,self.get_y()) # right one
        st="-END-            A2 도담도담"
        self.text(st,'NanumSqure','l',12,90,self.get_y()+10)
        
        
        
            
        

    #     def draw_rect()
        



    def set_title(self,title):
        self.set_xy(15.0,5.0)
        self.set_font('NanumSqure', 'B', 24)
        self.set_text_color(255, 215, 0)
        self.cell(w=100,h=20.0, align='L', txt=title)
        
    def text(self,text,font,type,size,x,y):
        self.set_xy(x,y)    
        self.set_text_color(0.0, 0.0, 0.0)
        self.set_font(font,type , size)
        self.multi_cell(0,10,text,border=0)
        
    def text_file(self,text_file,font,type,size,x,y):
        with open(text_file,'rb') as f:
            txt=f.read().decode('utf-8')
        self.set_xy(x,y)    
        self.set_text_color(0.0, 0.0, 0.0)
        self.set_font(font,type , size)
        self.multi_cell(0,10,txt)
        
    def wordCloud(self,plt,text,text2):
        self.set_xy(10.0,30)
        self.image(plt,  link='', type='', w=1000/10, h=1000/10)
        self.set_xy(10,10)
        self.set_font('NanumSqure', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.multi_cell( 0,10,txt=text, border=0)

        self.set_xy(120,30)
        self.set_font('NanumSqure', '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell( 0,10,txt=text2, border=0)
            
    def keyWord(self,chart1,chart2,chart3,text,text2):
        self.set_xy(10,170)
        self.image(chart1,  link='', type='', w=432/4.9, h=228/4.9)

        self.set_xy(110,170)
        self.image(chart2,  link='', type='', w=432/4.9, h=228/4.9)

        self.set_xy(10,230)
        self.image(chart3,  link='', type='', w=432/4.9, h=228/4.9)

        self.set_xy(10,150)
        self.set_font('NanumSqure', 'B', 24)
        self.set_text_color(0, 0, 0)
        self.multi_cell( 0,10,txt=text, border=0)

        self.set_xy(110,220)
        self.set_font('NanumSqure', '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell( 0,0,txt=text2, border=0)
            
            
    def dodam(self,dodam):
        self.set_xy(70.0,100.0)
        self.image(dodam,  link='', type='', w=800/10, h=800/10)
        
        
        
    def add_page(self,first=False):
        super().add_page()
    #         print("addpage")
        
        if first==True:
            self.set_line_width(2)
            self.set_draw_color(255, 185, 0)
            self.line(5,5,80,5) # top one
            self.line(130,5,205,5.) # top two
            self.line(5,292,205,292) # bottom one
            self.line(5,5,5,292) # left one
            self.line(205,5,205,292) # right one
        else:
            self.set_line_width(2)
            self.set_draw_color(255, 185, 0)
            self.line(5,5,205,5) # top one
            self.line(5,292,205,292) # bottom one
            self.line(5,5,5,292) # left one
            self.line(205,5,205,292) # right one

            
        
                        

                    
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
    keywords = keyword_extractor.summarize(sent, topk=n)
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
    len_texts = len(text)

    if (len_texts % n) == 0:
        number = len_texts//n
    else:
        number = len_texts//n + 1

    for i in range(n):
        if i == n-1:
            split_texts.append(text[(i*number):])
        else:
            split_texts.append(text[(i*number):(i+1)*number])
    return split_texts


# 시간대별 키워드 추출 함수
def split_keyword(split_text, n):
    split_keyword = []

    for i in range(len(split_text)):
        split_keyword.append((prob_key_word(split_text[i], n)[0], prob_key_word(split_text[i], n)[1]))
    return split_keyword


# WordCloud 생성 함수
def Wordcloud(texts, roomid):
    font_path = "./font/NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path, size=18)
    file_name = 'meeting/' + roomid + '/wordcloud.png'
    wc = WordCloud(font_path = "./font/NanumGothic.ttf",
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
    plt.close()

# chart 생성 함수
def Chart1(split_keyword, roomid):
    font_path = "./font/NanumGothic.ttf"
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
        file_name = 'meeting/' + roomid + '/chart' + str((i+1))
        title_name = title[i]
        plt.figure(figsize=(6.4, 4.8))
        plt.bar(x, cnt)
        plt.xticks(x, keyword, fontproperties=fontprop)
        plt.xticks(size = 20)
        plt.yticks(size = 20)
        plt.ylim([0, MAX])
        plt.title(title_name, fontproperties=fontprop, size = 30)
        plt.savefig(file_name)
        plt.show()
        plt.close()

    
# chart2 생성 함수
def Chart2(texts, keyword_list, roomid ):
    n=5
    split_text1 = split_texts(texts, n)
    cnt = 0
    ls = []
    final = []
    file_name = 'meeting/' + roomid + '/chart4'
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

    font_path = "./font/NanumGothic.ttf"
    fontprop = fm.FontProperties(fname=font_path)
    # font_name = fm.FontProperties(fname=font_path, size=18).get_name()
    # plt.rc('font', family = font_name)
    plt.rc('font', family = font_path)
    plt.rcParams['figure.figsize'] = [15, 8]
    plt.plot(df.index, df[keyword_list[0]], marker='o', color='r', )
    plt.plot(df.index, df[keyword_list[1]], marker='*', color='b')
    plt.plot(df.index, df[keyword_list[2]], marker='+', color='y')
    plt.xticks(fontproperties=fontprop, size=20)
    plt.yticks(size = 20)
    plt.title('시간대별 키워드', fontsize=30, fontproperties=fontprop) 
    plt.legend(keyword_list, fontsize=18, loc='best', fontproperties=fontprop)
    plt.savefig(file_name)
    plt.show()
    plt.close()


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

# 폴더 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# 끝점 검출
def word_ngram(sentence, num_gram):
    # in the case a file is given, remove escape characters
    sentence = sentence.replace('\n', ' ').replace('\r', ' ')
    text = list(sentence.split(' '))
    ngrams = [text[x:x+num_gram] for x in range(0, len(text))]
    return tuple(ngrams)

def make_dataset(text):
    data_set = []
    unigram = word_ngram(text,1)
    bigram = word_ngram(text,2)

    for i in range(len(text.split())):
        if i == len(text.split())-1:
            data_set.append(unigram[i])
        else:
            data_set.append(unigram[i])
            data_set.append(bigram[i])
    return data_set

def padding(literals):
    for i in literals:
        if len(i) == 1:
            i.append('PAD')    
        
def labeling(text):
    label=[]
    for i in text :
        if i[0].endswith(".")==True:
            label.append('1')
        elif i[0].endswith("?")==True:
            label.append('2')
        else :
            label.append('0')
    return label

def stripstext(texts):
    for i in texts:
        i[0] = i[0].strip(string.punctuation)
        i[1] = i[1].strip(string.punctuation)
        
def unit(text):
    last=[]
    for i in text:
        a =' '.join(i)
        last.append(a)
    return last

def text2seq(vocab, bigram_array):
    bigram_seq = []
    for bigram in bigram_array['data']:
        words = bigram.split(' ')
        seq = []
        for word in words:
            if word in vocab[0]:
                seq.append(vocab[0][word])
            else:
                seq.append(0) # OOV 인 경우 0
        bigram_seq.append(seq)
    return bigram_seq
    
# predict 한 것을 바탕으로 문장 끝점을 bigram_array 에 찍어주는 함수
def make_comma(data,predict):    
    for i in range(len(predict)):
        if predict[i]==1 :
            data[i][0]+=". "
        elif predict[i]==2:
            data[i][0]+="? "
        else :
            data[i][0]+=" "        
                
def make_sentence(data_set1):
    lists = []
    list_sentence=[]
    sentences =""
    for i in data_set1:
        if i[1]=='PAD':
            lists.append(i)    
    for j in lists:
        list_sentence.append(j[0])
    for k in list_sentence:
        sentences += k
    sentences = sentences.strip()
    return sentences


def main(roomid):
    # 모델 불러오기
    json_file = open("model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    loaded_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

    # vocab 불러오기
    with open('vocab.pickle','rb') as handle :
        vocab = pickle.load(handle)
        

    # json 파일 불러오기
    with open("meeting/"+roomid+'/json_file.json') as datafile:
        data = json.load(datafile)
    dataframe = pd.DataFrame(data)

    # 변수선언
    temp = list(dataframe['contents'])
    texts = []

    for i in temp:
        data_set = make_dataset(i)
        padding(data_set)
        label = labeling(data_set)
        labeled_dataset = unit(data_set)
        labeled_dataset = pd.DataFrame(labeled_dataset)
        labeled_dataset.columns = ['data']

        int_dataset = text2seq(vocab, labeled_dataset)
        x_data = np.array(int_dataset)

        predict = loaded_model.predict(x_data)
        y_predict = np.argmax(predict, axis = 1)
        y_predict = list(y_predict)

        make_comma(data_set,y_predict)

        final_text = make_sentence(data_set)
        texts.append(final_text)
        
    sents = change_sents(texts)
    roomid = list(set(dataframe['roomid']))[0]
    member = tuple(set(dataframe['username']))
    keyword_textrank = textrank_key_word(sents, 3)
    keyword_prob = prob_key_word(texts, 3)
    keyword_list = keyword_textrank[0]
    split_text = split_texts(texts, 3)
    split_keywords = split_keyword(split_text, 3)
    dataframe['contents'] = texts   
    data1 = dataframe.to_dict('index')

    data = []
    for val in data1.values():
        data.append(val)
        
        
        
    # 폴더 생성
    createFolder('meeting')
    createFolder('meeting/' + roomid)

    # keyword 별 요약
    keyword_dict = keyword_dic(keyword_textrank, texts)
    keyword1 = keyword_dict[keyword_textrank[0][0]]
    keyword2 = keyword_dict[keyword_textrank[0][1]]
    keyword3 = keyword_dict[keyword_textrank[0][2]]
    keyword1 = summarizer_text(keyword1, 3)
    keyword2 = summarizer_text(keyword2, 3)
    keyword3 = summarizer_text(keyword3, 3)
    keyword_dict[keyword_textrank[0][0]] = keyword1
    keyword_dict[keyword_textrank[0][1]] = keyword2
    keyword_dict[keyword_textrank[0][2]] = keyword3

    # 전체 요약
    total_summary = summarizer_text(texts, 10)

    # 화자 잡중도
    total_t = total_text(texts)
    speak_t = speak_text(dataframe)
    total_k = total_keyword(texts, keyword_prob)
    speak_k = speak_keyword(dataframe, keyword_prob)
    w = 0.5

    # 집중도
    best_member = concentration(total_t, speak_t, total_k, speak_k, w)
    best_member = sorted(best_member.items(), key = lambda item: item[1], reverse=True)
    best_member = dict(best_member)

    # 시각자료
    Wordcloud(texts, roomid)
    Chart1(split_keywords, roomid)
    Chart2(texts, keyword_list, roomid)

    # 이미지 경로
    wordcloud = 'meeting/'+ roomid + '/wordcloud.png'
    chart1 = 'meeting/'+ roomid + '/chart1.png'
    chart2 = 'meeting/'+ roomid + '/chart2.png'
    chart3 = 'meeting/'+ roomid + '/chart3.png'
    chart4 = 'meeting/'+ roomid + '/chart4.png'

    # json
    sample = {
        "date": "2020.12.29",
        "author": "도담도담(https://dodamdodam.site)",
        "roomid" : roomid,
        "member": member,
        "keywords": keyword_list,
        "total_summary" : total_summary,
        "summary": keyword_dict,
        "grade": best_member,
        "wordcloud": wordcloud,
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3,
        "chart4": chart4,
        "record": data
    }

    # json 저장
    josn_path="meeting/" + roomid + "/json_file_mod.json"
    with open(josn_path, "w") as json_file:
        json.dump(sample, json_file)

    # # default
    # pdf = PDF(orientation='P', unit='mm', format='A4')

    # pdf.read_json(roomid)


    # pdf.main_page_static()

    # pdf.main_page_dynamic()

    # pdf.second_page()

    # pdf.third_page()

    # pdf.final_page()

    # output='./meeting/'+roomid+'/dodam.pdf'

    # pdf.output(output,'F')

