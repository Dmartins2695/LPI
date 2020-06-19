import base64
import sys
from datetime import datetime

import cv2
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
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
        self.printTaken = -1
        self.disableCam = 0
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.btn_disable.clicked.connect(self.closeCvCam)
        self.btn_enable.clicked.connect(self.openCvCam)
        self.btn_leave.clicked.connect(self.leave)

    def sendPrintimg(self, frame):
        result, frame = cv2.imencode('.jpg', frame, self.encode_param)
        jpg_as_text = base64.b64encode(frame)
        json = {'image': jpg_as_text, 'studentName': credentials[0],
                'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
        postRequest = requests.post(url=URL + '/receiveImage', data=json)

    # LPI18062020203648
    def openCvCam(self):
        face_cascade = cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        json = {'studentName': credentials[0],
                'enable': 1, 'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
        postRequest = requests.post(url=URL + '/receiveEnable', data=json)
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10)
                if len(faces) > 0:
                    if self.printTaken == 1:
                        self.sendPrintimg(frame)
                    self.printTaken = 0
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
                else:
                    if self.printTaken == 0:
                        self.sendPrintimg(frame)
                    self.printTaken = 1
                frame = cv2.flip(frame, 1)
                cv2.imshow('frame', frame)
                k = cv2.waitKey(1)
                if k % 256 == 27 or self.disableCam == 1:
                    self.disableCam = 0
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        cv2.destroyAllWindows()

    def closeCvCam(self):
        self.disableCam = 1
        json = {'studentName': credentials[0],
                'disable': 1, 'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
        postRequest = requests.post(url=URL + '/receiveDisable', data=json)

    def leave(self):
        json = {'studentName': credentials[0],
                'logout': 0, 'timestamp': datetime.now().strftime("%Hh%Mm%Ss")}
        postRequest = requests.post(url=URL + '/receiveLeave', data=json)
        self.close()


app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
