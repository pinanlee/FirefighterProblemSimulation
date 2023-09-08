# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Yung-li\Desktop\ff\pull\UIv4.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1923, 964)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.descriptionLabel = QtWidgets.QLabel(self.centralwidget)
        self.descriptionLabel.setGeometry(QtCore.QRect(-1200, 240, 1091, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.descriptionLabel.setFont(font)
        self.descriptionLabel.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.node_info_label = QtWidgets.QLabel(self.centralwidget)
        self.node_info_label.setEnabled(True)
        self.node_info_label.setGeometry(QtCore.QRect(950, 350, 241, 141))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.node_info_label.setFont(font)
        self.node_info_label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.node_info_label.setObjectName("node_info_label")
        self.timeIndexLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeIndexLabel.setGeometry(QtCore.QRect(0, 0, 111, 91))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(22)
        self.timeIndexLabel.setFont(font)
        self.timeIndexLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeIndexLabel.setObjectName("timeIndexLabel")
        self.backgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundLabel.setGeometry(QtCore.QRect(300, 0, 1621, 751))
        self.backgroundLabel.setStyleSheet("border: 2px solid blue;")
        self.backgroundLabel.setText("")
        self.backgroundLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.networkLabel = QtWidgets.QLabel(self.centralwidget)
        self.networkLabel.setGeometry(QtCore.QRect(870, 600, 311, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.networkLabel.setFont(font)
        self.networkLabel.setWordWrap(False)
        self.networkLabel.setObjectName("networkLabel")
        self.hintLabel = QtWidgets.QLabel(self.centralwidget)
        self.hintLabel.setGeometry(QtCore.QRect(770, 170, 311, 161))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.hintLabel.setFont(font)
        self.hintLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid blue;")
        self.hintLabel.setText("")
        self.hintLabel.setWordWrap(True)
        self.hintLabel.setObjectName("hintLabel")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(1810, 0, 111, 41))
        self.backButton.setObjectName("backButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 760, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(320, 810, 441, 23))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.consoleLabel = QtWidgets.QLabel(self.centralwidget)
        self.consoleLabel.setGeometry(QtCore.QRect(800, 770, 631, 81))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.consoleLabel.setFont(font)
        self.consoleLabel.setStyleSheet("border: 2px solid blue;")
        self.consoleLabel.setObjectName("consoleLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 690, 261, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1923, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        self.menuinfromations = QtWidgets.QMenu(self.menubar)
        self.menuinfromations.setObjectName("menuinfromations")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionProblem = QtWidgets.QAction(MainWindow)
        self.actionProblem.setObjectName("actionProblem")
        self.actionAnimation = QtWidgets.QAction(MainWindow)
        self.actionAnimation.setObjectName("actionAnimation")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionControls = QtWidgets.QAction(MainWindow)
        self.actionControls.setObjectName("actionControls")
        self.menuinfromations.addAction(self.actionProblem)
        self.menuinfromations.addAction(self.actionControls)
        self.menuFile.addAction(self.actionNew)
        self.menuSettings.addAction(self.actionAnimation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuinfromations.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Firefighter Problem Simulation"))
        self.descriptionLabel.setText(_translate("MainWindow", "TextLabel"))
        self.node_info_label.setText(_translate("MainWindow", "TextLabel"))
        self.timeIndexLabel.setText(_translate("MainWindow", "t=0"))
        self.networkLabel.setText(_translate("MainWindow", "Hybrid network"))
        self.backButton.setText(_translate("MainWindow", "Back to game"))
        self.label.setText(_translate("MainWindow", "Total value: "))
        self.progressBar.setFormat(_translate("MainWindow", "%v"))
        self.consoleLabel.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "Now assigning:"))
        self.menuinfromations.setTitle(_translate("MainWindow", "Instructions"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionProblem.setText(_translate("MainWindow", "Problem description"))
        self.actionAnimation.setText(_translate("MainWindow", "Animation"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionControls.setText(_translate("MainWindow", "Controls"))
