# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Yung-li\Desktop\ff\new input format\titleScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 466)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_sidebar = QtWidgets.QWidget(self.centralwidget)
        self.widget_sidebar.setGeometry(QtCore.QRect(590, 0, 211, 471))
        self.widget_sidebar.setObjectName("widget_sidebar")
        self.button_case = QtWidgets.QPushButton(self.widget_sidebar)
        self.button_case.setGeometry(QtCore.QRect(0, 170, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_case.setFont(font)
        self.button_case.setObjectName("button_case")
        self.startButton = QtWidgets.QPushButton(self.widget_sidebar)
        self.startButton.setGeometry(QtCore.QRect(0, 250, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.button_tutorial = QtWidgets.QPushButton(self.widget_sidebar)
        self.button_tutorial.setGeometry(QtCore.QRect(0, 90, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_tutorial.setFont(font)
        self.button_tutorial.setObjectName("button_tutorial")
        self.button_home = QtWidgets.QPushButton(self.widget_sidebar)
        self.button_home.setGeometry(QtCore.QRect(0, 10, 211, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.button_home.setFont(font)
        self.button_home.setObjectName("button_home")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(0, 0, 591, 461))
        self.widget_3.setObjectName("widget_3")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setGeometry(QtCore.QRect(10, 70, 561, 111))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget_3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 571, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lable_pagetitle = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lable_pagetitle.setFont(font)
        self.lable_pagetitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lable_pagetitle.setObjectName("lable_pagetitle")
        self.horizontalLayout.addWidget(self.lable_pagetitle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_3)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 70, 561, 381))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 291, 111))
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.button_case1 = QtWidgets.QPushButton(self.page_3)
        self.button_case1.setGeometry(QtCore.QRect(80, 80, 141, 161))
        self.button_case1.setObjectName("button_case1")
        self.stackedWidget.addWidget(self.page_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FireFighter Simulator"))
        self.button_case.setText(_translate("MainWindow", "Example Case"))
        self.startButton.setText(_translate("MainWindow", "Random Graph Mode"))
        self.button_tutorial.setText(_translate("MainWindow", "Tutorial"))
        self.button_home.setText(_translate("MainWindow", "Introduction"))
        self.lable_pagetitle.setText(_translate("MainWindow", "FireFighter Simulatior"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.button_case1.setText(_translate("MainWindow", "case1"))
