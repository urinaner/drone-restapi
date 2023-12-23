
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
![Uploading 1234.png…]()
