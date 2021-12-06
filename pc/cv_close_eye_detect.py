# -*- coding: utf-8 -*-
import cv2
import time
import requests
import os
import json
import base64
from slacker import Slacker
eye_cascPath = '../haarcascade_eye_tree_eyeglasses.xml'  #eye detect model
face_cascPath = '../haarcascade_frontalface_alt.xml'  #face detect model
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)

os.environ['ACCESS_URL'] = "http://c38b-219-75-227-237.ngrok.io"
os.environ['USER'] = "うんぺろ"
os.environ['SAVE_PATH'] = "../images/"
os.environ['TOKEN'] = "xoxb-2817777618657-2828924448848-onO5o3l4Stn2y9yD5iTV4Jv1"
os.environ['CHANNEL'] = 'random'

def eyeDetect(len_eyes):
  global cnt
  global sleepFlg
  # 目を閉じているか判定
  if len(len_eyes) == 0:
    cnt += 1
  else:
    sleepFlg = False
    cnt = 0
  return

def sleepDetect(frame_tmp):
  global cnt
  global num
  global sleepFlg
  # payload = {'name': os.environ['USER']}
  # 目を2秒以上閉じていると画像を保存
  if cnt > 10 and sleepFlg == False:
    print('sleep!!')
    sleepFlg = True
    image = os.environ['SAVE_PATH'] + str(num) + ".jpg"
    cv2.imwrite(image, frame_tmp)
    message = os.environ["USER"] + 'が眠りに落ちたようだ。'
    # # 画像ファイルを開いてbase64に変換
    # with open(image, 'br') as f1:
    #   img_base64 = base64.b64encode(frame_tmp).decode('utf-8')

    # payload = {
    #   'name' : os.environ['USER'],
    #   'image' : img_base64
    # }
    # res = requests.post(os.environ["ACCESS_URL"] + '/sleep', data=json.dumps(payload))

    slackBot(message, True)

  return

def sleepLength():
  global sleepCnt
  global sleepFlg
  # payload = {'name': os.environ['USER']}
  # if sleepFlg == True:
  #   sleepCnt += 1
  # elif sleepCnt > 0:
  #   requests.post(os.environ["ACCESS_URL"] + '/wakeup', data=json.dumps(payload))
  #   sleepCnt = 0
  if sleepFlg == True:
    sleepCnt += 1
  elif sleepCnt > 0:
    print('Wake Up!!')
    message = os.environ['USER'] + 'が眠りから覚めたようだ。'
    slackBot(message, False)
    sleepCnt = 0
  return

def slackBot(message, fileExist):
  token = os.environ['TOKEN']
  channel = os.environ['CHANNEL']

  if fileExist == True:
    file = os.environ['SAVE_PATH'] + '1.jpg'
    files = {'file': open(file, 'rb')}
    param = {
      'token': token,
      'channels': channel,
      'filename': 'evidence',
      # Botのメッセージ
      'initial_comment': message,
      # Slack上のタイトル
      'title': "証拠だ！"
    }
    requests.post(url="https://slack.com/api/files.upload", params=param, files=files)
  else:
    param = {
      'token': token,
      'channel': channel,
      # Botのメッセージ
      'text': message,
    }
    requests.post('https://slack.com/api/chat.postMessage', headers={'Content-Type': 'application/json'}, params=param)

def main():
  cap = cv2.VideoCapture(0)
  while True:
    ret, img = cap.read()
    if ret:
      frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      # Detect faces in the image
      faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags = cv2.CV_HAAR_SCALE_IMAGE
      )
      # print("Found {0} faces!".format(len(faces)))
      if len(faces) > 0:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
          cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
          frame_tmp = img[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1, :]
          frame = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]:1]
          eyes = eyeCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            # flags = cv2.CV_HAAR_SCALE_IMAGE
          )
          eyeDetect(eyes)
          frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
          cv2.imshow('Face Recognition', frame_tmp)
          sleepDetect(frame_tmp)
          sleepLength()
        waitkey = cv2.waitKey(1)
        if waitkey == ord('q') or waitkey == ord('Q'):
          cv2.destroyAllWindows()
          break
      time.sleep(0.1)

if __name__ == '__main__':
  cnt = 0
  sleepFlg = False
  num = 1
  sleepCnt = 0
  main()
