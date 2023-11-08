from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
from nodeButtonController import NodeController

class nodePropertyVis(QLabel):
    def __init__(self, widget, controller):
        super().__init__(widget)
        self.__nodeController : NodeController = controller
        self.__valueAmount = controller.getGrassAmount()
        self.showValue()
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.setFont(font)
        self.hide()
    
    def showValue(self):
        self.__valueAmount = self.__nodeController.getValue()//10 * 10 + 25
        self.setText("")
        self.setGeometry(self.__nodeController.x()-int((self.__valueAmount - self.__nodeController.width())/2 ), self.__nodeController.y()-int((self.__valueAmount - self.__nodeController.height())/2), self.__valueAmount, self.__valueAmount)
        self.setStyleSheet("background-color: yellow; border: 3px solid blue;")
        self.show()

    def showGrassValue(self):
        self.__valueAmount = self.__nodeController.getGrassAmount()//10 * 10 + 25
        self.setGeometry(self.__nodeController.x()-int((self.__valueAmount - self.__nodeController.width())/2 ), self.__nodeController.y()-int((self.__valueAmount - self.__nodeController.height())/2), self.__valueAmount, self.__valueAmount)
        self.setStyleSheet("background-color: red; border: 3px solid blue;")
        self.setText(f"{self.__valueAmount}")
        self.show()