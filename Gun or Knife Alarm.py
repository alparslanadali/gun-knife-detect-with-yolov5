import cv2
import torch
import requests
import time



#Localden data girişi en iyi data bu!
# model = torch.hub.load(r"YOUR YOLOv5 path", 'custom', path=r"YOUR DATA MODEL PATH", source='local')
model = torch.hub.load(r"yolov5", 'custom', path=r"yolov5\gunknife.pt", source='local')


#Video Okuma
cap=cv2.VideoCapture(r"4.mp4")

def TelegramSendMessage(class_name):
    "That fonk. have been detect knife or any weapon will be send message."
    #Bot arg.
    TOKEN = "YOUR TOKEN"
    message = f"{class_name} Tespit edildi "+ "\n"+ time.strftime('%H:%M:%S') 
    chat_id = "YOUR CHAT ID"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

    requests.get(url).json()


def TelegramSendImage(frame):
    "That fonk. have been detect knife or any weapon will be image in every 10 second."
    #Bot arg.
    TOKEN = "YOUR TOKEN" 
    chat_id = "YOUR CHAT ID"

    photo=open(frame, 'rb')
    url2 = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
    files = {"photo": photo}

    requests.post(url2,files=files).json()


while True:
    ret,frame = cap.read()
    # Data okunmadığı durumlarda ret 0 döner.

    if ret:

        #Dataya uygun hale getiriliyor.
        frame = cv2.resize(frame,(480,270))

        #model sonuçları alınıyor
        results = model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        #koordinat katsayıları için
        x_shape, y_shape = 480, 270
        #Karedeki espit edilen nesne sayısı

        n = len(labels)
        for i in range(n):
            row = cord[i]
            #Tespit içindeki veri
            class_no = labels[i]
            class_no = int(class_no)
            class_name ="boş"
            if row[4] >= 0.45:
                # tespit edilen noktalar
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                # doğruluk değeri
                conf = float(row[4])
                conf = round(conf,2)
                bgr = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 1)
                #kutu üstüne yazı
                toplam ="TESPIT DEGERI" +str(conf)
                cv2.putText(frame,toplam,(x1,y1-20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),2)
                
                if class_no== 0:
                    class_name = "Knife"
                if class_no== 1:
                    class_name = "Gun"
                TelegramSendMessage(class_name)
                if str(round(time.time()))[-1] == "0":
                    cv2.imwrite("resim.png",frame2)
                    TelegramSendImage(r'resim.png')

    #Resim tekrar işleniyor
    frame2 = cv2.resize(frame,(1366,768))
    
    cv2.imshow("deneme",frame2)
    if cv2.waitKey(60) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()