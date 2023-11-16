# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Yung-li\Desktop\ff\final version\case1.ui'
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
        self.gamewidget = QtWidgets.QWidget(self.centralwidget)
        self.gamewidget.setGeometry(QtCore.QRect(290, 10, 1611, 731))
        self.gamewidget.setAutoFillBackground(False)
        self.gamewidget.setObjectName("gamewidget")
        self.networkLabel = QtWidgets.QLabel(self.gamewidget)
        self.networkLabel.setGeometry(QtCore.QRect(1330, 10, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.networkLabel.setFont(font)
        self.networkLabel.setWordWrap(False)
        self.networkLabel.setObjectName("networkLabel")
        self.label_background = QtWidgets.QLabel(self.gamewidget)
        self.label_background.setGeometry(QtCore.QRect(0, -30, 1611, 761))
        self.label_background.setText("")
        self.label_background.setObjectName("label_background")
        self.widget_progress = QtWidgets.QWidget(self.gamewidget)
        self.widget_progress.setGeometry(QtCore.QRect(10, 670, 1591, 51))
        self.widget_progress.setObjectName("widget_progress")
        self.label_4 = QtWidgets.QLabel(self.widget_progress)
        self.label_4.setGeometry(QtCore.QRect(970, 10, 621, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.widget_progress)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.widget_progress)
        self.progressBar.setGeometry(QtCore.QRect(150, 20, 831, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 100)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.comboBox_network = QtWidgets.QComboBox(self.gamewidget)
        self.comboBox_network.setGeometry(QtCore.QRect(10, 620, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.comboBox_network.setFont(font)
        self.comboBox_network.setObjectName("comboBox_network")
        self.comboBox_network.addItem("")
        self.comboBox_network.addItem("")
        self.comboBox_network.addItem("")
        self.label_14 = QtWidgets.QLabel(self.gamewidget)
        self.label_14.setGeometry(QtCore.QRect(270, 630, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.fireArrivalListWidget = QtWidgets.QListWidget(self.gamewidget)
        self.fireArrivalListWidget.setGeometry(QtCore.QRect(1340, 70, 251, 581))
        self.fireArrivalListWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.fireArrivalListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.fireArrivalListWidget.setObjectName("fireArrivalListWidget")
        self.label_background.raise_()
        self.networkLabel.raise_()
        self.widget_progress.raise_()
        self.comboBox_network.raise_()
        self.label_14.raise_()
        self.fireArrivalListWidget.raise_()
        self.widget_downbar = QtWidgets.QWidget(self.centralwidget)
        self.widget_downbar.setGeometry(QtCore.QRect(10, 750, 921, 151))
        self.widget_downbar.setObjectName("widget_downbar")
        self.label_7 = QtWidgets.QLabel(self.widget_downbar)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.selectLabel = QtWidgets.QLabel(self.widget_downbar)
        self.selectLabel.setGeometry(QtCore.QRect(40, 60, 121, 81))
        self.selectLabel.setText("")
        self.selectLabel.setObjectName("selectLabel")
        self.label_10 = QtWidgets.QLabel(self.widget_downbar)
        self.label_10.setGeometry(QtCore.QRect(420, 20, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_selectedFF = QtWidgets.QLabel(self.widget_downbar)
        self.label_selectedFF.setGeometry(QtCore.QRect(190, 20, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(14)
        self.label_selectedFF.setFont(font)
        self.label_selectedFF.setText("")
        self.label_selectedFF.setObjectName("label_selectedFF")
        self.widget_3 = QtWidgets.QWidget(self.widget_downbar)
        self.widget_3.setGeometry(QtCore.QRect(180, 60, 731, 91))
        self.widget_3.setObjectName("widget_3")
        self.defendButton = QtWidgets.QPushButton(self.widget_3)
        self.defendButton.setGeometry(QtCore.QRect(20, 10, 101, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.defendButton.setFont(font)
        self.defendButton.setObjectName("defendButton")
        self.idleButton = QtWidgets.QPushButton(self.widget_3)
        self.idleButton.setGeometry(QtCore.QRect(160, 10, 101, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.idleButton.setFont(font)
        self.idleButton.setObjectName("idleButton")
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        self.label_8.setGeometry(QtCore.QRect(310, 10, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.spinBox = QtWidgets.QSpinBox(self.widget_3)
        self.spinBox.setGeometry(QtCore.QRect(460, 10, 229, 61))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.spinBox.setWrapping(True)
        self.spinBox.setMinimum(1)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.checkBox = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox.setGeometry(QtCore.QRect(280, 50, 171, 27))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setObjectName("checkBox")
        self.label_11 = QtWidgets.QLabel(self.widget_downbar)
        self.label_11.setGeometry(QtCore.QRect(0, 0, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.widget_leftbar = QtWidgets.QWidget(self.centralwidget)
        self.widget_leftbar.setGeometry(QtCore.QRect(0, 20, 291, 721))
        self.widget_leftbar.setObjectName("widget_leftbar")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget_leftbar)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 150, 281, 561))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_1 = QtWidgets.QLabel(self.widget_leftbar)
        self.label_1.setGeometry(QtCore.QRect(0, 120, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.label_1.setFont(font)
        self.label_1.setMouseTracking(False)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.lcd_time = QtWidgets.QLCDNumber(self.widget_leftbar)
        self.lcd_time.setGeometry(QtCore.QRect(160, 60, 101, 41))
        self.lcd_time.setObjectName("lcd_time")
        self.button_menu = QtWidgets.QPushButton(self.widget_leftbar)
        self.button_menu.setGeometry(QtCore.QRect(20, 30, 61, 71))
        self.button_menu.setToolTipDuration(0)
        self.button_menu.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button_menu.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Yung-li\\Desktop\\ff\\final version\\image/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_menu.setIcon(icon)
        self.button_menu.setIconSize(QtCore.QSize(50, 100))
        self.button_menu.setAutoDefault(False)
        self.button_menu.setObjectName("button_menu")
        self.label_2 = QtWidgets.QLabel(self.widget_leftbar)
        self.label_2.setGeometry(QtCore.QRect(160, 20, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setMouseTracking(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.selectedFFlabel = QtWidgets.QLabel(self.widget_leftbar)
        self.selectedFFlabel.setGeometry(QtCore.QRect(200, 0, 131, 71))
        self.selectedFFlabel.setText("")
        self.selectedFFlabel.setPixmap(QtGui.QPixmap("c:\\Users\\Yung-li\\Desktop\\ff\\final version\\image/left_arrow.png"))
        self.selectedFFlabel.setScaledContents(True)
        self.selectedFFlabel.setObjectName("selectedFFlabel")
        self.widget_downmiddle = QtWidgets.QWidget(self.centralwidget)
        self.widget_downmiddle.setGeometry(QtCore.QRect(940, 750, 391, 151))
        self.widget_downmiddle.setObjectName("widget_downmiddle")
        self.label_15 = QtWidgets.QLabel(self.widget_downmiddle)
        self.label_15.setGeometry(QtCore.QRect(0, 0, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.consoleLabel = QtWidgets.QLabel(self.widget_downmiddle)
        self.consoleLabel.setGeometry(QtCore.QRect(10, 20, 371, 121))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(12)
        self.consoleLabel.setFont(font)
        self.consoleLabel.setStyleSheet("border: 1px solid black;")
        self.consoleLabel.setWordWrap(True)
        self.consoleLabel.setObjectName("consoleLabel")
        self.widget_downright = QtWidgets.QWidget(self.centralwidget)
        self.widget_downright.setGeometry(QtCore.QRect(1330, 750, 571, 151))
        self.widget_downright.setObjectName("widget_downright")
        self.label_9 = QtWidgets.QLabel(self.widget_downright)
        self.label_9.setGeometry(QtCore.QRect(0, 0, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.listWidget = QtWidgets.QListWidget(self.widget_downright)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 551, 121))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1923, 25))
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
        self.networkLabel.setText(_translate("MainWindow", "Vulnerable Nodes"))
        self.label_4.setText(_translate("MainWindow", "Objective: \"contain\" the fire (firefighter cannot extinguish fire)"))
        self.label.setText(_translate("MainWindow", "Total value: "))
        self.progressBar.setFormat(_translate("MainWindow", "%v"))
        self.comboBox_network.setItemText(0, _translate("MainWindow", "Hybrid network"))
        self.comboBox_network.setItemText(1, _translate("MainWindow", "Fire network"))
        self.comboBox_network.setItemText(2, _translate("MainWindow", "FF network"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p> Select or press \'S\' to switch</p></body></html>"))
        self.fireArrivalListWidget.setSortingEnabled(False)
        self.label_7.setText(_translate("MainWindow", "Now assigning:"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p>hold Z: check node value&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hold X: check firefighter\'s process time</p></body></html>"))
        self.defendButton.setText(_translate("MainWindow", "Defend"))
        self.idleButton.setText(_translate("MainWindow", "Idle"))
        self.label_8.setText(_translate("MainWindow", "Set Idle time:"))
        self.checkBox.setText(_translate("MainWindow", "Idle til the end"))
        self.label_11.setText(_translate("MainWindow", "Control Panel"))
        self.label_1.setText(_translate("MainWindow", "Firefighter lists:"))
        self.label_2.setText(_translate("MainWindow", "Time"))
        self.label_15.setText(_translate("MainWindow", "Information Window"))
        self.consoleLabel.setText(_translate("MainWindow", "TextLabel"))
        self.label_9.setText(_translate("MainWindow", "Live Stream"))
        self.menuinfromations.setTitle(_translate("MainWindow", "Instructions"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionProblem.setText(_translate("MainWindow", "Problem description"))
        self.actionAnimation.setText(_translate("MainWindow", "Animation"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionControls.setText(_translate("MainWindow", "Controls"))
