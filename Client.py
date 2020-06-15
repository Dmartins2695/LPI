import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import base64
import requests
import cv2, base64, requests
import numpy as np
import math

face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')
perfil_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_profileface.xml')

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

URL = "http://192.168.1.81:5000/"
# Capturing video from webcam:
cap = cv2.VideoCapture(0)

currentFrame = 0
midcenter=0
x1=0
y1=0
w1=0
h1=0
while True:
    if cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        profile = perfil_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
                if(x+x1>x+50 and x-x1<x-50 and y+y1>y+30 and y-y1<y-30):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (100, 0, 100), 1)

        for (px, py, pw, ph) in profile:
            if (len(profile) != 0):
                cv2.rectangle(frame, (px, py), (px + pw, py + ph), (0, 255, 0), 1)

        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, 1)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            break
        elif k % 256 == 32:
            # Sends Post to save image of the current frame in jpg file in server
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            jpg_as_text = base64.b64encode(frame)
            print("jpg_as_text")
            print(jpg_as_text)
            json = {'image': jpg_as_text}
            postRequest = requests.post(url=URL+'receiveImage', data=json)
        # To stop duplicate images
        currentFrame += 1
        faces1 = faces
        print("FACE1",faces1)
        if len(faces1)!=0:
            a=faces1
            array=a.tolist()
            print(type(array))
            x1=array[0]
            # y1=array[1]
            w1=array[2]
            h1=array[3]
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(('192.168.1.124', 8485))
#connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

URL="http://192.168.1.99:5000/receiveImage"

frame = cv2.imread("C:\\Users\plato\PycharmProjects\Client\\venv\App\\assets\mooncompositemain-800x800.jpg")
result, frame = cv2.imencode('.jpg', frame, encode_param)
jpg_as_text = base64.b64encode(frame)
print("jpg_as_text")
print(jpg_as_text)
json={'image':jpg_as_text}
r = requests.post(url = URL, data = json)



    #data = zlib.compress(pickle.dumps(frame, 0))
   # data = pickle.dumps(frame, 0)
    #size = len(data)


   # print("{}: {}".format(img_counter, size))
   # client_socket.sendall(struct.pack(">L", size) + data)
    #img_counter += 1

cam.release()