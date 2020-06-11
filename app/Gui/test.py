import math

import base64
import cv2
import numpy as np
import requests
from PyQt5 import QtCore, QtGui, QtWidget


class Ui_MainWindow(object):
    def __init__(self):
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.code = QtWidgets.QLineEdit(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.btn1 = QtWidgets.QPushButton(self.centralwidget)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget.setObjectName("centralwidget")
        self.btn1.setGeometry(QtCore.QRect(330, 320, 75, 23))
        self.btn1.setObjectName("btn1")
        self.label.setGeometry(QtCore.QRect(240, 230, 61, 31))
        self.label.setObjectName("label")
        self.code.setGeometry(QtCore.QRect(240, 270, 281, 31))
        self.code.setObjectName("code")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn1.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "ROOM CODE"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
