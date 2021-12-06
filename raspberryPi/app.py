# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request
import datetime
import os
import json
import cv2
import base64
import numpy as np

os.environ['SAVE_PATH'] = "./images/"
app = Flask(__name__)

@app.route('/sleep', methods=['POST'])
def callback():

  # get request body as text
  body = request.get_data(as_text = True)
  json_body = json.loads(body)
  dt_now = datetime.datetime.now()
  str_date = dt_now.strftime("%m月%d日 %H時%M分")
  print(str_date + ',' + json_body['name'] + 'さんが眠りにつきました。')

  #image upload
  image = os.environ['SAVE_PATH'] + "result.jpg"

  # Imageをデコード
  img_stream = base64.b64decode(json_body['image'])

  # 配列に変換
  img_array = np.asarray(bytearray(img_stream), dtype=np.uint8)

  # open-cv でグレースケール
  img_gray = cv2.imdecode(img_array, 0)

  # 変換結果を保存
  cv2.imwrite(image, img_array)

  return 'OK'

@app.route('/wakeup', methods=['POST'])
def wake_up():

  # get request body as text
  body = request.get_data(as_text = True)
  print(body)
  json_body = json.loads(body)

  print(json_body['name'] + 'さんが夢から覚めました。')
  return 'OK'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
#    app.run()

  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  