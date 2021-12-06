import cv2

# Haar-like特徴分類器の読み込み
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
lefteye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')

# 保存パスの指定
save_path = "./images"

def main():
  # カメラのキャプチャを開始
  cam = cv2.VideoCapture(0)
  img = get_image(cam)

  while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
      cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
      # regions of interest
      roi_gray = gray[y:y + h, (x+w)/2:x + w]
      roi_color = img[y:y + h, (x+w)/2:x + w]
      eye = 0
      openEye = 0
      counter = 0
      openEyes = eye_cascade.detectMultiScale(roi_gray)
      AllEyes = lefteye_cascade.detectMultiScale(roi_gray)
      for (ex, ey, ew, eh) in openEyes:
        openEye += 1
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0),2)

      for (ex, ey, ew, eh) in AllEyes:
        eye += 1
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 40),2)

      if (openEye != eye):
        print ('alert')
    
    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
      break

    cap.release()
    cv2.destroyAllWindows()

    # フレームの初期化 --- (*1)
    img1 = img2 = img3 = get_image(cam)
    th = 300
    num = 1
    while True:
      # Enterキーが押されたら終了
      if cv2.waitKey(1) == 13: break
      # 差分を調べる --- (*2)
      diff = check_image(img1, img2, img3)
      # 差分がthの値以上なら動きがあったと判定 --- (*3)
      cnt = cv2.countNonZero(diff)
      if cnt > th:
        print("カメラに動きを検出")
        # 写真を画像 --- (*4)
        cv2.imwrite(save_path + str(num) + ".jpg", img3)
        num += 1
      # 比較用の画像を保存 --- (*5)
      img1, img2, img3 = (img2, img3, get_image(cam))

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 顔を検知
    faces = face_cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
      # 検知した顔を矩形で囲む
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
      # 顔画像（グレースケール）
      roi_gray = gray[y:y+h, x:x+w]
      # 顔ｇ増（カラースケール）
      roi_color = img[y:y+h, x:x+w]
      # 顔の中から目を検知
      eyes = eye_cascade.detectMultiScale(roi_gray)
      for (ex,ey,ew,eh) in eyes:
        # 検知した目を矩形で囲む
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
      cv2.imwrite(save_path + str(num) + ".jpg", faces)
    # 何かキーを押したら終了
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# カメラから画像を取得する
def get_image(cam):
    img = cam.read()[1]
    img = cv2.resize(img, (600, 400))
    return img
main()



