from flask import Flask
from flask import request
from flask import make_response, send_file
import get_pdf
import json
import os


app = Flask(__name__) # Flask 클래스 객체화(Flast 웹 애플리케이션)

@app.route("/ping", methods=['GET']) # 엔드포인트 등록
def ping():
	return "pong"


@app.route("/api/report/<roomid>", methods=['POST', 'GET'])
def report(roomid):
	os.makedirs('./meeting/' + roomid, exist_ok=True)

	# json 파일 생성
	if request.method == 'POST':
		with open("meeting/"+roomid+"/json_file.json", "w") as f:
			json.dump(request.get_json(), f)
		return "success"

	# 만든 json 파일 이용해서 파일 가져오기
	if request.method == 'GET':
		filename = roomid + ".pdf"

		get_pdf.main(roomid) # 1차 끝점검출

		pdf = get_pdf.PDF(orientation='P', unit='mm', format='A4')
		pdf.read_json(roomid) # todo: json 파일명
		pdf.main_page_static()
		pdf.main_page_dynamic()
		pdf.second_page()
		pdf.third_page()
		pdf.final_page()
		pdf.output(filename, 'F')
		
		return send_file('./'+filename, attachment_filename='도담도담-회의록_요약.pdf', mimetype='application/pdf', as_attachment=True)