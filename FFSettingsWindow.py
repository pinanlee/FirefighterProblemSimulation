import json

from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF, pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QGraphicsScene, QFileDialog, QWidget, QVBoxLayout, QPushButton
from PyQt5 import QtWidgets, QtCore, QtGui
from UIffSettings import Ui_FFSettings
from PyQt5.QtGui import QPixmap, QPainter, QPen, QIntValidator
from PyQt5 import uic
import random
import math
import sys
import os


class FFnumWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.FFnumWindowUI()
        self.setup_control()
        self.window_FF = FFSettingsWindow()
        self.FFnum = -1


    def FFnumWindowUI(self):
        self.setWindowTitle("")
        self.setGeometry(650, 400, 400, 300)
        self.setFixedSize(400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label_enter = QtWidgets.QLabel(self.central_widget)
        self.label_enter.setGeometry(QtCore.QRect(100, 130, 171, 31))
        self.label_enter.setText("Firefighter number: ")


        self.lineEdit_num = QtWidgets.QLineEdit(self.central_widget)
        self.lineEdit_num.setGeometry(QtCore.QRect(250, 130, 111, 31))
        int_validator = QIntValidator()
        self.lineEdit_num.setValidator(int_validator)

        self.button_num = QPushButton('Next',self.central_widget)
        self.button_num.setGeometry(QtCore.QRect(250, 250, 111, 31))

        self.label_warning = QtWidgets.QLabel(self.central_widget)
        self.label_warning.setStyleSheet('color: red;')
        self.label_warning.setGeometry(QtCore.QRect(180, 150, 171, 31))
        self.label_warning.setText("")
        self.font = QtGui.QFont()
        self.font.setBold(False)
        self.label_warning.setFont(self.font)


    def setup_control(self):
        self.button_num.clicked.connect(self.openFFSettingsWindow)

    def openFFSettingsWindow(self):
        tempFFnum = self.lineEdit_num.text()
        if(tempFFnum != ""):
            self.FFnum = int(tempFFnum)
        if(self.FFnum <= 0):
            self.font.setBold(True)
            self.label_warning.setText("Please enter a number!!")
            self.label_warning.setFont(self.font)
        else:
            self.window_FF.FFnum = self.FFnum
            self.window_FF.initFFdict()
            self.window_FF.show()
            self.close()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if(a0.key()==Qt.Key_Enter-1):
            self.openFFSettingsWindow()


class FFSettingsWindow(QtWidgets.QMainWindow):
    updateFFnumSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.ui = Ui_FFSettings()
        self.ui.setupUi(self)
        self.setup_control()
        self.FFnum = -1
        self.ffdict = []
        self.ffdictindex = 0
        self.scene = QGraphicsScene()


    def setup_control(self):
        self.ui.pushButton_Default.clicked.connect(self.defaultButtonClicked)
        self.ui.pushButton_Upload.clicked.connect(self.uploadButtonClicked)
        self.ui.toolButton_next.clicked.connect(self.nextToolButtonClicked)
        self.ui.toolButton_pre.clicked.connect(self.preToolButtonClicked)
        self.ui.pushButton_Done.clicked.connect(self.doneButtonClicked)
        self.ui.pushButton_Save.clicked.connect(self.saveButtonClicked)


    def initFFdict(self):
        for i in range(self.FFnum):
            ffdict = {"num": i+1,
                      "img": "",
                      "ts": 0,
                      "er": 0
                      }
            self.ffdict.append(ffdict)
        self.ui.label_FFNoutput.setText(str(self.ffdict[0]["num"]))

    def defaultButtonClicked(self):
        self.scene.clear()
        self.ui.graphic_img.setScene(None)
        pixmap = QPixmap("image/firefighter.png")  # 替换为您自己的图像文件路径
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.ui.graphic_img.setScene(self.scene)
        self.ui.graphic_img.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.ui.graphic_img.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphic_img.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ffdict[self.ffdictindex]["img"] = "image/firefighter.png"


    def uploadButtonClicked(self):
        self.scene.clear()
        self.ui.graphic_img.setScene(None)
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.FileType
        file_filter = "图像文件 (*.png *.jpg)"
        file_path, _ = QFileDialog.getOpenFileName(self, '選擇照片', '', file_filter, options=options)
        pixmap = QPixmap(file_path)
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.ui.graphic_img.setScene(self.scene)
        self.ui.graphic_img.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.ui.graphic_img.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphic_img.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ffdict[self.ffdictindex]["img"] = file_path



    def nextToolButtonClicked(self):
        self.ffdictindex = (self.ffdictindex + 1) % self.FFnum
        self.ui.label_FFNoutput.setText(str(self.ffdict[self.ffdictindex]["num"]))
        pixmap = QPixmap(self.ffdict[self.ffdictindex]["img"])
        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.ui.graphic_img.setScene(self.scene)
        self.ui.graphic_img.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.ui.graphic_img.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphic_img.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.ui.lineEdit_FER.setText(str(self.ffdict[self.ffdictindex]["er"]))
        self.ui.lineEdit_TS.setText(str(self.ffdict[self.ffdictindex]["ts"]))

    def preToolButtonClicked(self):
        self.ffdictindex = (self.ffdictindex - 1) % self.FFnum
        self.ui.label_FFNoutput.setText(str(self.ffdict[self.ffdictindex]["num"]))
        pixmap = QPixmap(self.ffdict[self.ffdictindex]["img"])
        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)
        self.ui.graphic_img.setScene(self.scene)
        self.ui.graphic_img.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.ui.graphic_img.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphic_img.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.ui.lineEdit_FER.setText(str(self.ffdict[self.ffdictindex]["er"]))
        self.ui.lineEdit_TS.setText(str(self.ffdict[self.ffdictindex]["ts"]))



    def doneButtonClicked(self):
        data_to_store = {
            "FFnumber": self.FFnum,
            "FFinfo": self.ffdict
        }
        with open('FFInfo.json', 'w') as file:
            json.dump(data_to_store, file)

        self.updateFFnumSignal.emit(1)

    def saveButtonClicked(self):
        value_ts = self.ui.lineEdit_TS.text()
        value_er = self.ui.lineEdit_FER.text()
        self.ffdict[self.ffdictindex]["ts"] = value_ts
        self.ffdict[self.ffdictindex]["er"] = value_er








