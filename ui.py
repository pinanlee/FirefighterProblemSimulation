# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'example.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from FF import Node
import math

def aa():
    df = pd.read_excel("firefighter_route.xlsx")
    df_num = len(df.index)
    print(df)
    '''for i in N:
        A_p.append((i,i))
    for i in range(0,df_num):
        u = df.iloc[i]['i']
        v = df.iloc[i]['j']
        fighterIndex = df.iloc[i]['k']
        time = df.iloc[i]['travel time']
        A_p.append((u,v))
        tau[u,v,fighterIndex] = time
    df = pd.read_excel("fire_route.xlsx")
    df_num = len(df.index)
    for i in range(0,df_num):
        u = df.iloc[i]['i']
        v = df.iloc[i]['j']
        time = df.iloc[i]['travel time']
        A_f.append((u,v))
        lamb[u,v] = time
    for i in Q:
        process[i] = math.ceil(Q[i]*H[i]/P)'''

traveltime = [[]]

class Ui_MainWindow(object):
    def aa(self):
        global traveltime
        df = pd.read_excel("firefighter_route.xlsx")
        df_num = len(df.index)
        for i in range(df_num):
        #print(df_num)
            traveltime.append([df.iloc[i]["j"],df.iloc[i]["travel time"]])
        print(traveltime)
    def setupUi(self, MainWindow):
        self.aa()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 741)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 1051, 541))   
        self.background_label.raise_()

        self.timeIndexLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeIndexLabel.setGeometry(QtCore.QRect(30, 20, 91, 41))

        self.descriptionLabel = QtWidgets.QLabel(self.centralwidget)
        self.descriptionLabel.setGeometry(QtCore.QRect(380, 510, 661, 61))

        self.image_1 = QtWidgets.QLabel(self.centralwidget)
        self.image_1.setGeometry(QtCore.QRect(230, 0, 101, 101))
        node1Pos = QtCore.QRect(310, 20, 61, 51)
        self.nodeButton_1 = Node(self.centralwidget, self.image_1, 1, node1Pos)

        self.image_2 = QtWidgets.QLabel(self.centralwidget)
        self.image_2.setGeometry(QtCore.QRect(560, 0, 101, 101))
        node2Pos = QtCore.QRect(630, 40, 61, 51)
        self.nodeButton_2 = Node(self.centralwidget, self.image_2, 2, node2Pos)

        self.image_3 = QtWidgets.QLabel(self.centralwidget)
        self.image_3.setGeometry(QtCore.QRect(810, 20, 101, 101))
        node3Pos = QtCore.QRect(870, 50, 61, 51)
        self.nodeButton_3 = Node(self.centralwidget, self.image_3, 3, node3Pos)

        self.image_4 = QtWidgets.QLabel(self.centralwidget)
        self.image_4.setGeometry(QtCore.QRect(40, 110, 101, 101))
        node4Pos = QtCore.QRect(100, 130, 61, 61)
        self.nodeButton_4 = Node(self.centralwidget, self.image_4, 4, node4Pos)

        self.image_5 = QtWidgets.QLabel(self.centralwidget)
        self.image_5.setGeometry(QtCore.QRect(450, 100, 101, 101))
        node5Pos = QtCore.QRect(430, 140, 61, 51)
        self.nodeButton_5 = Node(self.centralwidget, self.image_5, 5, node5Pos)

        self.image_6 = QtWidgets.QLabel(self.centralwidget)
        self.image_6.setGeometry(QtCore.QRect(650, 160, 101, 101))
        node6Pos = QtCore.QRect(710, 190, 61, 51)
        self.nodeButton_6 = Node(self.centralwidget, self.image_6, 6, node6Pos)

        self.image_7 = QtWidgets.QLabel(self.centralwidget)
        self.image_7.setGeometry(QtCore.QRect(910, 170, 101, 101))
        node7Pos = QtCore.QRect(980, 190, 61, 51)
        self.nodeButton_7 = Node(self.centralwidget, self.image_7, 7, node7Pos)

        self.image_8 = QtWidgets.QLabel(self.centralwidget)
        self.image_8.setGeometry(QtCore.QRect(40, 300, 101, 101))
        node8Pos = QtCore.QRect(20, 330, 61, 51)
        self.nodeButton_8 = Node(self.centralwidget, self.image_8, 8, node8Pos)

        self.image_9 = QtWidgets.QLabel(self.centralwidget)
        self.image_9.setGeometry(QtCore.QRect(320, 230, 101, 101))
        node9Pos = QtCore.QRect(300, 250, 61, 51)
        self.nodeButton_9 = Node(self.centralwidget, self.image_9, 9, node9Pos)

        self.image_10 = QtWidgets.QLabel(self.centralwidget)
        self.image_10.setGeometry(QtCore.QRect(510, 240, 101, 101))
        node10Pos = QtCore.QRect(500, 270, 61, 51)
        self.nodeButton_10 = Node(self.centralwidget, self.image_10, 10, node10Pos)

        self.image_11 = QtWidgets.QLabel(self.centralwidget)
        self.image_11.setGeometry(QtCore.QRect(750, 300, 101, 101))
        node11Pos = QtCore.QRect(820, 300, 61, 61)
        self.nodeButton_11 = Node(self.centralwidget, self.image_11, 11, node11Pos)

        self.image_12 = QtWidgets.QLabel(self.centralwidget)
        self.image_12.setGeometry(QtCore.QRect(140, 450, 101, 101))
        node12Pos = QtCore.QRect(120, 480, 61, 51)
        self.nodeButton_12 = Node(self.centralwidget, self.image_12, 12, node12Pos)

        self.image_13 = QtWidgets.QLabel(self.centralwidget)
        self.image_13.setGeometry(QtCore.QRect(360, 380, 101, 101))
        node13Pos = QtCore.QRect(350, 410, 61, 51)
        self.nodeButton_13 = Node(self.centralwidget, self.image_13, 13, node13Pos)

        self.image_14 = QtWidgets.QLabel(self.centralwidget)
        self.image_14.setGeometry(QtCore.QRect(890, 420, 101, 101))
        node14Pos = QtCore.QRect(960, 430, 61, 51)
        self.nodeButton_14 = Node(self.centralwidget, self.image_14, 14, node14Pos)

        self.image_15 = QtWidgets.QLabel(self.centralwidget)
        self.image_15.setGeometry(QtCore.QRect(560, 430, 101, 101))
        node15Pos = QtCore.QRect(620, 470, 61, 51)
        self.nodeButton_15 = Node(self.centralwidget, self.image_15, 15, node15Pos)

        self.timeButton = QtWidgets.QPushButton(self.centralwidget)
        self.timeButton.setGeometry(QtCore.QRect(10, 500, 81, 51))


        self.node_info_label = QtWidgets.QLabel(self.centralwidget)
        self.node_info_label.setGeometry(QtCore.QRect(10, 570, 431, 121))

        self.moveFF = QtWidgets.QPushButton(self.centralwidget)
        self.moveFF.setGeometry(QtCore.QRect(800, 640, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.moveFF.setFont(font)
        self.moveFF.setObjectName("moveFF")
        self.moveButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveButton.setGeometry(QtCore.QRect(470, 640, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.moveButton.setFont(font)
        self.moveButton.setObjectName("moveButton")
        self.FFlabel = QtWidgets.QLabel(self.centralwidget)
        self.FFlabel.setGeometry(QtCore.QRect(750, 560, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FFlabel.setFont(font)

        self.processButton = QtWidgets.QPushButton(self.centralwidget)
        self.processButton.setGeometry(QtCore.QRect(470, 560, 201, 61))
        self.processButton.raise_()

        self.timeIndexLabel.raise_()
        self.descriptionLabel.raise_()
        self.timeButton.raise_()

        self.nodeButton_1.raise_()
        self.nodeButton_2.raise_()
        self.nodeButton_3.raise_()
        self.nodeButton_4.raise_()
        self.nodeButton_5.raise_()
        self.nodeButton_6.raise_()
        self.nodeButton_7.raise_()
        self.nodeButton_8.raise_()
        self.nodeButton_9.raise_()
        self.nodeButton_10.raise_()
        self.nodeButton_11.raise_()        
        self.nodeButton_12.raise_()
        self.nodeButton_13.raise_()
        self.nodeButton_14.raise_()
        self.nodeButton_15.raise_()

        self.node_info_label.raise_()
        self.moveFF.raise_()
        self.moveButton.raise_()
        self.FFlabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1050, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.timeIndexLabel.setText(_translate("MainWindow", "t: 0"))
        self.descriptionLabel.setText(_translate("MainWindow", "choose vertices to save"))
        self.timeButton.setText(_translate("MainWindow", "t++"))
        self.background_label.setText(_translate("MainWindow", "TextLabel"))
        self.background_label.setPixmap(QtGui.QPixmap("network.png"))  
        self.node_info_label.setText(_translate("MainWindow", "TextLabel"))
        self.moveFF.setText(_translate("MainWindow", "change Firefighter"))
        self.moveButton.setText(_translate("MainWindow", "move to this node"))
        self.FFlabel.setText(_translate("MainWindow", "selected FireFighter: 1"))
        self.processButton.setText(_translate("MainWindow", "defend"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

