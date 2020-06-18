import math
import sys
from datetime import datetime
import base64
import cv2
import numpy as np
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi

URL = "http://192.168.1.81:5000"

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
        json = {'roomCode': roomCode, 'studentName': credentials[0]}  # mandar username
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
        self.faceDetected = -1
        self.printTaken = -1
        self.closeFlag = 0
        self.btn_disable.clicked.connect(self.closeCvCam)
        self.btn_enable.clicked.connect(self.openCvCam)
        self.btn_leave.clicked.connect(self.leave)

    def alternative(self):
        pixmap = QPixmap('SuperVisor.jpg')
        self.imgLabel.setPixmap(pixmap)

    def openCvCam(self):
        cv2.namedWindow(credentials[0])
        self.cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        currentFrame = 0
        while True:
            if self.cap.isOpened():
                self.faceDetected = 0 # não encontrou cara
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                if ret:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                    if faces is not None:
                        self.faceDetected = 1 # encontrou cara
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    # Handles the mirroring of the current frame
                    frame = cv2.flip(frame, 1)
                    # Display the resulting frame
                    cv2.imshow(credentials[0], frame)
                    if self.faceDetected == 1 and self.printTaken == 1 or self.faceDetected == 0 and self.printTaken == 0: #tem cara e já tirou print ou nao tem cara e nao tirou print
                        # Sends Post to save image of the current frame in jpg file in server
                        result, frame = cv2.imencode('.jpg', frame, encode_param)
                        jpg_as_text = base64.b64encode(frame)
                        json = {'image': jpg_as_text, 'studentName': credentials[0],
                                'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
                        postRequest = requests.post(url=URL + '/receiveImage', data=json)
                        if self.faceDetected == 0: #se nao tem cara já tirou um print
                            self.printTaken = 1 # 1º print tirado
                    if self.faceDetected == 1: #encontrou cara novamente tira outro print
                        self.printTaken = 0 # segundo print tirado volta ao inicio cara e sem print
                    if self.closeFlag == 1:
                        self.closeFlag = 0
                        break
                    # To stop duplicate images
                    currentFrame += 1
        self.cap.release()
        cv2.destroyWindow(credentials[0])

    def closeCvCam(self):
        self.closeFlag = 1

    def leave(self):
        pass


app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
