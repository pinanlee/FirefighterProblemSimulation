# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Yung-li\Desktop\ff\pull\UIv3.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1894, 1061)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
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
        self.node_info_label.setGeometry(QtCore.QRect(950, 600, 241, 141))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.node_info_label.setFont(font)
        self.node_info_label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.node_info_label.setObjectName("node_info_label")
        self.instruct = QtWidgets.QLabel(self.centralwidget)
        self.instruct.setGeometry(QtCore.QRect(800, 350, 400, 200))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.instruct.setFont(font)
        self.instruct.setStyleSheet("background-color: white;border: 2px solid blue;")
        self.instruct.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.instruct.setObjectName("instruct")
        self.yesButton = QtWidgets.QPushButton(self.centralwidget)
        self.yesButton.setGeometry(QtCore.QRect(990, 550, 101, 51))
        self.yesButton.setStyleSheet("background-color: white;border: 2px solid blue;")
        self.yesButton.setObjectName("yesButton")
        self.noButton = QtWidgets.QPushButton(self.centralwidget)
        self.noButton.setGeometry(QtCore.QRect(1090, 550, 101, 51))
        self.noButton.setStyleSheet("background-color: white;border: 2px solid blue;")
        self.noButton.setObjectName("noButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1891, 1021))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.timeIndexLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeIndexLabel.sizePolicy().hasHeightForWidth())
        self.timeIndexLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(22)
        self.timeIndexLabel.setFont(font)
        self.timeIndexLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.timeIndexLabel.setObjectName("timeIndexLabel")
        self.verticalLayout_4.addWidget(self.timeIndexLabel)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.backgroundLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backgroundLabel.sizePolicy().hasHeightForWidth())
        self.backgroundLabel.setSizePolicy(sizePolicy)
        self.backgroundLabel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.backgroundLabel.setText("")
        self.backgroundLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.gridLayout.addWidget(self.backgroundLabel, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.networkLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.networkLabel.sizePolicy().hasHeightForWidth())
        self.networkLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.networkLabel.setFont(font)
        self.networkLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.networkLabel.setWordWrap(False)
        self.networkLabel.setObjectName("networkLabel")
        self.verticalLayout_4.addWidget(self.networkLabel)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1894, 18))
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Firefighter Problem Simulation"))
        self.descriptionLabel.setText(_translate("MainWindow", "TextLabel"))
        self.node_info_label.setText(_translate("MainWindow", "TextLabel"))
        self.instruct.setText(_translate("MainWindow", "<html><head/><body><p>Do you need</p><p>step by step turtorial?</p></body></html>"))
        self.yesButton.setText(_translate("MainWindow", "Yes"))
        self.noButton.setText(_translate("MainWindow", "No"))
        self.timeIndexLabel.setText(_translate("MainWindow", "t=0"))
        self.networkLabel.setText(_translate("MainWindow", "Hybrid network"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Control Panel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Node Information"))
        self.menuinfromations.setTitle(_translate("MainWindow", "Instructions"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionProblem.setText(_translate("MainWindow", "Problem description"))
        self.actionAnimation.setText(_translate("MainWindow", "Animation"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionControls.setText(_translate("MainWindow", "Controls"))
