import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUi
from controller import MainWindow_controller
import json
import pandas as pd
from simulationWindow import SimulationWindow


class titleScreen(QtWidgets.QMainWindow):
    result = None
    buttonlist = []
    shift = False
    def __init__(self):
        super().__init__()
        loadUi("titleScreen.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        self.buttonlist.append(self.button_home)
        self.buttonlist.append(self.button_tutorial)
        self.buttonlist.append(self.startButton)
        self.buttonlist.append(self.button_case)
        self.buttonlist.append(self.button_simulation)
        for i in self.buttonlist:
            i.setCheckable(True)
            i.clicked.connect(self.buttonClicked)
        self.button_startGame.clicked.connect(lambda: self.goto(1))
        self.button_case1.clicked.connect(lambda: self.goto(2))
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.button_home.setChecked(True)
        self.button_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.button_tutorial.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.button_case.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.startButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.button_simulation.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.button_enter.clicked.connect(lambda: self.goto(3))
        self.button_file.clicked.connect(self.buttonfileEvent)
        self.checkBox.stateChanged.connect(self.checkboxEvent)
        self.checkBox.setCheckState(2)

    def goto(self, mode):
        if(mode == 3) :
            self.result = SimulationWindow()
            self.result.show()
            self.close()
        elif self.shift or mode == 2:
            self.result = MainWindow_controller(mode)
            self.result.show()
            self.close()

    def buttonClicked(self):
        sender_button = self.sender()
        for i in self.buttonlist:
            i.setChecked(False)
        sender_button.setChecked(True)
        self.lable_pagetitle.setText(sender_button.text())

    def buttonfileEvent(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Excel Files (*.xlsx)"
        options |= QFileDialog.FileType
        file_path, _ = QFileDialog.getOpenFileName(self, '選擇檔案', '', file_filter, options=options)
        self.label_filename.setText(file_path)
        if file_path:
            temp = {"filename": file_path}
            with open('filename.json', 'w') as file:
                json.dump(temp, file)
            data = pd.read_excel(file_path, sheet_name='ff_source', header=None)
            fs = data.iat[1, 0]
            data = pd.read_excel(file_path, sheet_name='fire_source', header=None)
            dn = data.iat[1, 0]
            ffn = 1
            df = pd.read_excel(file_path, sheet_name='coordinates', header=None)
            first_column = df.iloc[:,0]
            nn = first_column.count() - 1
            df = pd.read_excel(file_path, sheet_name='firefighter_route', header=None)
            first_column = df.iloc[:, 0]
            ffn = first_column.iloc[-1]
            self.textBrowser_fs.setPlainText(str(fs))
            self.textBrowser_dn.setPlainText(str(dn))
            self.textBrowser_nn.setPlainText(str(nn))
            self.textBrowser_ffn.setPlainText(str(ffn))
        if os.path.exists("filename.json"):
            self.shift = True

    def checkboxEvent(self):
        if self.checkBox.isChecked():
            file_path = "./network/FF2test/FFP_n20_no1.xlsx"
            temp = {"filename": file_path}
            with open('filename.json', 'w') as file:
                json.dump(temp, file)
            self.label_filename.setText(file_path)
            data = pd.read_excel(file_path, sheet_name='ff_source', header=None)
            fs = data.iat[1, 0]
            data = pd.read_excel(file_path, sheet_name='fire_source', header=None)
            dn = data.iat[1, 0]
            nn = 20
            ffn = 2
            self.textBrowser_fs.setPlainText(str(fs))
            self.textBrowser_dn.setPlainText(str(dn))
            self.textBrowser_nn.setPlainText(str(nn))
            self.textBrowser_ffn.setPlainText(str(ffn))
            self.shift = True
        else:
            self.label_filename.setText("")
            self.textBrowser_fs.setPlainText("")
            self.textBrowser_dn.setPlainText("")
            self.textBrowser_nn.setPlainText("")
            self.textBrowser_ffn.setPlainText("")
            self.shift = False

    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        if os.path.exists("filename.json"):
            os.remove("filename.json")
