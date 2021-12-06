# -*- coding: utf-8 -*-
import cv2
import time
eye_cascPath = '../haarcascade_eye_tree_eyeglasses.xml'  #eye detect model
face_cascPath = '../haarcascade_frontalface_alt.xml'  #face detect model
faceCascade = cv2.CascadeClassifier(face_cascPath)
eyeCascade = cv2.CascadeClassifier(eye_cascPath)
# faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
# eyeCascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')


cap = cv2.VideoCapture(0)
save_path = "../images/"
cnt = 0
num = 1
sleepFlg = False

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
        # 目を閉じているか判定
        if len(eyes) == 0:
          cnt += 1
        else:
          sleepFlg = False
          cnt = 0
        frame_tmp = cv2.resize(frame_tmp, (400, 400), interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Face Recognition', frame_tmp)
        print(cnt)
        # 目を2秒以上閉じていると画像を保存
        if cnt > 20 and sleepFlg == False:
          print('sleep!!')
          sleepFlg = True
          cv2.imwrite(save_path + str(num) + ".jpg", frame_tmp)
          num += 1

    waitkey = cv2.waitKey(1)
    if waitkey == ord('q') or waitkey == ord('Q'):
      cv2.destroyAllWindows()
      break
  time.sleep(0.1)