from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from controller import MainWindow_controller

class titleScreen(QtWidgets.QMainWindow):
    result = None
    buttonlist = []
    def __init__(self):
        super().__init__()
        loadUi("titleScreen.ui", self)
        self.buttonlist.append(self.button_home)
        self.buttonlist.append(self.button_tutorial)
        self.buttonlist.append(self.startButton)
        self.buttonlist.append(self.button_case)
        for i in self.buttonlist:
            i.setCheckable(True)
            i.clicked.connect(self.buttonClicked)

        self.startButton.clicked.connect(self.goto)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.button_home.setChecked(True)

    def goto(self):
        self.result = MainWindow_controller()
        self.result.show()
        self.close()

    def buttonClicked(self):
        sender_button = self.sender()
        for i in self.buttonlist:
            i.setChecked(False)
        sender_button.setChecked(True)
        self.lable_pagetitle.setText(sender_button.text())
