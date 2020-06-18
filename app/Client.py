import cv2, base64, requests
import numpy as np
import math
from datetime import datetime

face_cascade = cv2.CascadeClassifier('Gui\cascades\data\haarcascade_frontalface_alt2.xml')

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

URL = "http://192.168.1.81:5000/"

printTaken = -1


def sendPrintimg(frame):
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    jpg_as_text = base64.b64encode(frame)
    json = {'image': jpg_as_text, 'studentName': 'sara',
            'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
    postRequest = requests.post(url=URL + '/receiveImage', data=json)



# Capturing video from webcam:
cap = cv2.VideoCapture(0)

currentFrame = 0
midcenter = 0
x1 = 0
y1 = 0
w1 = 0
h1 = 0

while True:
    if cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        if len(faces) > 0:
            if printTaken == 1:
                sendPrintimg(frame)
            printTaken = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
        else:
            if printTaken == 0:
                sendPrintimg(frame)
                printTaken = 1
        # Handles the mirroring of the current frame
        frame = cv2.flip(frame, 1)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            break

        # To stop duplicate images
        currentFrame += 1
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
