from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from controller import MainWindow_controller

class titleScreen(QtWidgets.QMainWindow):
    result = None
    def __init__(self):
        super().__init__()
        loadUi("titleScreen.ui", self)
        self.startButton.clicked.connect(self.goto)
    def goto(self):
        self.result = MainWindow_controller()
        self.result.show()
        self.close()