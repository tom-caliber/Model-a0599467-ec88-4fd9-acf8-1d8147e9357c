__author__ = 'mohak'

from flask import Flask, jsonify, request
from pan_validation import PANValidation
import json
from skimage import io 
import numpy as np

app = Flask(__name__)


@app.errorhandler(400)
def bad_request():
    message = {'status': 400, 'message': 'Bad Request: ' + request.url + ' JSON format: <img_url> <pan_text>'}
    resp = jsonify(message)
    print(request)
    resp.status_code = 400
    return resp

@app.route('/healthz', methods=['GET'])
def healthz():
    message = {"status": "I'm alive!!!"}
    response = jsonify(message)
    response.status_code = 200
    return response

@app.route("/predict", methods=['POST'])
def pan_validate_server():
    try:
        pan_validator = PANValidation('rsc/haarcascade_frontalface_default.xml')
        data_json = request.get_json()
        print(data_json)
        img_url=data_json['img_url']
        pan_txt = data_json['pan_txt']
        img = io.imread(img_url)
        pan_dict = pan_validator.validate_pan(img, pan_txt)
        return json.dumps(str("success"))

    except Exception as e:
        print(e)
        return (bad_request())

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    #curl - i - H "Content-Type: application/json" - X POST - d '{"img_url":"/home/dell/Documents/sygmoid/syg_pan/img", "pan_txt": "AWIPP1078K"}' http: // localhost:5000 / pan_validate_server

