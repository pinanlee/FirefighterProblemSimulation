# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIv.2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(1195, 786)
        MainWindow.setGeometry(QtCore.QRect(150, 150, 1195, 786))
        MainWindow.setFixedSize(1195, 786)
        MainWindow.setWindowFlags(Qt.WindowCloseButtonHint)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 570, 391, 161))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.label.setFont(font)
        self.label.setObjectName("label")
<<<<<<< HEAD
        '''self.FFlabel = QtWidgets.QLabel(self.centralwidget)
        self.FFlabel.setGeometry(QtCore.QRect(470, 590, 191, 141))
        self.FFlabel.setObjectName("FFlabel")
        self.FFlabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.FFlabel_2.setGeometry(QtCore.QRect(810, 590, 191, 141))
        self.FFlabel_2.setObjectName("FFlabel_2")
=======
        from controller import FFNum
        self.numFF = FFNum
        self.labelList = []
        for i in range(self.numFF):
            self.FFlabel = QtWidgets.QLabel(self.centralwidget)
            self.FFlabel.setGeometry(QtCore.QRect(470, 590, 50, 50))
            self.labelList.append(self.FFlabel)
        # self.FFlabel = QtWidgets.QLabel(self.centralwidget)
        # self.FFlabel.setGeometry(QtCore.QRect(470, 590, 191, 141))
        # self.FFlabel.setObjectName("FFlabel")
        # self.FFlabel_2 = QtWidgets.QLabel(self.centralwidget)
        # self.FFlabel_2.setGeometry(QtCore.QRect(810, 590, 191, 141))
        # self.FFlabel_2.setObjectName("FFlabel_2")
        # self.FFlabel_3 = QtWidgets.QLabel(self.centralwidget)
        # self.FFlabel_3.setGeometry(QtCore.QRect(810, 590, 191, 141))
        # self.FFlabel_3.setObjectName("FFlabel_3")
>>>>>>> 6a91006f35f0dee3d276506145015e43398b44d7
        self.statuslabel = QtWidgets.QLabel(self.centralwidget)
        self.statuslabel.setGeometry(QtCore.QRect(590, 620, 181, 71))'''
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        '''self.statuslabel.setFont(font)
        self.statuslabel.setObjectName("statuslabel")
        self.statuslabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.statuslabel_2.setGeometry(QtCore.QRect(930, 620, 181, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.statuslabel_2.setFont(font)
        self.statuslabel_2.setObjectName("statuslabel_2")'''
        self.backgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, 1191, 561))
        self.backgroundLabel.setText("")
        self.backgroundLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.networkLabel = QtWidgets.QLabel(self.centralwidget)
        self.networkLabel.setGeometry(QtCore.QRect(870, 500, 311, 71))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(16)
        self.networkLabel.setFont(font)
        self.networkLabel.setObjectName("networkLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1195, 18))
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
        self.actionnodes = QtWidgets.QAction(MainWindow)
        self.actionnodes.setObjectName("actionnodes")
        self.actionAnimation = QtWidgets.QAction(MainWindow)
        self.actionAnimation.setObjectName("actionAnimation")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.menuinfromations.addAction(self.actionnodes)
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
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Instructions:</p><p>Enter:  move to next time</p><p>C: change selected firefighter</p><p>A, D: change selected node</p><p>Space: Assign firefighter to selected node</p></body></html>"))
<<<<<<< HEAD
        '''self.FFlabel.setText(_translate("MainWindow", "TextLabel"))
        self.FFlabel_2.setText(_translate("MainWindow", "TextLabel"))
=======
>>>>>>> 6a91006f35f0dee3d276506145015e43398b44d7
        self.statuslabel.setText(_translate("MainWindow", "TextLabel"))
        self.statuslabel_2.setText(_translate("MainWindow", "TextLabel"))'''
        self.networkLabel.setText(_translate("MainWindow", "Hybrid network"))
        self.menuinfromations.setTitle(_translate("MainWindow", "Status"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionnodes.setText(_translate("MainWindow", "InformationWindow"))
        self.actionAnimation.setText(_translate("MainWindow", "Firefighter"))
        self.actionNew.setText(_translate("MainWindow", "New"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

