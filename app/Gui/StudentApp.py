import math
import sys

import base64
import cv2
import numpy as np
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

URL = "http://192.168.1.99:5000"

credentials = []


class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        self.myRoomWindow = CodePage()
        loadUi('form.ui', self)
        self.btn_login.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.register)

    def login(self):
        username = self.login_username.text()
        password = self.login_pass.text()
        json = {'StudentUser': username, 'StudentPassword': password}
        print(json)
        postRequest = requests.post(url=URL + '/studentLogin', data=json)
        postJason = postRequest.json()

        if postJason['code'] == 'wrong_credentials':
            print('erro login')
        elif postJason['code'] == 'sucess':
            self.login_username.clear()
            self.login_pass.clear()
            credentials.append(username)
            widget.close()
            self.myRoomWindow.show()
            print('login com sucesso')

    def register(self):
        username = self.reg_username.text()
        password = self.reg_pass.text()
        email = self.reg_email.text()
        json = {'StudentUser': username, 'StudentPassword': password, 'StudentEmail': email}
        print(json)
        postRequest = requests.post(url=URL + '/studentRegister', data=json)
        if postRequest.status_code == 200:
            print('Registrada')
            self.reg_username.clear()
            self.reg_pass.clear()
            self.reg_email.clear()
        else:
            print('Erro no registro')


class CodePage(QMainWindow):
    def __init__(self):
        super(CodePage, self).__init__()
        self.myCamWindow = camPage()
        loadUi('codeForm.ui', self)
        self.btn1.clicked.connect(self.getCode)

    def getCode(self):
        roomCode = self.code.text()
        print(roomCode)
        json = {'roomCode': roomCode} #mandar username
        postRequest = requests.post(url=URL + '/receiveCode', data=json)
        postJason = postRequest.json()
        if postJason['code'] == 'sucess':
            self.code.clear()
            print('enter room')
            self.close()
            self.myCamWindow.show()
        elif postJason['code'] == 'error':
            self.code.clear()
            print(postJason['message'])


class camPage(QMainWindow):
    def __init__(self):
        super(camPage, self).__init__()
        loadUi('webCam.ui', self)
        self.cap = cv2.VideoCapture(0)
        self.btn_disable.clicked.connect(self.closeCvCam)
        self.btn_enable.clicked.connect(self.alternative)
        self.btn_leave.clicked.connect(self.leave)

    def alternative(self) :
        pixmap = QPixmap('SuperVisor.jpg')
        self.imgLabel.setPixmap(pixmap)

    def openCvCam(self):
        self.cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
        eye_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')
        perfil_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_profileface.xml')
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        currentFrame = 0
        x1 = 0
        y1 = 0
        while True:
            if self.cap.isOpened():
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                    profile = perfil_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                    for (x, y, w, h) in faces:
                        if x + x1 > x + 50 and x - x1 < x - 50 and y + y1 > y + 30 and y - y1 < y - 30:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                            roi_gray = gray[y:y + h, x:x + w]
                            roi_color = frame[y:y + h, x:x + w]
                            eyes = eye_cascade.detectMultiScale(roi_gray)
                            for (ex, ey, ew, eh) in eyes:
                                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (100, 0, 100), 1)

                    for (px, py, pw, ph) in profile:
                        if len(profile) != 0:
                            cv2.rectangle(frame, (px, py), (px + pw, py + ph), (0, 255, 0), 1)

                    # Handles the mirroring of the current frame
                    frame = cv2.flip(frame, 1)
                    frame = QPixmap(frame)
                    # Display the resulting frame
                    self.imgLabel.setPixmap(frame)
                    k = cv2.waitKey(1)
                    if k % 256 == 27:
                        break
                    elif k % 256 == 32:  # SPACE KEY
                        # Sends Post to save image of the current frame in jpg file in server
                        result, frame = cv2.imencode('.jpg', frame, encode_param)
                        jpg_as_text = base64.b64encode(frame)
                        print("jpg_as_text")
                        print(jpg_as_text)
                        json = {'image': jpg_as_text}
                        postRequest = requests.post(url=URL + 'receiveImage', data=json)
                    # To stop duplicate images
                    currentFrame += 1

    # def displayImage(self, frame, param):
    #     qformat = QImage.Format_Indexed8
    #
    #     if len(frame.shape) == 3:
    #         if (frame.shape[2]) == 4:
    #             qformat = QImage.Format_RGBA8888
    #         else:
    #             qformat = QImage.Format_RGBA8888
    #
    #     frame = QImage(frame, frame.shape[1], frame.shape[0], qformat)
    #     frame = frame.rgbSwapped()
    #     self.imgLabel.setPixmap(QPixmap.fromImage(frame))
    #     self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def closeCvCam(self):
        pixmap = QPixmap('blackscreen.jpg')
        self.imgLabel.setPixmap(pixmap)
        self.cap.release()

    def leave(self):
        pass


app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
