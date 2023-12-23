<img width="1440" alt="1234" src="https://github.com/urinaner/drone-restapi/assets/27186972/6c7cb2ad-21c1-4d8f-b8f6-3b69e12e33a5">
## Rest API
혼잡도 REST API
도로지면 계산 후 차지 비율 반환

실행방법
----------------------------------------------------------------------------------------------
python3 restapi.py --port 1234 --model drone 

* `python3 -m venv venv`
* `source venv/bin/activate`
* `(venv) $ pip install -r requirements.txt`
* `(venv) $ python3 restapi.py --port 1234`

Then use [curl](https://curl.se/) to perform a request:

`$ curl -X POST -F image=@tests/zidane.jpg 'http://localhost:1234/v1/object-detection/yolov5'`
<img width="848" alt="스크린샷 2023-12-23 오후 11 53 03" src="https://github.com/urinaner/drone-restapi/assets/27186972/c61039cd-9ab9-4ca6-b91c-a902e9d1b249">
