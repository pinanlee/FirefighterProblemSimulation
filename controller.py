#!/usr/bin/env python
# coding: utf-8
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets, QtCore, QtGui
import random
import math
from UIv2_ui import Ui_MainWindow
from FF import FireFighter
from node import Node 
from fire import Fire
from InformationWindow import InformationWindow
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5 import uic
import pandas as pd
import numpy as np
'''
information table跑不出來 
取消選取功能
提示視窗有誤
'''

travel_time = [[]]

def readExcel():
    df = pd.read_excel("coordinates data.xlsx")
    df_num = len(df.index)
    for i in range(df_num):
        travel_time.append([])
    df = pd.read_excel("adjacent data.xlsx")
    for j in df.iloc:
        travel_time[ord(j["i"])-64].append([ord(j["j"])-64, 1])
        travel_time[ord(j["j"])-64].append([ord(j["i"])-64, 1]) 
readExcel()

FFNum = 2

class MainWindow_controller(QtWidgets.QMainWindow):
    fire : Fire = None
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 2
    selectedStyle : str = "border: 2px solid blue;"
    FFindex = 0    
    focusIndex = 14
    labels : QtWidgets.QLabel = []
    timer = QTimer()
    currentTime = 0
    pageList = -1
    xPositionList = [[]]
    yPositionList = [[]]

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        df = pd.read_excel("coordinates data.xlsx")
        df_num = len(df.index)
        for i in range(df_num):
            image = QtWidgets.QLabel(self.ui.centralwidget)
            image.setGeometry(QtCore.QRect(df.iloc[i]["x"], df.iloc[i]["y"], 101, 101))
            nodePos = QtCore.QRect(df.iloc[i]["x"], df.iloc[i]["y"], 61, 51)
            nodeButton = Node(self.ui.centralwidget, image, i+1, nodePos)
            self.nodeList.append(nodeButton)

        global FFNum
        self.firefighterNum = FFNum
        self.nw = InformationWindow()
        self.subwindows = []
        self.setup_control()

    def setup_control(self):
        # init UI
        self.focusIndex = len(self.nodeList) - 1
        self.initUI()
        # init network
        self.initNode()
        self.NodeConnection()
        self.randomFireAndDepot()


        self.updateStatus()
        for i in self.firefighterList:
            i.doneSignal.connect(self.updateStatus)
            i.protectSignal.connect(self.updateMinTime)

    def initUI(self):
        self.ui.actionnodes.triggered.connect(self.showInformationWindow)
        self.descriptionAnimate("choose vertices to save")
        self.ui.node_info_label.setVisible(False)
        self.nodeList[self.focusIndex].setFocus()
        self.labels = [self.ui.FFlabel, self.ui.FFlabel_2]
        self.statusLabels = [self.ui.statuslabel,self.ui.statuslabel_2]
        self.ui.FFlabel.setPixmap(QPixmap("./image/firefighter.png"))
        self.ui.FFlabel_2.setPixmap(QPixmap("./image/fireman.png"))

    def updateStatus(self):
        for i in range(self.firefighterNum):
            if(self.firefighterList[i].isTraveling()):
                self.statusLabels[i].setText("Traveling")
            elif(self.firefighterList[i].isProcess()):
                self.statusLabels[i].setText("Processing")
            elif(self.firefighterList[i].isSelected()):
                self.statusLabels[i].setText("Selected")
            else:
                self.statusLabels[i].setText("Idle")

    def initNode(self):
        for i in self.nodeList:
            temp = random.randrange(5,11)
            i.clicked.connect(self.choose)       
            #i.updateAmount(temp)
            self.xPositionList.append(i.getXposition() + i.width() / 2)
            self.yPositionList.append(i.getYposition() + i.width() / 2)

    def randomFireAndDepot(self):
        def ySort(elem: Node):
            return elem.geometry().y()
        #random fire depot
        self.nodeList.sort(key=ySort)
        a = random.randint(0, len(self.nodeList)-1)
        self.fire = Fire(self.nodeList[a])
        self.updateMinTime()
        #init depot
        depot = self.nodeList[-1]
        for i in range(self.firefighterNum):
            ff = FireFighter(i+1, depot)
            depot.depotSetting()
            self.firefighterList.append(ff)
            
        self.firefighterList[1].pixmap = QPixmap("./image/fireman.png")
        self.nodeList[self.focusIndex].setStyleSheet("background-color: black;border: 2px solid blue;")

    def updateMinTime(self):
        for i in self.nodeList:
            self.fire.minTimeFireArrival(i)

    def NodeConnection(self):
        for i in self.nodeList:
            pos1 = np.array((i.geometry().x(),i.geometry().y()))
            for j in travel_time[i.getNum()]:
                pos2 = np.array((self.nodeList[j[0]-1].x(),self.nodeList[j[0]-1].y()))
                length = np.linalg.norm(pos1-pos2)
                print(length)
                i.connectNode(self.nodeList[j[0]-1], length)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.InfoDisable()
        if(a0.key()==Qt.Key_Enter-1):
            self.nextTime()
        elif(a0.key() == Qt.Key_A):
            self.buttonFocusStyle(-1)
        elif(a0.key() == Qt.Key_D):
            self.buttonFocusStyle(1)
        elif(a0.key() == Qt.Key_C):
            self.selectFireFighter()
        elif(a0.key() == Qt.Key_X):
            if(not self.ui.node_info_label.isVisible()):
                self.InfoShow()
        self.updateStatus()

    def buttonFocusStyle(self, plus):
        style = self.nodeList[self.focusIndex].styleSheet()
        result_string = ""
        for i in style.split(";"):
            if(i+";" != self.selectedStyle):
                result_string += i+";"
        self.nodeList[self.focusIndex].clearFocus()
        self.nodeList[self.focusIndex].setStyleSheet(result_string)
        self.focusIndex = (self.focusIndex + plus) % len(self.nodeList)
        style = self.nodeList[self.focusIndex].styleSheet()
        self.nodeList[self.focusIndex].setStyleSheet(style + self.selectedStyle)
        self.nodeList[self.focusIndex].setFocus()

    def nextFocus(self, plus):
        if(plus == 1):
            self.nodeList[self.focusIndex].geometry().x()

    def nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(10, 240))
        self.anim.setEndValue(QPoint(1200, 240))
        self.anim.setDuration(500)
        def start():
            self.anim.start()
        QTimer.singleShot(1000, start)  

    def descriptionAnimate(self, text):
        self.ui.descriptionLabel.setText(text)
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setEndValue(QPoint(10, 240))
        self.anim.setDuration(500)
        self.anim.start()

        self.anim.finished.connect(self.nextAnim)      
        self.ui.descriptionLabel.raise_()

    def InfoShow(self): #鼠標移到node時呼叫
        #移動label位置
        geo = self.nodeList[self.focusIndex].geometry()
        self.ui.node_info_label.setVisible(True)
        pos = QtCore.QRect(geo.x(), geo.y() + geo.width(), self.ui.node_info_label.frameRect().width(), self.ui.node_info_label.frameRect().height())
        self.ui.node_info_label.setGeometry(pos)
        self.ui.node_info_label.raise_()

        #處理顯示文字
        infotext = self.checkStatus(self.nodeList[self.focusIndex]) #檢查指定消防員是否可以移動到指定點
        text = infotext + "\nnode: {}, A = {}, L= ".format(self.nodeList[self.focusIndex].getNum(), self.nodeList[self.focusIndex].getWaterAmount())
        #取得arc長度
        if(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex]) == -1):
            text += "None"
        else:
            text += str(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"])
        self.ui.node_info_label.setText(text)


    #鼠標離開呼叫: 隱藏label
    def InfoDisable(self):
        self.ui.node_info_label.setVisible(False)

    def selectFireFighter(self): #選擇消防員
        prev = self.FFindex  
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].curPos().setImage(self.firefighterList[self.FFindex].pixmap)

        self.firefighterList[prev].closeaccessibleVisualize()
        self.firefighterList[self.FFindex].accessibleVisualize(self.nodeList)
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))

    def __opacitySet(self):
        def setOpacity(num, label):
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(num)
            label.setGraphicsEffect(opacity_effect)

        for i in range(self.firefighterNum):
            opacity = 1 if i == self.FFindex else 0.3
            setOpacity(opacity, self.firefighterList[i].curPos().getLabel())
            setOpacity(opacity, self.labels[i])
        setOpacity(1, self.firefighterList[self.FFindex].curPos().getLabel())

    def printStatus(func):
        def aa(self):
            ff = self.firefighterList[self.FFindex]
            if(ff.isSelected() and self.sender() != ff.destNode):
                text = "already selected"
            else:
                text = func(self)
                if(text == "vaild choose"):
                    self.sender().setText(str(self.firefighterList[self.FFindex].num))
            self.updateStatus()
            self.descriptionAnimate(text)
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        text = self.checkStatus(self.sender())
        if(text == "vaild choose"):
            if(self.firefighterList[self.FFindex].destNode == self.sender()):
                self.firefighterList[self.FFindex].reset()
                self.sender().setStyleSheet("")
                return "{} reset".format(self.firefighterList[self.FFindex].getName())
            text = self.firefighterList[self.FFindex].processCheck(self.sender())
            return text
        return text

    def checkStatus(self, node):
        if(self.firefighterList[self.FFindex].isProcess()):
            return "this firefighter is processing"
        if(self.firefighterList[self.FFindex].isTraveling()):
            return "this firefighter is moving"
        if(node == self.firefighterList[self.FFindex].curPos()):
            return "vaild choose"
            #check if selected FireFighter can move to assigned Node
        text = self.firefighterList[self.FFindex].next_Pos_Accessment(node)
        return text
        
    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():
            text = "moving"
            for i in range(self.currentTime % 3):
                text += "."
            self.descriptionAnimate(text)  
            self.upadateInformation()
            self.currentTime+=1
            self.fire.fire_spread(self.currentTime)
            for i in self.firefighterList:
                if(i.checkArrival(self.currentTime)):
                    self.timer.stop()
            self.__opacitySet()
            self.ui.timeIndexLabel.setText("t= "+str(self.currentTime))

        for i in self.firefighterList:
            if(not (i.isTraveling() or i.isProcess())):
                i.finishTimeSet()
            i.move(self.currentTime)
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(timeSkip)
        self.timer.start()

    def showInformationWindow(self):
        self.upadateInformation()
        self.nw.show()
        self.subwindows.append(self.nw)

    def onSubWindowPageChanged(self, index):
        self.pageList = index
   
    def upadateInformation(self):
        self.nw.pageChanged.connect(self.onSubWindowPageChanged)
        temp = self.nw.updateOutputMatrix(self.nodeList,self.firefighterList)
        temp2 = self.nw.setSetupMatrix(self.nodeList, self.firefighterNum,
                                    self.firefighterList[self.FFindex].rate_extinguish,
                                    self.firefighterList[self.FFindex].move_man, self.fire.rate_fireburn,
                                    self.fire.move_fire)
        self.nw.inputmatrix = temp
        self.nw.setupmatrix = temp2
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        self.nw.ui()
        self.nw.tab_widget.setCurrentIndex(self.pageList)

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpen = QPen(Qt.darkGray, 2, Qt.SolidLine)
        qpainter.setPen(qpen)

        for i in self.nodeList:
            for j in i.getNeighbors():
                qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[j.getNum()], self.yPositionList[j.getNum()]))
                i.getXposition() + i.width()/2

        for i in self.nodeList:
            if(i.isBurned()):
                for j in i.getNeighbors():
                    tempXpercent = (self.xPositionList[j.getNum()] - self.xPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)
                    tempYpercent = (self.yPositionList[j.getNum()] - self.yPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)

                    qpen.setColor(Qt.red)
                    qpen.setWidth(6)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[i.getNum()]+tempXpercent ,self.yPositionList[i.getNum()]+tempYpercent))

        for i in self.nodeList:
                for j in i.getNeighbors():
                    tempXpercent = (self.xPositionList[j.getNum()] - self.xPositionList[i.getNum()]) * i.getArcPercentage_FF(j)
                    tempYpercent = (self.yPositionList[j.getNum()] - self.yPositionList[i.getNum()]) * i.getArcPercentage_FF(j)

                    qpen.setColor(Qt.darkGreen)
                    qpen.setWidth(6)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[i.getNum()]+tempXpercent ,self.yPositionList[i.getNum()]+tempYpercent))

        self.update()
        qpainter.end()

    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        for subwindow in self.subwindows:
            subwindow.close()  # Close all open subwindows
        event.accept()



