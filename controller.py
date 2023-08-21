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
from fireObject import Fire
from network import Network
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5 import uic
import pandas as pd
import numpy as np
from dataBase import DataBase
from informationWindow import  InformationWindow

'''
information table跑不出來 

提示視窗有誤
'''

FFNum = 2

class MainWindow_controller(QtWidgets.QMainWindow):
    fire : list[Fire] = []
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 2
    nodeNum = len(nodeList)
    selectedStyle : str = "border: 2px solid blue;"
    FFindex = 0 
    focusIndex = 14
    labels : QtWidgets.QLabel = []
    statusLabels = []
    timer = QTimer()
    currentTime = 0
    pageList = -1
    FFnetwork : Network = None
    fireNetwork : Network = None
    showFFnetwork : bool = True
    showFireNetwork : bool = True
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DataBase()
        self.nw = InformationWindow(self.db)
        global FFNum
        self.firefighterNum = FFNum
        self.subwindows = []
        self.setup_control()



    '''------------------------------------初始化--------------------------------------------------------'''
    def setup_control(self):
        def initNetwork(): #建立network class和node
            self.ui.backgroundLabel.setStyleSheet("background-color: rgba(200, 200, 200, 100);")
            self.FFnetwork = Network("adjacent data -- ff.xlsx", "coordinates data.xlsx")
            self.fireNetwork = Network("adjacent data -- fire.xlsx", "coordinates data.xlsx")
            for i in self.FFnetwork.nodeList:
                image = QtWidgets.QLabel(self.ui.centralwidget)
                node = Node(self.ui.centralwidget, image, i)
                node.clicked.connect(self.choose)
                self.nodeList.append(node)
        initNetwork()
        self.nodeNum = len(self.nodeList)
        self.db.numNode = self.nodeNum
        print(f'self.nodeNum{self.nodeNum}')


        def initUI(): # UI設定(可略)
            self.focusIndex = len(self.nodeList) - 1
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.7)
            self.ui.descriptionLabel.setGraphicsEffect(opacity_effect)
            self.ui.actionnodes.triggered.connect(self.showInformationWindow)
            self.descriptionAnimate("choose vertices to save")
            self.ui.node_info_label.setVisible(False)
            self.nodeList[self.focusIndex].setFocus()
            self.labels = [self.ui.FFlabel, self.ui.FFlabel_2]
            self.statusLabels = [self.ui.statuslabel,self.ui.statuslabel_2]
            self.ui.FFlabel.setPixmap(QPixmap("./image/firefighter.png"))
            self.ui.FFlabel_2.setPixmap(QPixmap("./image/fireman.png"))
        initUI()
        self.showInformationWindow()

        def NodeConnection():
            for i in self.nodeList:
                '''for j in self.FFnetwork.nodeList:
                    if(i.getNum() == j.getNum()):
                        i.connectNode(j.getArcs())'''
                pos1 = np.array((i.geometry().x(),i.geometry().y()))
                for j in self.FFnetwork.adjList[i.getNum()]:
                    pos2 = np.array((self.nodeList[j[0]-1].x(),self.nodeList[j[0]-1].y()))
                    length = np.linalg.norm(pos1-pos2)
                    i.connectNode(self.nodeList[j[0]-1], length)
        NodeConnection()

        def randomFireAndDepot(): #初始化火和消防員
            def ySort(elem: Node):
                return elem.geometry().y()
            #初始化火
            self.nodeList.sort(key=ySort)
            a = random.randint(0, len(self.nodeList)-2)
            self.fire.append(Fire(self.fireNetwork, a))
            self.fire[-1].burnedSignal.connect(self.networkUpdateF)
            self.fire[-1].opacitySignal.connect(self.fireVisualize)
            self.fire[-1].burn()
            self.updateMinTime()
            #初始化消防員
            depot = self.nodeList[-1]
            for i in range(self.firefighterNum):
                ff = FireFighter(i+1, depot)
                ff.FFdoneSignal.connect(self.updateFFStatus)
                ff.FFprotectSignal.connect(self.updateMinTime)
                ff.FFprotectSignal.connect(self.networkUpdate)
                ff.FFidleSignal.connect(self.updateNodeIdle)
                depot.depotSetting()
                self.firefighterList.append(ff)
            self.networkUpdate(depot.getNum())
            self.firefighterList[1].pixmap = QPixmap("./image/fireman.png")
            self.nodeList[self.focusIndex].setStyleSheet("background-color: black;border: 2px solid blue;")
        randomFireAndDepot()

        self.selectFireFighter()
        self.updateFFStatus()

        def databaseInit():
            self.nw.numFF = self.firefighterNum
            self.db.numFF = self.firefighterNum
            self.db.numNode = len(self.nodeList)

        databaseInit()
        self.dataRecord()

    '''---------------------------------------firefighter signal-----------------------------------------'''
    def networkUpdate(self,value): #FF network有節點被保護時呼叫，更新fire network
        for i in self.fireNetwork.nodeList:
            if(i.getNum() == value):
                i.defend()
        self.updateMinTime()

    def updateMinTime(self): #更新FF network的fireMinArrivalTime
        for i in self.fireNetwork.nodeList:
            i.fireMinArrivalTime = 10000

        for i in self.fire:
            i.minTimeFireArrival(self.currentTime)
        for i in self.FFnetwork.nodeList:
            i.fireMinArrivalTime = self.fireNetwork.nodeList[i.getNum()-1].fireMinArrivalTime

    def updateFFStatus(self): #消防員移動/澆水完成時呼叫，更新消防員的狀態
        for i in range(self.firefighterNum):
            if(self.firefighterList[i].isTraveling()):
                self.statusLabels[i].setText("Traveling to\nNode {}".format(self.firefighterList[i].destNode.getNum()))
            elif(self.firefighterList[i].isProcess()):
                self.statusLabels[i].setText("Processing\nNode {}".format(self.firefighterList[i].destNode.getNum()))
            elif(self.firefighterList[i].isSelected()):
                self.statusLabels[i].setText("Selected\nNode {}".format(self.firefighterList[i].destNode.getNum()))
            else:
                self.statusLabels[i].setText("Idle")
    def updateNodeIdle(self,value):
        for i in self.fireNetwork.nodeList:
            if(i.getNum() == value):
                i.ffidle()


    '''------------------------------------------fire signal---------------------------------------------'''
    def networkUpdateF(self,value): #當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        for i in self.nodeList:
            if(i.getNum() == value):
                i.onFire()
                self.fire.append(Fire(self.fireNetwork, value))
                self.fire[-1].burnedSignal.connect(self.networkUpdateF)
                self.fire[-1].opacitySignal.connect(self.fireVisualize)

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        for i in self.nodeList:
            if(i.getNum()== no):
                i.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')

    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.ui.node_info_label.setVisible(False)
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
        elif(a0.key() == Qt.Key_S):
                self.networkChange()
        self.updateFFStatus()

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

    def networkChange(self):
        if(self.showFFnetwork and self.showFireNetwork):
            self.showFireNetwork = False
            self.ui.networkLabel.setText("FF network")
        elif(self.showFFnetwork and not self.showFireNetwork):
            self.showFFnetwork = False
            self.showFireNetwork = True
            self.ui.networkLabel.setText("Fire network")
        elif(not self.showFFnetwork and self.showFireNetwork):
            self.showFFnetwork = True
            self.ui.networkLabel.setText("Hybrid network")

    def nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(10, 240))
        self.anim.setEndValue(QPoint(1200, 240))
        self.anim.setDuration(250)
        def start():
            self.anim.start()
        QTimer.singleShot(800, start)  

    def descriptionAnimate(self, text):
        self.ui.descriptionLabel.setText(text)
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setEndValue(QPoint(10, 240))
        self.anim.setDuration(250)
        self.anim.start()

        self.anim.finished.connect(self.nextAnim)      
        self.ui.descriptionLabel.raise_()

    def InfoShow(self): #查看node資訊
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

    def selectFireFighter(self): #切換選擇消防員
        prev = self.FFindex  
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].curPos().setImage(self.firefighterList[self.FFindex].pixmap)

        self.firefighterList[prev].closeaccessibleVisualize()
        self.firefighterList[self.FFindex].accessibleVisualize()
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))

    def __opacitySet(self): #調整FF的opacity
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
            self.updateFFStatus()
            self.descriptionAnimate(text)
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        text = self.checkStatus(self.sender()) #檢查選擇的node是否符合限制
        if(text == "vaild choose"):
            if(self.firefighterList[self.FFindex].destNode == self.sender()): #是否選擇取消(再次點擊同node)
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
            self.dataRecord()
            text = "moving"
            for i in range(self.currentTime % 3):
                text += "."
            self.descriptionAnimate(text)  
            self.upadateInformation()
            self.currentTime+=1
            for i in self.fire:
                i.fire_spread()
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
        self.timer.setInterval(300)
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
        self.nw.tab_widget.setCurrentIndex(self.pageList)
        # x = self.nw.pos().x()
        # y = self.nw.pos().y()
        # self.nw.move(x, y)

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        
        if(self.showFFnetwork):
            qpen = QPen(Qt.black, 2, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                for j in i.getNeighbors():
                    qpainter.drawLine(QPointF(i.x() + i.width()/2, i.y()+ 3/2*i.height()), QPointF(j.x()+ j.width()/2, j.y()+ 3/2*j.height()))
        if(self.showFireNetwork):
            qpen = QPen(Qt.darkRed, 4, Qt.DashLine)
            qpen.setDashPattern([10, 50, 10, 50])
            qpainter.setPen(qpen)
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    qpainter.drawLine(QPointF(i.pos.x() + i.pos.width()/2, i.pos.y()+ 3/2*i.pos.height()), QPointF(j.pos.x()+ j.pos.width()/2, j.pos.y()+ 3/2*j.pos.height()))          

        for i in self.fire:
            for j in i.arcs:
                    tempXpercent = (j["node"].pos.x() + j["node"].pos.width()/2 - i.firePos.pos.x() - i.firePos.pos.width()/2) * i.getArcPercentage_Fire(j)
                    tempYpercent = (j["node"].pos.y() + 3/2*j["node"].pos.height() - i.firePos.pos.y() - 3/2*i.firePos.pos.height()) * i.getArcPercentage_Fire(j)
                    qpen = QPen(Qt.red, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(i.firePos.pos.x() + i.firePos.pos.width()/2, i.firePos.pos.y() + 3/2*i.firePos.pos.height()), QPointF(i.firePos.pos.x() + i.firePos.pos.width()/2 + tempXpercent, i.firePos.pos.y() + 3/2*i.firePos.pos.height() + tempYpercent))                 
        
        for i in self.firefighterList:
            if(i.curMovingArc != None):
                    tempXpercent = (i.curMovingArc["node"].x() + i.curMovingArc["node"].width()/2 - i.curPos().x() - i.curPos().width()/2) * i.getArcPercentage_FF(i.curMovingArc["node"])
                    tempYpercent = (i.curMovingArc["node"].y() + 3/2*i.curMovingArc["node"].height() - i.curPos().y() - 3/2*i.curPos().height()) * i.getArcPercentage_FF(i.curMovingArc["node"])
                    qpen = QPen(Qt.darkGreen, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(i.curPos().x() + i.curPos().width()/2, i.curPos().y() + 3/2*i.curPos().height()), QPointF(i.curPos().x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 3/2*i.curPos().height()+tempYpercent))                

        self.update()
        qpainter.end()

    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        for subwindow in self.subwindows:
            subwindow.close()  # Close all open subwindows
        event.accept()

    def dataRecord(self): #將資料傳入database
        self.db.currentTime = self.currentTime
        self.db.ffnetworkNodeList[self.currentTime] = self.FFnetwork.nodeList
        self.db.fireNetworkNodeList[self.currentTime]  = self.fireNetwork.nodeList
        self.db.controllerNodeList[self.currentTime]  = self.nodeList
        self.db.firefighterList[self.currentTime] = self.firefighterList
        self.db.infoNextTime()

    def loadRecord(self): #讀檔(未完成)
        print("active ")
        self.currentTime = self.db.currentTime-1
        print(f'self.currentTime{self.currentTime}')
        self.FFnetwork.nodeList = self.db.ffnetworkNodeList[self.currentTime]
        self.fireNetwork.nodeList = self.db.fireNetworkNodeList[self.currentTime]
        self.nodeList = self.db.controllerNodeList[self.currentTime]
        self.updateFFStatus()
        self.updateMinTime()
        self.syncFireMinArrivalTime()

