from PyQt5.QtGui import QPixmap, QCursor, QResizeEvent, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel
from PyQt5 import QtWidgets,QtCore,QtGui
from nodeButtonController import NodeController

class nodePropertyVis(QLabel):
    def __init__(self, widget, controller):
        super().__init__(widget)
        self.__nodeController : NodeController = controller
        self.__valueAmount = controller.getGrassAmount()
        self.showValue()
        self.__pix = QPixmap(self.size())
        self.hide()
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self.__pix)
        painter.setBrush(QColor(255,255,255))
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawEllipse(self.rect())
        painter.end()
    
    def showValue(self):
        self.__valueAmount = self.__nodeController.getValue() *3
        self.setText("")
        self.setGeometry(self.__nodeController.x()-int((self.__valueAmount - self.__nodeController.width())/2 ), self.__nodeController.y()-int((self.__valueAmount - self.__nodeController.height())/2), self.__valueAmount, self.__valueAmount)
        self.setStyleSheet("background-color: yellow; border: 3px solid blue;")
        self.__pix = QPixmap(self.size())
        self.show()

    def showGrassValue(self):
        self.__valueAmount = self.__nodeController.getGrassAmount()
        self.setGeometry(self.__nodeController.x()-int((self.__valueAmount - self.__nodeController.width())/2 ), self.__nodeController.y()-int((self.__valueAmount - self.__nodeController.height())/2), self.__valueAmount, self.__valueAmount)
        self.setStyleSheet("background-color: red; border: 3px solid blue;")
        self.setText(f"{self.__valueAmount}")
        self.__pix = QPixmap(self.size())
        self.show()