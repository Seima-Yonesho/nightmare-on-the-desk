import cv2

# Haar-like特徴分類器の読み込み
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

# 保存パスの指定
save_path = "./"
def main():
    # カメラのキャプチャを開始
    cam = cv2.VideoCapture(0)
    # フレームの初期化 --- (*1)
    img1 = img2 = img3 = get_image(cam)
    th = 300
    num = 1
    while True:
        # Enterキーが押されたら終了
        if cv2.waitKey(1) == 13: break
        
            cv2.imshow('PUSH ENTER KEY', diff)
        # 比較用の画像を保存 --- (*5)
        img1, img2, img3 = (img2, img3, get_image(cam))
    # 後始末
    cam.release()
    cv2.destroyAllWindows()

# カメラから画像を取得する
def get_image(cam):
    img = cam.read()[1]
    img = cv2.resize(img, (600, 400))
    return img
main()

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

# 画像表示
cv2.imshow('img',img)

# 何かキーを押したら終了
cv2.waitKey(0)
cv2.destroyAllWindows()