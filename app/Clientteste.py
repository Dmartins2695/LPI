
import base64
import sys
from datetime import datetime

import cv2
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

URL = "http://192.168.1.81:5000"

credentials = ['ola', 'daniel', 'tens', 'ai', 'lista']
json = {'eventType': 'test', 'nItems': len(credentials),
        'package0': credentials[0],
        'package1': credentials[1],
        'package2': credentials[2],
        'package3': credentials[3],
        'package4': credentials[4]}
print(json)
x = requests.post(url=URL + '/test', data=json)
