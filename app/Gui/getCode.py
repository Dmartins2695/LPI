import math
import sys

import base64
import cv2
import numpy as np
import requests
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi

URL = "http://192.168.1.134:5000"

class CodePage(QMainWindow):
    def __init__(self):
        super(CodePage, self).__init__()
        loadUi('test.ui', self)
        self.btn1.clicked.connect(self.getCode)

    def getCode(self):
        roomCode = self.code.text()
        print(roomCode)
        json = {'roomCode': roomCode}
        postRequest = requests.post(url=URL + '/receiveCode', data=json)
        postJason= postRequest.json()
        if postJason['code']== 'sucess':
            self.code.clear()
            print('enter room')
        elif postJason['code']== 'error':
            self.code.clear()
            print(postJason['message'])


app = QApplication(sys.argv)
widget = CodePage()
widget.show()
sys.exit(app.exec_())
