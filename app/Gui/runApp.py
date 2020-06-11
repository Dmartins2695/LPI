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

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('test.ui', self)
        self.btn1.clicked.connect(self.getCode)

    def getCode(self):
        roomCode = self.code.text()
        print(roomCode)
        json = {'roomCode': roomCode}
        postRequest = requests.post(url=URL + '/receiveCode', data=json)
        reponse = requests.get(url=URL+'/check')
        if reponse.status_code == 200:
            print('entrei na room')
        else:
            print('Não entrei an room')


app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
