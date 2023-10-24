from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets
from PyQt5 import uic
import os


class resultsWindow(QtWidgets.QMainWindow):

    def __init__(self, nodes, t):
        super().__init__()
        uic.loadUi("gameOver_window.ui",self)
        self.setGeometry(400,100,1100,800)

        self.folder_path = "image/timescreenshot"
        self.timestampList = []
        for _, _, files in os.walk(self.folder_path):
            for file_name in files:
                file_path = "image/timescreenshot/" + file_name
                self.timestampList.append(file_path)

        text = "Protected: \n"
        value = 0
        ctr = 1
        for i in nodes:
            if(i.isBurned()):
                text += ""
            else:
                if(ctr % 3 == 0):
                    text += "\n"
                value += i.getValue()
                text += "node {}, ".format(i.getNum())
                ctr+=1
        self.nodeLabel.setText(text)

        self.valueLabel.setText("Protected value: {}".format(value))
        self.timeLabel.setText("Finish time: {}".format(t))

        self.toolButton_next.setArrowType(Qt.RightArrow)
        self.toolButton_pre.setArrowType(Qt.LeftArrow)
        self.button_start.clicked.connect(self.startAnimation)
        self.button_stop.clicked.connect(self.stopAnimation)
        self.toolButton_next.clicked.connect(self.nextImage)
        self.toolButton_pre.clicked.connect(self.preImage)
        self.totalTime = t
        self.currrentTime = 0
        self.setImage()
        self.setCurrentTime()
        print(f'self.totalTime{self.totalTime}')




    def startAnimation(self):
        def animation():
            self.currrentTime = (self.currrentTime+1)%self.totalTime
            self.setImage()
            self.setCurrentTime()

        self.timer_animation = QTimer()
        self.timer_animation.setInterval(300)
        self.timer_animation.timeout.connect(animation)
        self.timer_animation.start()

    def stopAnimation(self):
        self.timer_animation.stop()

    def nextImage(self):
        self.currrentTime = (self.currrentTime+1) % self.totalTime
        self.setImage()
        self.setCurrentTime()



    def preImage(self):
        self.currrentTime = (self.currrentTime-1) % self.totalTime
        self.setImage()
        self.setCurrentTime()


    def setImage(self):
        displayImage = QPixmap(self.timestampList[self.currrentTime])
        scaledImage = displayImage.scaled(self.label_display.width(), self.label_display.height())
        self.label_display.setPixmap(scaledImage)
        self.label_display.update()
        self.setCurrentTime()

    def setCurrentTime(self):
        text = "Time: {} ".format(self.currrentTime)
        self.currentTimeLabel.setText(text)







