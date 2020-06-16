import math
import sys

import base64
import cv2
import numpy as np
import requests
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi


URL = "http://192.168.1.99:5000"

credentials = []

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        self.myotherWindow = CodePage()
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
            self.myotherWindow.show()
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
        loadUi('codeForm.ui', self)
        self.btn1.clicked.connect(self.getCode)

    def getCode(self):
        roomCode = self.code.text()
        print(roomCode)
        json = {'roomCode': roomCode}
        postRequest = requests.post(url=URL + '/receiveCode', data=json)
        postJason = postRequest.json()
        if postJason['code'] == 'sucess':
            self.code.clear()
            print('enter room')
        elif postJason['code'] == 'error':
            self.code.clear()
            print(postJason['message'])



app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
