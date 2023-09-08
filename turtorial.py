#!/usr/bin/env python
# coding: utf-8
import json
import os

from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsOpacityEffect,QVBoxLayout
from PyQt5 import QtWidgets, QtCore, QtGui
import random
import math

from FFSettingsWindow import FFSettingsWindow
from FFSettingsWindow import FFnumWindow
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
from results import resultsWindow
import sys

FFNum = 2


class turtorial(QtWidgets.QMainWindow):
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
    FFInfoDict = []
    turtorialWindow = None
    turtorialList = [
        "This is a firefighter problem simulation. In this simulation, you are a firefighter manager, trying to contruct barriers in order to contain the fire spreading in a given network",
        "You need to create a barrier by assigning every firefighter to some specific positions, and defend it",
        "Let's begin with some basics",
        "This is a depot, where firefighters start their mission",
        "Press C to change the select firefighter",
        "You can see hidden firefighters by pressing C, so don't be panic if there is some firefighters missing in the network",
        "\"Blue\" nodes indicate that this node is accessable by selected firefighter, in this example, there is only one option for both firefighters",
        "Click the blue node to assign selected firefighter to there",
        "Firefighter 1 has assigned to node 7, let's try assigning another firefighter to the same node",
        "All firefighter has assigned to a destination, press \"Enter\" to move!"
    ]
    turtorialing = True
    turtorialIndex = 0
    practice = False
    def __init__(self, window):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.mainWindow = window
        global FFNum
        uic.loadUi("UIv4.ui",self)
        #self.centralWidget().setGeometry(self.geometry())
        if os.path.exists("FFInfo.json"):
            with open("FFInfo.json", 'r') as file:
                data = json.load(file)
            FFNum = int(data["FFnumber"])
        self.db = DataBase()
        self.nw = InformationWindow(self.db)
        self.firefighterNum = FFNum
        self.subwindows = []
        self.setup_control()
        self.window_FFnum = FFnumWindow()
        self.window_FFnum.window_FF.updateFFnumSignal.connect(self.newFFnum)
        self.hintLabel.setText(self.turtorialList[self.turtorialIndex])
        self.hintLabel.raise_()
        self.consoleLabel.raise_()

    '''------------------------------------初始化--------------------------------------------------------'''
    
    def nextPage(self):
        self.turtorialIndex+=1
        self.hintLabel.setText(self.turtorialList[self.turtorialIndex])
        if(self.turtorialIndex == 3):
            self.hintLabel.setGeometry(self.nodeList[-1].x(), self.nodeList[-1].y()+50,self.hintLabel.width(),self.hintLabel.height())
        elif(self.turtorialIndex == 6):
            self.hintLabel.setGeometry(self.FFnetwork.nodeList[6].pos.x(), self.FFnetwork.nodeList[6].pos.y()+50,self.hintLabel.width(),self.hintLabel.height())
        elif(self.turtorialIndex == 8 or self.turtorialIndex == 9):
            self.turtorialing = False
            self.practice = True            
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if(self.turtorialing):
            self.nextPage()
        if(self.turtorialIndex == 4 or self.turtorialIndex == 7 ):
            self.turtorialing = False
            self.practice = True
            
    def setup_control(self):
        def initNetwork(): #建立network class和node
            self.backgroundLabel.setStyleSheet("background-color: rgba(200, 200, 200, 100);")
            self.FFnetwork = Network("G15_fire_route_example.xlsx", "G15_nodeInformation_example.xlsx")
            self.fireNetwork = Network("G15_firefighter_route_example.xlsx", "G15_nodeInformation_example.xlsx")
            for i in self.FFnetwork.nodeList:
                node = Node(self.centralwidget, i)
                node.clicked.connect(self.choose)
                self.nodeList.append(node)
                #self.gridLayout.addWidget(node)
        initNetwork()
        self.nodeNum = len(self.nodeList)
        self.db.numNode = self.nodeNum


        def initUI(): # UI設定(可略)
            self.focusIndex = len(self.nodeList) - 1
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.7)
            self.descriptionLabel.setGraphicsEffect(opacity_effect)
            
            self.actionProblem.triggered.connect(self.showProblem)
            self.actionControls.triggered.connect(self.showControls)
            self.actionAnimation.triggered.connect(self.showFFWindow)
            self.actionNew.triggered.connect(self.newNetwork)
            self.backButton.clicked.connect(self.back)
            #self.descriptionAnimate("choose vertices to save")
            self.node_info_label.setVisible(False)
            self.nodeList[self.focusIndex].setFocus()

        initUI()
        self.showInformationWindow()

        def NodeConnection():
            for i in self.nodeList:
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
            a = 13
            self.fire.append(Fire(self.fireNetwork, a, self.currentTime))
            self.fire[-1].burnedSignal.connect(self.networkUpdateF)
            self.fire[-1].opacitySignal.connect(self.fireVisualize)
            self.fire[-1].terminateSignal.connect(self.finish)
            self.fire[-1].burn()
            self.updateMinTime()

            #初始化消防員
            depot = self.nodeList[-1]
            if os.path.exists("FFInfo.json"): #若有自定義的情況
                with open("FFInfo.json", 'r') as file:
                    data = json.load(file)
                self.FFInfoDict = data["FFinfo"]
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.centralwidget, i+1, depot)
                    ff.FFdoneSignal.connect(self.updateFFStatus)
                    ff.FFprotectSignal.connect(self.updateMinTime)
                    ff.FFprotectSignal.connect(self.networkUpdate)
                    ff.FFidleSignal.connect(self.updateNodeIdle)
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                self.networkUpdate(depot.getNum())
                self.nodeList[self.focusIndex].setStyleSheet("background-color: black;border: 2px solid blue;")
                for i in self.firefighterList:
                    tempNum = i.num
                    pixmap = QPixmap(self.FFInfoDict[tempNum-1]["img"])
                    scaled_pixmap = pixmap.scaled(self.labels[tempNum-1].size(), aspectRatioMode=Qt.KeepAspectRatio,
                                                  transformMode=Qt.SmoothTransformation)
                    i.setPixmap(scaled_pixmap)
                    i.rate_extinguish = int(self.FFInfoDict[tempNum-1]["er"])
                    i.move_man = int(self.FFInfoDict[tempNum-1]["ts"])
            else:
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.centralwidget, i+1, depot)
                    ff.FFdoneSignal.connect(self.updateFFStatus)
                    ff.FFprotectSignal.connect(self.updateMinTime)
                    ff.FFprotectSignal.connect(self.networkUpdate)
                    ff.FFidleSignal.connect(self.updateNodeIdle)
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                self.networkUpdate(depot.getNum())
                self.firefighterList[1].setPixmap(QPixmap("./image/fireman.png"))
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

    def back(self):
        self.mainWindow.show()
        self.close()

    def turtorial(self):
        self.turtorialWindow = turtorial()
        self.turtorialWindow.show()
        self.close()

    def intoGame(self):
        self.setStyleSheet("")

        
    def showProblem(self):
        self.instruct.setGeometry(300,50,600,600)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.instruct.setFont(font)
        self.instruct.setText("This is a firefighter simulation problem")
        self.noButton.setGeometry(799,599,101,51)
        self.noButton.setText("back to game")

    def showControls(self):
        self.instruct.setGeometry(300,50,600,600)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.instruct.setFont(font)
        self.instruct.setAlignment(QtCore.Qt.AlignLeft)
        self.instruct.setText("Instructions:\n\n"+
        "Enter: \n\tMove to next time\n"+
        "C: \n\tChange selected firefighter\n"+
        "A, D: \n\tChange selected node\n"+
        "Space: \n\tAssign firefighter to selected node\n"
        +"S: \n\tChange the view of network\n")
        self.noButton.setGeometry(799,599,101,51)
        self.noButton.setText("back to game")

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
            #print("node {}: {}".format(i.getNum(), i.fireMinArrivalTime))


    def updateFFStatus(self): #消防員移動/澆水完成時呼叫，更新消防員的狀態
        for i in range(self.firefighterNum):
            if(self.firefighterList[i].isTraveling()):
                #self.statusLabels[i].setText("Traveling to Node {}".format(self.firefighterList[i].destNode.getNum()))
                if (i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Traveling to Node {}".format(self.firefighterList[i].destNode.getNum())
                elif (i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Traveling to Node {}".format(self.firefighterList[i].destNode.getNum())
            elif(self.firefighterList[i].isProcess()):
                #self.statusLabels[i].setText("Processing Node {}".format(self.firefighterList[i].destNode.getNum()))
                if (i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Processing Node {}".format(self.firefighterList[i].destNode.getNum())
                elif (i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Processing Node {}".format(self.firefighterList[i].destNode.getNum())
            elif(self.firefighterList[i].isSelected()):
                #self.statusLabels[i].setText("Selected Node {}".format(self.firefighterList[i].destNode.getNum()))
                if(i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Selected Node {}".format(self.firefighterList[i].destNode.getNum())
                elif(i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Selected Node {}".format(self.firefighterList[i].destNode.getNum())
            else:
                #self.statusLabels[i].setText("Idle")
                if(i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Idle"
                elif(i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Idle"
        self.iw_pageCP_FF()



    def updateNodeIdle(self,value):
        for i in self.fireNetwork.nodeList:
            if(i.getNum() == value):
                i.ffidle()


    '''------------------------------------------fire signal---------------------------------------------'''
    def networkUpdateF(self,value): #當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        for i in self.nodeList:
            if(i.getNum() == value):
                i.onFire()
                self.fire.append(Fire(self.fireNetwork, value, self.currentTime))
                self.fire[-1].burnedSignal.connect(self.networkUpdateF)
                self.fire[-1].opacitySignal.connect(self.fireVisualize)
                self.fire[-1].terminateSignal.connect(self.finish)

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        for i in self.fireNetwork.nodeList:
            if(i.getNum() == no):
                tempGrass = i.getGrassAmount()
                i.updateStatus()
        for i in self.nodeList:
            if(i.getNum()== no):
                i.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
                i.updateGrassAmount(tempGrass)
                i.updateStatus()

    def finish(self):
        self.timer.stop()
        self.result = resultsWindow(self.nodeList, self.currentTime)
        self.result.show()


    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if(self.practice):
            self.node_info_label.setVisible(False)
            if(a0.key()==Qt.Key_Enter-1):
                    self.nextTime()
            elif(a0.key() == Qt.Key_A):
                self.buttonFocusStyle(-1)
                self.iw_pageCP_node()
            elif(a0.key() == Qt.Key_D):
                self.buttonFocusStyle(1)
                self.iw_pageCP_node()
            elif(a0.key() == Qt.Key_C):
                if(self.practice):
                    self.selectFireFighter()
                    if(self.turtorialIndex == 4):
                        self.turtorialing = True
                        self.practice = False
                        self.nextPage()
                #self.iw_pageCP_FF()
            elif(a0.key() == Qt.Key_X):
                if(not self.node_info_label.isVisible()):
                    self.InfoShow()
            elif(a0.key() == Qt.Key_S):
                    self.networkChange()
            elif(a0.key() == Qt.Key_N):
                self.newNetwork()
            elif(a0.key() == Qt.Key_Q):
                self.finish()
            elif(a0.key() == Qt.Key_L):
                self.firefighterList[self.FFindex].lock()
                if(self.firefighterList[self.FFindex].idleLock):
                    self.descriptionAnimate("FF {} : idle locked".format(self.FFindex+1))
                else:
                    self.descriptionAnimate("FF {} : idle unlocked".format(self.FFindex+1))
        self.updateFFStatus()

    def newNetwork(self):
        import subprocess
        import os
        subprocess.call("GenerateGraph.py", shell=True)
        p = sys.executable
        os.execl(p, p, *sys.argv)

    def newFFnum(self):
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)

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
            self.networkLabel.setText("FF network")
        elif(self.showFFnetwork and not self.showFireNetwork):
            self.showFFnetwork = False
            self.showFireNetwork = True
            self.networkLabel.setText("Fire network")
        elif(not self.showFFnetwork and self.showFireNetwork):
            self.showFFnetwork = True
            self.networkLabel.setText("Hybrid network")

    def nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(310, 240))
        self.anim.setEndValue(QPoint(2200, 240))
        self.anim.setDuration(250)
        def start():
            self.anim.start()
        QTimer.singleShot(800, start)  

    def descriptionAnimate(self, text):
        self.descriptionLabel.setText(text)
        self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
        self.anim.setEndValue(QPoint(310, 240))
        self.anim.setDuration(250)
        self.anim.start()

        self.anim.finished.connect(self.nextAnim)      
        self.descriptionLabel.raise_()

    def InfoShow(self): #查看node資訊
        #移動label位置
        geo = self.nodeList[self.focusIndex].geometry()
        self.node_info_label.setVisible(True)
        pos = QtCore.QRect(geo.x(), geo.y() + geo.width(), self.node_info_label.frameRect().width(), self.node_info_label.frameRect().height())
        self.node_info_label.setGeometry(pos)
        self.node_info_label.raise_()

        #處理顯示文字
        infotext = self.checkStatus(self.nodeList[self.focusIndex]) #檢查指定消防員是否可以移動到指定點
        text = infotext + "\nnode: {}, A = {}, L= ".format(self.nodeList[self.focusIndex].getNum(), self.nodeList[self.focusIndex].getWaterAmount())
        #取得arc長度
        if(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex]) == -1):
            text += "None"
        else:
            text += str(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"])
        self.node_info_label.setText(text)

    def iw_pageCP_node(self):
        #part node
        self.nw.title_label_node_des.setText(str(self.nodeList[self.focusIndex].getNum()))

        if (self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex]) == -1):
            self.nw.nodeblock_textlen = "Not neighbor"
            temptta = "Not neighbor"
        else:
            self.nw.nodeblock_textlen = str(math.ceil(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"]))
            templen = self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"]
            tempextRate = self.firefighterList[self.FFindex].move_man
            temptta = math.ceil(self.currentTime + templen / tempextRate)

        self.nw.title_label_length_des.setText(self.nw.nodeblock_textlen)
        self.nw.title_label_tta_des.setText(str(temptta))
        tempttb = self.nodeList[self.focusIndex].getFireMinArrivalTime()
        self.nw.title_label_ttb_des.setText(str(tempttb))
        self.nw.nodeblock_textsta =  self.nodeList[self.focusIndex].getStatus()
        self.nw.title_label_sta_des.setText(self.nw.nodeblock_textsta)

        if(self.nw.nodeblock_textsta == "Burned"):
            self.nw.nodeCircle.setStyleSheet("background-color: red;")
        elif (self.nw.nodeblock_textsta == "Damaged"):
            self.nw.nodeCircle.setStyleSheet("background-color: darkred;")
        elif (self.nw.nodeblock_textsta == "Safe"):
            self.nw.nodeCircle.setStyleSheet("background-color: darkgreen;")
        elif(self.nw.nodeblock_textsta == "Protected"):
            self.nw.nodeCircle.setStyleSheet("background-color: green;")
        else:
            self.nw.nodeCircle.setStyleSheet("background-color: white;")

    def iw_pageCP_FF(self):
        #part FF
        self.nw.ffblockCP_img1 = self.firefighterList[self.FFindex].grab()
        self.nw.ffblockCP_name1 = self.firefighterList[self.FFindex].getName()
        self.nw.ffblockCP_wr1 = str(self.firefighterList[self.FFindex].rate_extinguish)
        self.nw.ffblockCP_img2 = self.firefighterList[self.nextFFindex].grab()
        self.nw.ffblockCP_name2 = self.firefighterList[self.nextFFindex].getName()
        self.nw.ffblockCP_wr2 = str(self.firefighterList[self.nextFFindex].rate_extinguish)
        self.nw.pageCP_generateblockFF()


    def selectFireFighter(self): #切換選擇消防員
        self.prevFFindex = self.FFindex
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        self.nextFFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].setPixmap(self.firefighterList[self.FFindex].grab())
        self.firefighterList[self.prevFFindex].closeaccessibleVisualize()
        self.firefighterList[self.FFindex].accessibleVisualize(self.currentTime)
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))

    def __opacitySet(self): #調整FF的opacity
        def setOpacity(num, label):
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(num)
            label.setGraphicsEffect(opacity_effect)

        for i in range(self.firefighterNum):
            opacity = 1 if i == self.FFindex else 0.3
            setOpacity(opacity, self.firefighterList[i])
            #setOpacity(opacity, self.labels[i])
        setOpacity(1, self.firefighterList[self.FFindex])

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
            #if(self.practice):
            #    self.descriptionAnimate(text)
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        if(self.practice):
            text = self.checkStatus(self.sender()) #檢查選擇的node是否符合限制
            if(text == "vaild choose"):
                if(self.firefighterList[self.FFindex].destNode == self.sender()): #是否選擇取消(再次點擊同node)
                    self.firefighterList[self.FFindex].reset()
                    self.sender().setStyleSheet("")
                    return "{} reset".format(self.firefighterList[self.FFindex].getName())
                if(self.turtorialIndex == 7 or self.turtorialIndex == 8):
                    self.practice = False
                    self.turtorialing = True
                    self.nextPage()
                text = self.firefighterList[self.FFindex].processCheck(self.sender())
                self.descriptionAnimate(text)
                return text
            return text
        return ""

    def checkStatus(self, node):
        if(self.firefighterList[self.FFindex].isProcess()):
            return "this firefighter is processing"
        if(self.firefighterList[self.FFindex].isTraveling()):
            return "this firefighter is moving"
        if(node == self.firefighterList[self.FFindex].curPos()):
            return "vaild choose"
            #check if selected FireFighter can move to assigned Node
        text = self.firefighterList[self.FFindex].next_Pos_Accessment(node, self.currentTime)
        return text
        
    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():
            ctr = 0
            for i in self.fire:
                if(i.finishSpread):
                    ctr+=1
            print("ctr: {}, all: {}".format(ctr, len(self.fire)))
            if(ctr == len(self.fire)):
                self.finish()
            self.dataRecord()
            text = "moving"
            for i in range(self.currentTime % 3):
                text += "."
            self.descriptionAnimate(text)  
            self.upadateInformation()
            self.currentTime+=1
            for i in self.fire:
                i.fire_spread(self.currentTime)
            for i in self.firefighterList:
                if(i.checkArrival(self.currentTime)):
                    self.timer.stop()
                    self.nextPage()
            self.__opacitySet()
            self.timeIndexLabel.setText("t= "+str(self.currentTime))

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
        # if os.path.exists("FFInfo.json"):
        #     os.remove("FFInfo.json")
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
        self.currentTime = self.db.currentTime-1
        self.FFnetwork.nodeList = self.db.ffnetworkNodeList[self.currentTime]
        self.fireNetwork.nodeList = self.db.fireNetworkNodeList[self.currentTime]
        self.nodeList = self.db.controllerNodeList[self.currentTime]
        self.updateFFStatus()
        self.updateMinTime()

    def showFFWindow(self):
        self.subwindows.append(self.window_FFnum)
        self.subwindows.append(self.window_FFnum.window_FF)
        self.window_FFnum.show()





