from fpdf import FPDF
import matplotlib.pyplot as plt
import json
import pandas as pd

class PDF(FPDF):
	def read_json(self, roomid):
		with open("meeting/"+roomid+'/json_file.json', 'r') as file:
			self.data = json.load(file)
		

	def main_page_static(self):
		#page 1 lines
	#         self.add_font('NanumGothic', 'Bold','/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf', uni=True)
	#         self.add_font('NanumGothic', '','/usr/share/fonts/truetype/nanum/NanumGothic.ttf', uni=True)   
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
			st+="["+s['time']+"] "+s['userid']+": "+s['contents']+"\n"       
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
			
			
	# def dodam(self,dodam):
	#     self.set_xy(70.0,100.0)
	#     self.image(dodam,  link='', type='', w=800/10, h=800/10)
		
		
		
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

			
		
						

	# # default
	# pdf = PDF(orientation='P', unit='mm', format='A4')

	# roomid=pdf.read_json('test')

	# pdf.main_page_static()

	# pdf.main_page_dynamic()

	# pdf.second_page()

	# pdf.third_page()

	# pdf.final_page()
	# file_name=roomid+'.pdf'
	# pdf.output(file_name,'F')
