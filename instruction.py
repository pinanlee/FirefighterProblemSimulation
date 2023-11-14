from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

class Instruction(QLabel):
    def __init__(self, widget):
        super().__init__(widget)
        self.setGeometry(600,50,600,600)
        self.index = 0
        import os

        # 資料夾路徑
        self.folder_path = './image/turtorial/'

        # 獲取資料夾中的所有檔案名稱
        self.file_list = os.listdir(self.folder_path)

        # 使用列表生成式過濾出檔案，如果你只想要特定類型的檔案，可以加上條件判斷
        self.file_list = [file for file in self.file_list if os.path.isfile(os.path.join(self.folder_path, file))]

        self.font = QtGui.QFont()
        self.font.setFamily("Arial Rounded MT Bold")
        self.font.setPointSize(10)
        self.setFont(self.font)
        self.setPixmap(QPixmap(self.folder_path + self.file_list[self.index]))
        self.setStyleSheet("background-color: white;border: 2px solid blue;")
        self.leaveButton = QPushButton(widget)
        self.leaveButton.setGeometry(850,599,101,51)
        self.leaveButton.setText("back to game")
        self.leaveButton.clicked.connect(self.intoGame)
        self.nextButton = QPushButton(widget)
        self.nextButton.setGeometry(1100,599,101,51)
        self.nextButton.setText("next")
        self.nextButton.clicked.connect(self.nextImg)       
        self.prevButton = QPushButton(widget)
        self.prevButton.setGeometry(600,599,101,51)
        self.prevButton.setText("prev")
        self.prevButton.setEnabled(False)
        self.prevButton.clicked.connect(self.prevImg)  
        self.intoGame()     

    def intoGame(self):
        self.setHidden(True)
        self.leaveButton.setHidden(True)
        self.prevButton.setHidden(True)
        self.nextButton.setHidden(True)
        self.lower()
        self.leaveButton.lower()
        self.nextButton.lower()
        self.prevButton.lower()
    
    def show(self):
        self.raise_()
        self.leaveButton.raise_()
        self.nextButton.raise_()
        self.prevButton.raise_()
        self.setHidden(False)
        self.leaveButton.setHidden(False)
        self.prevButton.setHidden(False)
        self.nextButton.setHidden(False)

    def nextImg(self):
        self.prevButton.setEnabled(True)
        if(self.index == len(self.file_list) - 1):
            self.nextButton.setEnabled(False)
        else:
            self.index += 1
        self.setPixmap(QPixmap(self.folder_path + self.file_list[self.index]))

    def prevImg(self):
        self.nextButton.setEnabled(True)
        if(self.index == 0):
            self.prevButton.setEnabled(False)
        else:
            self.index -= 1
        self.setPixmap(QPixmap(self.folder_path + self.file_list[self.index]))