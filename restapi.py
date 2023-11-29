"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
from PIL import Image
import pandas as pd
import json

import torch
from flask import Flask, request

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5"


@app.route("/")
def hello():
    return "선우형 /v1/object-detection/yolov5으로 들어가"

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"] #요청받은 이미지
        image_bytes = image_file.read() 
        img = Image.open(io.BytesIO(image_bytes)) #열기
        results = model(img, size=640) # 이미지축소
        print(type(results.pandas()))
        print(type(results.pandas().xyxy[0]))
        print(results.pandas().xyxy[0])
        print("hi\n")
        print(results.pandas().xyxy[0][results.pandas().xyxy[0]['confidence'] >= 0.55])
        clean = results.pandas().xyxy[0][results.pandas().xyxy[0]['confidence'] >= 0.7]
        print(clean)
        name_counts = clean['name'].value_counts().reset_index()
        name_counts.columns = ['name', 'count']
        image_width = 1800
        image_height = 2800
        total_image_area = image_width * image_height

        # 각 바운딩 박스의 넓이 계산
        clean['box_area'] = (clean['xmax'] - clean['xmin']) * (clean['ymax'] - clean['ymin'])

        # 바운딩 박스들의 넓이의 합 계산
        total_box_area = clean['box_area'].sum()

        # 바운딩 박스들의 넓이의 합이 이미지 전체 넓이의 몇 퍼센트인지 계산
        box_area_percentage = (total_box_area / total_image_area) * 100

        # 새로운 데이터프레임 생성
        new_clean = pd.DataFrame()

        if box_area_percentage > 50:
            new_clean['Status'] = ['traffic']
        elif box_area_percentage > 35:
            new_clean['Status'] = ['nomal']
        else:
            new_clean['Status'] = ['no_traffic']
        json1 = name_counts.to_json(orient='records')
        json2 = new_clean.to_json(orient='records')

        # JSON 객체로 변환
        json_obj1 = json.loads(json1)
        json_obj2 = json.loads(json2)

        # 두 JSON 객체를 하나의 딕셔너리에 담기
        combined_json = {'type': json_obj1, 'traffic': json_obj2}

        # 딕셔너리를 JSON 형태의 문자열로 변환
        
        new_format = {}

        # type 필드 처리
        for item in combined_json['type']:
            new_format[item['name']] = item['count']

        # traffic 필드 처리
        new_format['traffic'] = combined_json['traffic'][0]['Status']
        if new_format['traffic'] == 'no_traffic':
            new_format['traffic'] = 0
        elif new_format['traffic'] == 'no_traffic':
            new_format['traffic'] = 1
        else:
            new_format['traffic'] = 2


        final_json = json.dumps(new_format)
        print(new_clean)
        print(results)

        return final_json #json변환후 리턴

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing yolov5 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    parser.add_argument('--model', default='yolov5s', help='model to run, i.e. --model yolov5s')
    args = parser.parse_args()

    # model = torch.hub.load('ultralytics/yolov5', args.model)
    model = torch.hub.load("ultralytics/yolov5", 'custom', 'drone.pt', force_reload=True, skip_validation=True)
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
