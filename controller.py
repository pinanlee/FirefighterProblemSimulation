#!/usr/bin/env python
# coding: utf-8
import json
import os
from functools import partial

from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF,pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QWidget
from PyQt5 import QtWidgets, QtCore, QtGui
import random
import math

from FFSettingsWindow import FFSettingsWindow
from FFSettingsWindow import FFnumWindow
from FF import FireFighter
from node import Node 
from fireObject import Fire
from network import Network
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QCursor, QPalette, QColor
from PyQt5 import uic
import pandas as pd
import numpy as np
from dataBase import DataBase
from informationWindow import  InformationWindow
from results import resultsWindow
from turtorial import turtorial
import sys

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
    timer = QTimer()
    currentTime = 0
    pageList = -1
    FFnetwork : Network = None
    fireNetwork : Network = None
    showFFnetwork : bool = True
    showFireNetwork : bool = True
    FFInfoDict = []
    turtorialWindow = None
    totalValue = 0
    availFF = 0
    assignedFF = 0
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        
        global FFNum
        uic.loadUi("UIv4.ui",self)
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
        self.block_completelist = []



    '''------------------------------------初始化--------------------------------------------------------'''
    def setup_control(self):
        def initNetwork(): #建立network class和node
            self.backgroundLabel.setStyleSheet("background-color: rgba(200, 200, 200, 100);")
            self.FFnetwork = Network("network/G30_fire_route.xlsx", "network/G30_nodeInformation.xlsx")
            self.fireNetwork = Network("network/G30_firefighter_route.xlsx", "network/G30_nodeInformation.xlsx")
            for i in self.FFnetwork.nodeList:
                node = Node(self.centralwidget, i)
                node.clicked.connect(self.choose)
                node.showSignal.connect(self.InfoShow)
                self.nodeList.append(node)
                self.totalValue+=node.getValue()
            self.progressBar.setMaximum(self.totalValue)
            self.progressBar.setValue(self.totalValue)
        initNetwork()
        self.nodeNum = len(self.nodeList)
        self.db.numNode = self.nodeNum


        def initUI(): # UI設定(可略)
            self.setStyleSheet("background-color: rgb(100, 100, 100);")
            self.hintLabel.setGeometry(-100,-300, self.hintLabel.width(),self.hintLabel.height())
            self.focusIndex = len(self.nodeList) - 1
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.7)
            self.descriptionLabel.setGraphicsEffect(opacity_effect)
            self.actionProblem.triggered.connect(self.showProblem)
            self.actionControls.triggered.connect(self.showControls)
            self.actionAnimation.triggered.connect(self.showFFWindow)
            self.actionNew.triggered.connect(self.newNetwork)
            self.yesButton.clicked.connect(self.turtorial)
            self.node_info_label.setVisible(False)
            self.nodeList[self.focusIndex].setFocus()
            self.instruct.raise_()
            self.yesButton.raise_()
            self.noButton.raise_()
            self.yesButton.clicked.connect(self.intoGame)
            self.noButton.clicked.connect(self.intoGame)
            self.idleButton.clicked.connect(self.assignIdle)
            self.defendButton.clicked.connect(self.choose)
            self.checkBox.toggled.connect(self.idleLock)
            self.lcd_time.display(self.currentTime)
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
            #初始化火
            for i in self.FFnetwork.nodeList:
                if(not i.getArcs()):
                    a = i.getNum()
            self.fire.append(Fire(self.fireNetwork, a, self.currentTime))
            self.fire[-1].fireSignal.connect(self.fireSignalDetermination)
            '''self.fire[-1].burnedSignal.connect(self.networkUpdateF)
            self.fire[-1].opacitySignal.connect(self.fireVisualize)'''
            self.fire[-1].burn()
            self.updateMinTime()
            #初始化消防員
            for i in self.fireNetwork.nodeList:
                if(not i.getArcs()):
                    depot = i
            for i in self.nodeList:
                if(i.getNum() == depot.getNum()):
                    depot = i
            if os.path.exists("FFInfo.json"): #若有自定義的情況
                with open("FFInfo.json", 'r') as file:
                    data = json.load(file)
                self.FFInfoDict = data["FFinfo"]
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.centralwidget, i+1, depot)
                    ff.FFSignal.connect(self.ffSignalDetermination)
                    '''ff.FFdoneSignal.connect(self.updateFFStatus)
                    ff.FFprotectSignal.connect(self.updateMinTime)
                    ff.FFprotectSignal.connect(self.networkUpdate)
                    ff.FFidleSignal.connect(self.updateNodeIdle)'''
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                self.networkUpdate(depot.getNum())
                for i in self.firefighterList:
                    tempNum = i.num
                    pixmap = QPixmap(self.FFInfoDict[tempNum-1]["img"])
                    self.labels.append(pixmap)
                    scaled_pixmap = pixmap.scaled(self.labels[tempNum-1].size(), aspectRatioMode=Qt.KeepAspectRatio,
                                                  transformMode=Qt.SmoothTransformation)
                    i.setPixmap(scaled_pixmap)
                    i.rate_extinguish = int(self.FFInfoDict[tempNum-1]["er"])
                    i.move_man = int(self.FFInfoDict[tempNum-1]["ts"])
            else:
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.centralwidget, i+1, depot)
                    ff.FFSignal.connect(self.ffSignalDetermination)
                    '''ff.FFdoneSignal.connect(self.updateFFStatus)
                    ff.FFprotectSignal.connect(self.updateMinTime)
                    ff.FFprotectSignal.connect(self.networkUpdate)
                    ff.FFidleSignal.connect(self.updateNodeIdle)'''
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                self.networkUpdate(depot.getNum())
                #self.firefighterList[1].setPixmap(QPixmap("./image/fireman.png"))

        randomFireAndDepot()
        self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName()) #UI SETTING: put here because the order of initialization
        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)
        self.selectFireFighter()

        self.generateblockFF_gameWindow()
        self.updateFFStatus()
        

        self.howManyAvail()
        self.hintAnimate("firefighter available: {}".format(self.availFF))
        def databaseInit():
            self.nw.numFF = self.firefighterNum
            self.db.numFF = self.firefighterNum
            self.db.numNode = len(self.nodeList)

        databaseInit()
        self.dataRecord()

        def setOpacity(num, label):
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(num)
            label.setGraphicsEffect(opacity_effect)
        if(self.firefighterList[self.FFindex].curPos().isProtected()):
            setOpacity(0.5,self.defendButton)
            self.defendButton.setEnabled(False)
        else:
            setOpacity(1,self.defendButton)
            self.defendButton.setEnabled(True)

    def turtorial(self):
        self.turtorialWindow = turtorial(self)
        self.turtorialWindow.show()
        self.close()
        
    def howManyAvail(self):
        self.assignedFF = 0
        self.availFF = 0
        for i in self.firefighterList:
            if(i.getcumArrivalTime() == self.currentTime):
                self.availFF += 1

    def intoGame(self):
        self.setStyleSheet("")
        self.instruct.setGeometry(-200,-200,400,200)
        self.yesButton.setGeometry(-200,-200,101,51)
        self.noButton.setGeometry(-200,-200,101,51)
        self.descriptionAnimate("Assign firefighter to new position or protect the current node")
        
    def showProblem(self):
        self.instruct.setGeometry(300,50,600,600)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(10)
        self.instruct.setFont(font)
        self.instruct.setText("This is a firefighter simulation problem")
        self.noButton.setGeometry(799,599,101,51)
        self.noButton.setText("back to game")

    def assignIdle(self):
        self.assignedFF += 1
        self.hintAnimate("firefighter available: {}".format(self.availFF - self.assignedFF))
        if(not self.firefighterList[(self.FFindex + 1) % self.firefighterNum].isSelected()):
            self.selectFireFighter()
        self.updateFFStatus()
        self.descriptionAnimate("{} idle for {} time step(s)".format(self.firefighterList[self.FFindex].getName(), self.spinBox.value()))
        self.nextTime()

    def idleLock(self):
        if(self.checkBox.isChecked()):
            self.spinBox.setValue(99)
            self.spinBox.setEnabled(False)
        else:
            self.spinBox.setEnabled(True)

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
    def ffSignalDetermination(self, text, no):
        if(text == "done"):
            self.updateFFStatus()
        elif(text == "protect"):
            self.networkUpdate(no)
        elif(text == "idle"):
            self.updateNodeIdle(no)

    def networkUpdate(self,no): #FF network有節點被保護時呼叫，更新fire network
        self.fireNetwork.nodeList[no-1].defend()
        self.updateMinTime()

    def updateMinTime(self): #更新FF network的fireMinArrivalTime
        
        for i in self.fireNetwork.nodeList:
            i.fireMinArrivalTime = 10000

        for i in self.fire:
            i.minTimeFireArrival()
        for i in self.FFnetwork.nodeList:
            i.fireMinArrivalTime = self.fireNetwork.nodeList[i.getNum()-1].fireMinArrivalTime
            #print("node {}: {}".format(i.getNum(), i.fireMinArrivalTime))


    def updateFFStatus(self): #消防員移動/澆水完成時呼叫，更新消防員的狀態
        for i in range(self.firefighterNum):
            self.firefighterList[i].updateStatus()
            if(self.firefighterList[i].isTraveling()):
                if (i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Traveling to Node {}".format(self.firefighterList[i].destNode.getNum())
                elif (i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Traveling to Node {}".format(self.firefighterList[i].destNode.getNum())
            elif(self.firefighterList[i].isProcess()):
                if (i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Processing Node {}".format(self.firefighterList[i].destNode.getNum())
                elif (i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Processing Node {}".format(self.firefighterList[i].destNode.getNum())
            elif(self.firefighterList[i].isSelected()):
                if(i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Selected Node {}".format(self.firefighterList[i].destNode.getNum())
                elif(i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Selected Node {}".format(self.firefighterList[i].destNode.getNum())
            else:
                if(i == self.FFindex):
                    self.nw.ffblockCP_sta1 = "Idle"
                elif(i == self.prevFFindex):
                    self.nw.ffblockCP_sta2 = "Idle"
        self.iw_pageCP_FF()

    def updateNodeIdle(self, no):
        self.fireNetwork.nodeList[no-1].ffidle()

    '''------------------------------------------fire signal---------------------------------------------'''
    def fireSignalDetermination(self, text, opacity = 0, no = 0):
        if(text == "burn"):
            self.networkUpdateF(no)
        elif(text == "visual"):
            self.fireVisualize(opacity, no)
    
    def networkUpdateF(self,no): #當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        self.nodeList[no - 1].onFire()
        self.fire.append(Fire(self.fireNetwork, no, self.currentTime))
        self.fire[-1].fireSignal.connect(self.fireSignalDetermination)
        '''self.fire[-1].burnedSignal.connect(self.networkUpdateF)
        self.fire[-1].opacitySignal.connect(self.fireVisualize)'''

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        self.fireNetwork.nodeList[no-1].updateStatus()
        self.nodeList[no-1].nodeController.style = f'background-color: rgba(255, 0, 0, {opacity}); color: white;'
        self.nodeList[no-1].setStyleSheet(self.nodeList[no-1].nodeController.style)
        self.nodeList[no-1].updateGrassAmount(self.fireNetwork.nodeList[no-1].getGrassAmount())
        self.nodeList[no-1].updateStatus()

        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)

    def finish(self):
        self.timer.stop()
        self.result = resultsWindow(self.nodeList, self.currentTime)
        self.result.show()


    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.node_info_label.setVisible(False)
        if(a0.key()==Qt.Key_Enter-1):
            self.nextTime()
        elif(a0.key() == Qt.Key_C):
            self.selectFireFighter()
            #self.iw_pageCP_FF()
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
        self.clear_layout(self.verticalLayout)
        self.generateblockFF_gameWindow()

    def newNetwork(self):
        import subprocess
        import os
        subprocess.call("./randomPlanerGraph/GenerateGraph.py", shell=True)
        p = sys.executable
        os.execl(p, p, *sys.argv)

    def newFFnum(self):
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)

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
        self.anim.setStartValue(QPoint(750, 710))
        self.anim.setEndValue(QPoint(2200, 710))
        self.anim.setDuration(250)
        def start():
            self.anim.start()
        QTimer.singleShot(1500, start)

    def descriptionAnimate(self, text):
        
        self.descriptionLabel.setText(text)
        self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(2200, 710))
        self.anim.setEndValue(QPoint(750, 710))
        self.anim.setDuration(250)
        self.anim.start()

        self.anim.finished.connect(self.nextAnim)      
        self.descriptionLabel.raise_()

    def nextHintAnim(self):
        if self.index < len(self.text):
            self.consoleLabel.setText(self.text[:self.index+1])
            self.index += 1
        else:
            self.timeHint.stop()

    def hintAnimate(self, text):
        self.index = 0
        self.text = text
        self.timeHint = QTimer()
        self.timeHint.setInterval(10)
        self.timeHint.timeout.connect(self.nextHintAnim)
        self.timeHint.start()        

    def InfoShow(self): #查看node資訊
        #處理顯示文字
        self.iw_pageCP_node()
        text = "This is node: {}, you need to protect it before time {}".format(self.sender().getNum(),self.sender().getFireMinArrivalTime())
        self.hintAnimate(text)

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
        self.firefighterList[self.prevFFindex].closeaccessibleVisualize(self.nodeList)
        self.firefighterList[self.FFindex].accessibleVisualize(self.currentTime)
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))
        image = self.firefighterList[self.FFindex].grab()
        scaled_pixmap = image.scaled(self.selectLabel.width(), self.selectLabel.height())
        self.selectLabel.setPixmap(scaled_pixmap)
        if(self.firefighterList[self.FFindex].isSelected()):
            warn = QPixmap("./image/warning.png")
            self.warningLabel.setPixmap(warn.scaled(90,70))
        else:
            self.warningLabel.setPixmap(QPixmap())

    def __opacitySet(self): #調整FF的opacity
        def setOpacity(num, label):
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(num)
            label.setGraphicsEffect(opacity_effect)

        for i in range(self.firefighterNum):
            opacity = 1 if i == self.FFindex else 0.3
            setOpacity(opacity, self.firefighterList[i])
        setOpacity(1, self.firefighterList[self.FFindex])

    def printStatus(func):
        def aa(self):
            ff = self.firefighterList[self.FFindex]
            if(ff.isSelected() and self.sender() != ff.destNode):
                text = "already selected"
            else:
                text = func(self)
                self.assignedFF += text[1]
                self.hintAnimate("firefighter available: {}".format(self.availFF - self.assignedFF))
                if(not self.firefighterList[(self.FFindex + 1) % self.firefighterNum].isSelected() and text[1] == 1):
                    self.selectFireFighter()
            self.updateFFStatus()
            self.descriptionAnimate(text[0])
            
            self.nextTime()
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        send = None
        self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
        if(self.sender().objectName() == "defendButton"):
            text = self.checkStatus(self.firefighterList[self.FFindex].curPos())
            send = self.firefighterList[self.FFindex].curPos()
        else:
            text = self.checkStatus(self.sender()) #檢查選擇的node是否符合限制
            send = self.sender()
        if(text == "vaild choose"):
            if(self.firefighterList[self.FFindex].destNode == send): #是否選擇取消(再次點擊同node)
                self.firefighterList[self.FFindex].reset()
                send.setStyleSheet("")
                return ("{} reset".format(self.firefighterList[self.FFindex].getName()), -1)
            text = self.firefighterList[self.FFindex].processCheck(send)
            self.firefighterList[self.FFindex].ready()
            self.firefighterList[self.FFindex].updateStatus()
            self.clear_layout(self.verticalLayout)
            self.generateblockFF_gameWindow()
            return (text, 1)
        return (text, 0)

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
            self.lcd_time.display(self.currentTime)
            ctr = 0
            for i in self.fire:
                if(i.finishSpread):
                    ctr+=1
            print("ctr: {}, all: {}".format(ctr, len(self.fire)))
            if(ctr == len(self.fire)):
                self.finish()
            self.dataRecord()
            self.upadateInformation()
            self.currentTime+=1
            for i in self.fire:
                i.fire_spread(self.currentTime)
            for i in self.firefighterList:
                i.cancelReady()
                i.updateStatus()
                if(i.checkArrival(self.currentTime)):
                    self.timer.stop()
                    self.FFindex = i.num - 2
                    self.selectFireFighter()
                    self.descriptionAnimate("firefighter {} has finished task".format(i.num))
                    self.howManyAvail()
                    self.hintAnimate("firefighter available: {}".format(self.availFF))
                    def setOpacity(num, label):
                        opacity_effect = QGraphicsOpacityEffect()
                        opacity_effect.setOpacity(num)
                        label.setGraphicsEffect(opacity_effect)
                    if(i.curPos().isProtected()):
                        setOpacity(0.5,self.defendButton)
                        self.defendButton.setEnabled(False)
                    else:
                        setOpacity(1,self.defendButton)
                        self.defendButton.setEnabled(True)
            self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
            self.__opacitySet()
            self.timeIndexLabel.setText("t= "+str(self.currentTime))
            # self.lcd_time.display(self.currentTime)
            self.clear_layout(self.verticalLayout)
            self.generateblockFF_gameWindow()
        if(self.assignedFF == self.availFF):
            self.clear_layout(self.verticalLayout)
            self.generateblockFF_gameWindow()
            for i in self.firefighterList:
                if(not (i.isTraveling() or i.isProcess())):
                    i.finishTimeSet(self.spinBox.value())
                    i.closeaccessibleVisualize(self.nodeList)
                i.move()
            self.timer = QTimer()
            self.timer.setInterval(700)
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
        # self.nw.(x, y)

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        if(self.showFireNetwork):
            qpen = QPen(Qt.red, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    qpainter.drawLine(QPointF(i.pos.x() + i.pos.width()/2, i.pos.y()+ 3/2*i.pos.height()), QPointF(j.pos.x()+ j.pos.width()/2, j.pos.y()+ 3/2*j.pos.height()))          
            for i in self.nodeList:
                i.setText(str(i.getFireMinArrivalTime()))
        if(self.showFFnetwork):
            qpen = QPen(Qt.black, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                i.setText(str(i.getNum()))
                for j in i.getNeighbors():
                    if(not self.showFireNetwork):
                        '''if(i.getArc(j)["length"] < 150):
                            qpen = QPen(Qt.green, 4, Qt.SolidLine)
                        elif(i.getArc(j)["length"] < 300):
                            qpen = QPen(Qt.darkYellow, 4, Qt.SolidLine)
                        else:
                            qpen = QPen(Qt.red, 4, Qt.SolidLine)
                            
                    qpainter.setPen(qpen)'''
                    qpainter.drawLine(QPointF(i.x() + i.width()/2, i.y()+ 3/2*i.height()), QPointF(j.x()+ j.width()/2, j.y()+ 3/2*j.height()))
        for i in self.fire:
            for j in i.arcs:
                    tempXpercent = (j["node"].pos.x() + j["node"].pos.width()/2 - i.firePos.pos.x() - i.firePos.pos.width()/2) * i.getArcPercentage_Fire(j)
                    tempYpercent = (j["node"].pos.y() + 3/2*j["node"].pos.height() - i.firePos.pos.y() - 3/2*i.firePos.pos.height()) * i.getArcPercentage_Fire(j)
                    qpen = QPen(Qt.darkRed, 6, Qt.SolidLine)
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


    def blockFFContent_gameWindow(self, num):
        for i in self.firefighterList:
            if(num == i.num):
                font = QFont()
                font.setPointSize(11)
                font.setBold(True)

                blockff = QWidget()
                blockff.setObjectName(f'{num}')
                blockff.setFixedSize(240,115)
                blockff.setStyleSheet(
                    "QWidget {"
                    "   border: 2px solid ;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "}"
                )
                pixmap = i.grab()
                title_label_img = QLabel(blockff)
                title_label_img.setGeometry(10, 10, 85,100)

                title_label_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                title_label_img.setStyleSheet(
                    "QLabel {"
                    "   border: 2px solid #0078d7;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "}"
                )
                scaled_pixmap = pixmap.scaled(title_label_img.width(), title_label_img.height())
                title_label_img.setPixmap(scaled_pixmap)

                title_label_name_des = QLabel(i.getName(), blockff)
                title_label_name_des.setFont(font)
                title_label_name_des.setGeometry(100, 75, 120, 30)

                temp = str(i.status)
                self.title_label_ready_des = QLabel(temp, blockff)
                self.title_label_ready_des.setFont(font)
                self.title_label_ready_des.setGeometry(100, 25, 120, 35)

        return blockff
    def blockFFComplete_gameWindow(self, num):
        for i in self.firefighterList:
            if(num == i.num):
                font = QFont()
                font.setPointSize(11)
                font.setBold(True)

                blockff = QWidget(self.centralwidget)
                blockff.setObjectName(f'{num}')
                blockff.setFixedSize(240,380)
                blockff.setStyleSheet(
                    "QWidget {"
                    "   border: 2px solid ;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "background-color: white;"
                    "}"
                )

                def delete_self(self):
                    blockff.close()
                button_delete = QPushButton("Close",blockff)
                button_delete.setGeometry(180, 10, 50, 25)
                button_delete.clicked.connect(delete_self)


                pixmap = i.grab()
                title_label_img = QLabel(blockff)
                title_label_img.setGeometry(10, 10, 85,100)

                title_label_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                title_label_img.setStyleSheet(
                    "QLabel {"
                    "   border: 2px solid #0078d7;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "}"
                )
                scaled_pixmap = pixmap.scaled(title_label_img.width(), title_label_img.height())
                title_label_img.setPixmap(scaled_pixmap)
                title_label_name = QLabel("Name\t:", blockff)
                title_label_name.setFont(font)
                title_label_name.setGeometry(0, 115, 80, 30)
                title_label_name_des = QLabel(i.getName(), blockff)
                title_label_name_des.setFont(font)
                title_label_name_des.setGeometry(0, 155, 120, 30)

                title_label_wr = QLabel("Water Rate\t:", blockff)
                title_label_wr.setFont(font)
                title_label_wr.setGeometry(0, 205, 120, 30)
                temp = str(i.rate_extinguish)
                title_label_wr_des = QLabel(temp, blockff)
                title_label_wr_des.setFont(font)
                title_label_wr_des.setGeometry(0, 245, 150, 30)

                title_label_mr = QLabel("Move Rate\t:", blockff)
                title_label_mr.setFont(font)
                title_label_mr.setGeometry(0, 295, 120, 30)
                temp = str(i.move_man)
                title_label_mr_des = QLabel(temp, blockff)
                title_label_mr_des.setFont(font)
                title_label_mr_des.setGeometry(0, 335, 150, 30)

        return blockff

    def generateblockFF_gameWindow(self):
        self.blocklist = []
        for i in self.firefighterList:
            block = self.blockFFContent_gameWindow(i.num)
            self.blocklist.append(block)
            block.mousePressEvent = partial(self.blockFF_mousePressEvent,block.objectName())
            block.enterEvent = partial(self.blockFF_mouseEnterEvent,block.objectName())
            block.leaveEvent = partial(self.blockFF_mouseLeaveEvent,block.objectName())
            self.verticalLayout.addWidget(block)

    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def checkAllReady(self):
        templist = []
        for i in self.firefighterList:
            templist.append(i.nextRound)
        if(False in templist):
            self.ready = False
        else:
            self.ready = True

    def blockFF_mousePressEvent(self,nums,event):
        for i in self.block_completelist:
            i.close()
            self.block_completelist = []
        for i in self.blocklist:
            if(i.objectName() == nums):
                nums = int(nums)
                block_complete = self.blockFFComplete_gameWindow(nums)
                self.block_completelist.append(block_complete)
                block_complete.raise_()
                block_complete.show()
                block_complete.setGeometry(270,250,240,400)

    def blockFF_mouseEnterEvent(self,nums ,event):
        for i in self.blocklist:
            if(i.objectName() == nums):
                i.setStyleSheet(
                    "QWidget {"
                    "   border: 2px solid #FF4778 ;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "}"
                )
                i.setCursor(QCursor(Qt.PointingHandCursor))

    def blockFF_mouseLeaveEvent(self,nums ,event):
        for i in self.blocklist:
            if(i.objectName() == nums):
                i.setStyleSheet(
                    "QWidget {"
                    "   border: 2px solid  ;"  
                    "   border-radius: 10px;"  
                    "   padding: 5px;"  
                    "}"
                )



