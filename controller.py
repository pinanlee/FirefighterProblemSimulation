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
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QCursor, QPalette, QColor, QIcon
from PyQt5 import uic
import pandas as pd
import numpy as np
from dataBase import DataBase
from informationWindow import  InformationWindow
from results import resultsWindow
import sys
from PIL import ImageGrab
from instruction import Instruction

FFNum = 2


class MainWindow_controller(QtWidgets.QMainWindow):
    fire : list[Fire] = []
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 2
    nodeNum = len(nodeList)
    FFindex = 0 
    #focusIndex = 14
    labels : QtWidgets.QLabel = []
    timer = QTimer()
    currentTime = 0
    pageList = -1
    FFnetwork : Network = None
    fireNetwork : Network = None
    showFFnetwork : bool = True
    showFireNetwork : bool = True
    FFInfoDict = []
    totalValue = 0
    availFF = 0
    screenshot_range = (290, -10, 1900, 751)

    def __init__(self,mode):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.mode = mode
        global FFNum
        if mode == 1:
            uic.loadUi("UIv4.ui",self)
        elif mode == 2:
            uic.loadUi("case1.ui",self)
            pixmap = QPixmap("image/case1image.jpg")  # 替换为您的图像文件路径
            self.label_background.setPixmap(pixmap)

            self.backgroundLabel_2

        if os.path.exists("FFInfo.json"):
            with open("FFInfo.json", 'r') as file:
                data = json.load(file)
            FFNum = int(data["FFnumber"])
        #self.db = DataBase()
        #self.nw = InformationWindow(self.db)
        #self.inst = Instruction(self.centralWidget())
        #self.inst.intoGame()
        self.firefighterNum = FFNum
        self.subwindows = []
        self.setup_control()
        self.window_FFnum = FFnumWindow()
        self.window_FFnum.window_FF.updateFFnumSignal.connect(self.newFFnum)
        self.block_completelist = []



    '''------------------------------------初始化--------------------------------------------------------'''
    def setup_control(self):
        def initNetwork(): #建立network class和node
            if self.mode == 1:
                self.FFnetwork = Network("./network/testModel/G30_firefighter_route.xlsx", "./network/testModel/G30_nodeInformation.xlsx", "N_D")
                self.fireNetwork = Network("./network/testModel/G30_fire_route.xlsx", "./network/testModel/G30_nodeInformation.xlsx", "N_F")
            elif self.mode == 2:
                self.FFnetwork = Network("./network/case1/case1_firefighter_route.xlsx", "network/case1/case1_nodeInformation.xlsx", "N_D")
                self.fireNetwork = Network("./network/case1/case1_fire_route.xlsx", "network/case1/case1_nodeInformation.xlsx", "N_F")

            for i in self.FFnetwork.nodeList:
                node = Node(self.gamewidget, i)
                if self.mode == 2:
                    if i.getNum() == 2:
                        image1 = QIcon("image/tent.png")
                        node.setIcon(image1)
                node.clicked.connect(self.choose)
                node.showSignal.connect(self.InfoShow)
                self.nodeList.append(node)
                self.totalValue+=node.getValue()
            self.progressBar.setMaximum(self.totalValue)
            self.progressBar.setValue(self.totalValue)
        initNetwork()
        self.nodeNum = len(self.nodeList)
        #self.db.numNode = self.nodeNum


        def initUI(): # UI設定(可略)
            #self.setStyleSheet("background-color: rgb(100, 100, 100);")
            #self.focusIndex = len(self.nodeList) - 1
            self.button_menu.clicked.connect(self.backMenu)
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.7)
            self.descriptionLabel.setGraphicsEffect(opacity_effect)
            if self.mode == 1:
                self.actionProblem.triggered.connect(self.showProblem)
            self.actionAnimation.triggered.connect(self.showFFWindow)
            self.actionNew.triggered.connect(self.newNetwork)
            # self.nodeList[self.focusIndex].setFocus()
            if self.mode == 1:
                self.yesButton.clicked.connect(self.showProblem)
                self.node_info_label.setVisible(False)
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
                for j in i.getArcs():
                    node = self.nodeList[j["node"].getNum()-1]
                    i.connectNode(node)
        NodeConnection()

        def randomFireAndDepot(): #初始化火和消防員
            #初始化火
            fireDepot = next((i.getNum() for i in self.fireNetwork.nodeList if i.isDepot()), None)
            self.fire.append(Fire(self.fireNetwork, fireDepot, self.currentTime))
            self.fire[-1].burn()
            self.nodeList[fireDepot-1].onFire()
            self.fire[-1].fireSignal.connect(self.fireSignalDetermination)
            #初始化消防員
            self.updateMinTime()

            depot = next((i for i in self.nodeList if i.isDepot()), None)

            if os.path.exists("FFInfo.json"): #若有自定義的情況
                with open("FFInfo.json", 'r') as file:
                    data = json.load(file)
                self.FFInfoDict = data["FFinfo"]
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.gamewidget, i+1, depot)
                    ff.FFSignal.connect(self.ffSignalDetermination)
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                #self.networkUpdate(depot.getNum())
                for i in self.firefighterList:
                    tempNum = i.getNum()
                    pixmap = QPixmap(self.FFInfoDict[tempNum-1]["img"])
                    self.labels.append(pixmap)
                    scaled_pixmap = pixmap.scaled(self.labels[tempNum-1].size(), aspectRatioMode=Qt.KeepAspectRatio,
                                                  transformMode=Qt.SmoothTransformation)
                    i.setPixmap(scaled_pixmap)
                    i.rate_extinguish = int(self.FFInfoDict[tempNum-1]["er"])
                    i.move_man = int(self.FFInfoDict[tempNum-1]["ts"])
            else:
                for i in range(self.firefighterNum):
                    ff = FireFighter(self.gamewidget, i+1, depot)
                    ff.FFSignal.connect(self.ffSignalDetermination)
                    depot.depotSetting()
                    self.firefighterList.append(ff)
                #self.networkUpdate(depot.getNum())
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
            return
            #self.nw.numFF = self.firefighterNum
            #self.db.numFF = self.firefighterNum
            #self.db.numNode = len(self.nodeList)

        databaseInit()
        self.dataRecord()

        self.defendButton.setEnabled(not self.firefighterList[self.FFindex].curPos().isProtected())
        
    def howManyAvail(self):
        self.availFF = len([i for i in self.firefighterList if i.getcumArrivalTime() == self.currentTime])

    def intoGame(self):
        self.setStyleSheet("")
        self.instruct.setGeometry(-200,-200,400,200)
        self.yesButton.setGeometry(-200,-200,101,51)
        self.noButton.setGeometry(-200,-200,101,51)
        
    def showProblem(self):
        self.inst.show()

    def assignIdle(self):
        self.availFF -= 1
        self.hintAnimate("firefighter available: {}".format(self.availFF))
        if(not self.firefighterList[(self.FFindex + 1) % self.firefighterNum].isSelected()):
            self.selectFireFighter()
        self.updateFFStatus()
        self.descriptionAnimate("{} idle for {} time step(s)".format(self.firefighterList[self.FFindex].getName(), self.spinBox.value()))
        self.nextTime()

    def idleLock(self):
        if(self.checkBox.isChecked()):
            self.spinBox.setValue(99)
        self.spinBox.setEnabled(not self.checkBox.isChecked())


    '''---------------------------------------firefighter signal-----------------------------------------'''
    def ffSignalDetermination(self, text, no):
        if(text == "done"):
            self.updateFFStatus()
        elif(text == "protect"):
            self.networkUpdate(no)
        '''elif(text == "idle"):
            self.updateNodeIdle(no)'''

    def networkUpdate(self,no): #FF network有節點被保護時呼叫，更新fire network
        self.fireNetwork.nodeList[no-1].defend()
        self.updateMinTime()

    def updateMinTime(self): #更新FF network的fireMinArrivalTime
        for i in self.fireNetwork.nodeList:
            i.setFireMinArrivalTime(10000)
        
        [i.minTimeFireArrival() for i in self.fire]
        for i in self.FFnetwork.nodeList:
            i.setFireMinArrivalTime(self.fireNetwork.nodeList[i.getNum()-1].getFireMinArrivalTime())

    def updateFFStatus(self): #消防員移動/澆水完成時呼叫，更新消防員的狀態
        for i in range(self.firefighterNum):
            self.firefighterList[i].updateStatus()
            # if(self.firefighterList[i].isTraveling()):
            #     if (i == self.FFindex):
            #         return
            #         #self.nw.ffblockCP_sta1 = "Traveling to Node {}".format(self.firefighterList[i].destination().getNum())
            #     elif (i == self.prevFFindex):
            #         return
            #         # self.nw.ffblockCP_sta2 = "Traveling to Node {}".format(self.firefighterList[i].destination().getNum())
            # elif(self.firefighterList[i].isProcess()):
            #     if (i == self.FFindex):
            #         return
            #         #self.nw.ffblockCP_sta1 = "Processing Node {}".format(self.firefighterList[i].destination().getNum())
            #     elif (i == self.prevFFindex):
            #         return
            #         #self.nw.ffblockCP_sta2 = "Processing Node {}".format(self.firefighterList[i].destination().getNum())
            # elif(self.firefighterList[i].isSelected()):
            #     if(i == self.FFindex):
            #         return
            #         #self.nw.ffblockCP_sta1 = "Selected Node {}".format(self.firefighterList[i].destination().getNum())
            #     elif(i == self.prevFFindex):
            #         return
            #         #self.nw.ffblockCP_sta2 = "Selected Node {}".format(self.firefighterList[i].destination().getNum())
            # else:
            #     if(i == self.FFindex):
            #         return
            #         #self.nw.ffblockCP_sta1 = "Idle"
            #     elif(i == self.prevFFindex):
            #         return
            #         #self.nw.ffblockCP_sta2 = "Idle"
        self.iw_pageCP_FF()

    # def updateNodeIdle(self, no):
    #     self.fireNetwork.nodeList[no-1].ffidle()

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

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        self.fireNetwork.nodeList[no-1].updateStatus()
        self.nodeList[no-1].setStyle(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
        self.nodeList[no-1].setStyleSheet(self.nodeList[no-1].getStyle())
        self.nodeList[no-1].updateStatus()

        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)

    def finish(self):
        self.timer.stop()
        self.result = resultsWindow(self.nodeList, self.currentTime)
        self.result.show()


    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        #self.node_info_label.setVisible(False)
        if(a0.key() == Qt.Key_S):
                self.networkChange()
        if(a0.key() == Qt.Key_N):
            self.newNetwork()
        if(a0.key() == Qt.Key_Q):
            self.finish()
        self.updateFFStatus()
        self.refreshBlock()

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

    def __nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(750, 710))
        self.anim.setEndValue(QPoint(2200, 710))
        self.anim.setDuration(250)
        def start():
            self.anim.start()
        QTimer.singleShot(1500, start)

    def descriptionAnimate(self, text):
        def initAnim(self):
            self.descriptionLabel.setText(text)
            self.descriptionLabel.raise_()
            self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
            self.anim.setStartValue(QPoint(2200, 710))
            self.anim.setEndValue(QPoint(750, 710))
            self.anim.setDuration(250)
            
        initAnim(self)
        self.anim.finished.connect(self.__nextAnim)
        self.anim.start()


    def __nextHintAnim(self):
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
        self.timeHint.timeout.connect(self.__nextHintAnim)
        self.timeHint.start()        

    def InfoShow(self): #查看node資訊
        #處理顯示文字
        self.iw_pageCP_node()
        text = "This is node: {}, \nthe earlist burn time: {}, \nNode value: {}, Processing time: {}".format(self.sender().getNum(),self.sender().getFireMinArrivalTime(),self.sender().getValue(), math.ceil(self.sender().getProcessingTime() / self.firefighterList[self.FFindex].rate_extinguish))
        self.hintAnimate(text)

    def iw_pageCP_node(self):
        #part node
        #self.nw.title_label_node_des.setText(str(self.nodeList[self.focusIndex].getNum()))

        '''if (self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex]) == -1):
            #self.nw.nodeblock_textlen = "Not neighbor"
            temptta = "Not neighbor"
        else:
            #self.nw.nodeblock_textlen = str(math.ceil(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"]))
            templen = self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"]
            tempextRate = self.firefighterList[self.FFindex].move_man
            temptta = math.ceil(self.currentTime + templen / tempextRate)'''

        #self.nw.title_label_length_des.setText(self.nw.nodeblock_textlen)
        #self.nw.title_label_tta_des.setText(str(temptta))
        #tempttb = self.nodeList[self.focusIndex].getFireMinArrivalTime()
        #self.nw.title_label_ttb_des.setText(str(tempttb))
        #self.nw.nodeblock_textsta =  self.nodeList[self.focusIndex].getStatus()
        #self.nw.title_label_sta_des.setText(self.nw.nodeblock_textsta)

        '''if(self.nw.nodeblock_textsta == "Burned"):
            self.nw.nodeCircle.setStyleSheet("background-color: red;")
        elif (self.nw.nodeblock_textsta == "Damaged"):
            self.nw.nodeCircle.setStyleSheet("background-color: darkred;")
        elif (self.nw.nodeblock_textsta == "Safe"):
            self.nw.nodeCircle.setStyleSheet("background-color: darkgreen;")
        elif(self.nw.nodeblock_textsta == "Protected"):
            self.nw.nodeCircle.setStyleSheet("background-color: green;")
        else:
            self.nw.nodeCircle.setStyleSheet("background-color: white;")'''

    def iw_pageCP_FF(self):
        #part FF
        return
        # self.nw.ffblockCP_img1 = self.firefighterList[self.FFindex].grab()
        # self.nw.ffblockCP_name1 = self.firefighterList[self.FFindex].getName()
        # self.nw.ffblockCP_wr1 = str(self.firefighterList[self.FFindex].rate_extinguish)
        # self.nw.ffblockCP_img2 = self.firefighterList[self.nextFFindex].grab()
        # self.nw.ffblockCP_name2 = self.firefighterList[self.nextFFindex].getName()
        # self.nw.ffblockCP_wr2 = str(self.firefighterList[self.nextFFindex].rate_extinguish)
        # self.nw.pageCP_generateblockFF()


    def selectFireFighter(self): #切換選擇消防員
        #self.prevFFindex = self.FFindex
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        #self.nextFFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].setPixmap(self.firefighterList[self.FFindex].grab())
        self.firefighterList[self.FFindex - 1].closeaccessibleVisualize(self.nodeList)
        self.firefighterList[self.FFindex].accessibleVisualize(self.currentTime,self.nodeList)
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))
        image = self.firefighterList[self.FFindex].grab()
        scaled_pixmap = image.scaled(self.selectLabel.width(), self.selectLabel.height())
        self.selectLabel.setPixmap(scaled_pixmap)

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
            if(ff.isSelected() and self.sender() != ff.destination()):
                text = "already selected"
            else:
                text = func(self)
                self.availFF -= text[1]
                self.hintAnimate("firefighter available: {}".format(self.availFF))
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
        send = self.firefighterList[self.FFindex].curPos() if self.sender().objectName() == "defendButton" else self.sender()
        text = self.checkStatus(send)
        if(text == "vaild choose"):
            if(self.firefighterList[self.FFindex].destination() == send): #是否選擇取消(再次點擊同node)
                self.firefighterList[self.FFindex].reset()
                send.setStyleSheet("")
                return ("{} reset".format(self.firefighterList[self.FFindex].getName()), -1)
            text = self.firefighterList[self.FFindex].processCheck(send)
            #self.firefighterList[self.FFindex].ready()
            self.firefighterList[self.FFindex].updateStatus()
            self.refreshBlock()
            return (text, 1)
        return (text, 0)

    def refreshBlock(self):
        self.clear_layout(self.verticalLayout)
        self.generateblockFF_gameWindow()

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
            screenshot = ImageGrab.grab(self.screenshot_range)
            screenshot.save(f"image/timescreenshot/time00{self.currentTime:03d}.png")
            gameTerminated = all(i.isComplete() for i in self.fire)
            if gameTerminated:
                self.finish()

            self.dataRecord()
            self.upadateInformation()
            self.currentTime+=1
            for i in self.fire:
                i.fire_spread(self.currentTime)
            for i in self.firefighterList:
                #i.cancelReady()
                i.updateStatus()
                if(i.checkArrival(self.currentTime)):
                    screenshot = ImageGrab.grab(self.screenshot_range)
                    screenshot.save(f"image/timescreenshot/time00{self.currentTime:03d}.png")
                    self.timer.stop()
                    self.FFindex = i.getNum() - 2
                    self.selectFireFighter()
                    self.descriptionAnimate("firefighter {} has finished task".format(i.getNum()))
                    self.howManyAvail()
                    self.hintAnimate("firefighter available: {}".format(self.availFF))
                    self.defendButton.setEnabled(not i.curPos().isProtected())

            self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
            self.__opacitySet()
            self.lcd_time.display(self.currentTime)
            self.refreshBlock()
        if(not self.availFF):
            self.refreshBlock()
            for ff in self.firefighterList:
                if(not (ff.isTraveling() or ff.isProcess())):
                    ff.finishTimeSet(self.spinBox.value())
                    ff.closeaccessibleVisualize(self.nodeList)
                ff.move()
            self.timer = QTimer()
            self.timer.setInterval(300)
            self.timer.timeout.connect(timeSkip)
            self.timer.start()

    def showInformationWindow(self):
        self.upadateInformation()
        # self.nw.show()
        # self.subwindows.append(self.nw)


    def onSubWindowPageChanged(self, index):
        self.pageList = index
   
    def upadateInformation(self):
        return
        # self.nw.pageChanged.connect(self.onSubWindowPageChanged)
        # self.nw.tab_widget.setCurrentIndex(self.pageList)
        # x = self.nw.pos().x()
        # y = self.nw.pos().y()
        # self.nw.(x, y)

    def paintEvent(self, event):
        if self.mode == 1:
            qpainter = QPainter()
        elif self.mode == 2 :
            qpainter = QPainter(self.label_background.pixmap())
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        if(self.showFireNetwork):
            qpen = QPen(Qt.red, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            if(not self.showFFnetwork):
                for i in self.nodeList:
                    i.grassVisualize.showGrassValue()
                    i.grassVisualize.show()
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 3 / 2 * j.height()))
                    elif self.mode == 2:
                        qpainter.drawLine(
                            QPointF(i.x()  + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x()  + j.width() / 2, j.y() + 3 / 2 * j.height()))

            for i in self.nodeList:
                i.setText(str(i.getFireMinArrivalTime()))
        if(self.showFFnetwork):
            qpen = QPen(Qt.black, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                if(not self.showFireNetwork):
                    i.grassVisualize.showValue()
                    i.grassVisualize.show()
                else:
                    i.grassVisualize.hide()
                i.setText(str(i.getNum()))
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 3 / 2 * j.height()))
                    elif self.mode == 2:
                        qpainter.drawLine(
                            QPointF(i.x()  + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x()  + j.width() / 2, j.y() + 3 / 2 * j.height()))
        for i in self.fire:
            for j in i.getArcs():
                    tempXpercent = (j["node"].x() + j["node"].width()/2 - i.x() - i.width()/2) * i.getArcPercentage_Fire(j)
                    tempYpercent = (j["node"].y() + 3/2*j["node"].height() - i.y() - 3/2*i.height()) * i.getArcPercentage_Fire(j)
                    qpen = QPen(Qt.darkRed, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.x() + self.gamewidget.x() + i.width()/2, i.y() + 3/2*i.height()), QPointF(i.x() + self.gamewidget.x() + i.width()/2 + tempXpercent, i.y() + 3/2*i.height() + tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.x() + i.width()/2, i.y() + 3/2*i.height()), QPointF(i.x()  + i.width()/2 + tempXpercent, i.y() + 3/2*i.height() + tempYpercent))

        for i in self.firefighterList:
            if(i.destination() != None):
                    tempXpercent = (i.destination().x() + i.destination().width()/2 - i.curPos().x() - i.curPos().width()/2) * i.getArcPercentage_FF(i.destination())
                    tempYpercent = (i.destination().y() + 3/2*i.destination().height() - i.curPos().y() - 3/2*i.curPos().height()) * i.getArcPercentage_FF(i.destination())
                    qpen = QPen(Qt.darkGreen, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2, i.curPos().y() + 3/2*i.curPos().height()), QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 3/2*i.curPos().height()+tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.curPos().x()+ i.curPos().width()/2, i.curPos().y() + 3/2*i.curPos().height()), QPointF(i.curPos().x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 3/2*i.curPos().height()+tempYpercent))

        self.update()
        qpainter.end()

    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        # if os.path.exists("FFInfo.json"):
        #     os.remove("FFInfo.json")
        for subwindow in self.subwindows:
            subwindow.close()  # Close all open subwindows
        event.accept()

        folder_path_to_delete = "image/timescreenshot"
        try:
            for filename in os.listdir(folder_path_to_delete):
                file_path = os.path.join(folder_path_to_delete, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print("Error")

    def dataRecord(self): #將資料傳入database
        '''self.db.currentTime = self.currentTime
        self.db.ffnetworkNodeList[self.currentTime] = self.FFnetwork.nodeList
        self.db.fireNetworkNodeList[self.currentTime]  = self.fireNetwork.nodeList
        self.db.controllerNodeList[self.currentTime]  = self.nodeList
        self.db.firefighterList[self.currentTime] = self.firefighterList
        self.db.infoNextTime()'''

    def loadRecord(self): #讀檔(未完成)
        #self.currentTime = self.db.currentTime-1
        #self.FFnetwork.nodeList = self.db.ffnetworkNodeList[self.currentTime]
        #self.fireNetwork.nodeList = self.db.fireNetworkNodeList[self.currentTime]
        #self.nodeList = self.db.controllerNodeList[self.currentTime]
        self.updateFFStatus()
        self.updateMinTime()

    def showFFWindow(self):
        self.subwindows.append(self.window_FFnum)
        self.subwindows.append(self.window_FFnum.window_FF)
        self.window_FFnum.show()


    def blockFFContent_gameWindow(self, num):
        for i in self.firefighterList:
            if(num == i.getNum()):
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
                title_label_name_des.setGeometry(100, 75, 140, 30)

                temp = str(i.getStatus())
                self.title_label_ready_des = QLabel(temp, blockff)
                self.title_label_ready_des.setFont(font)
                self.title_label_ready_des.setGeometry(100, 25, 120, 35)

        return blockff
    def blockFFComplete_gameWindow(self, num):
        for i in self.firefighterList:
            if(num == i.getNum()):
                font = QFont()
                font.setPointSize(11)
                font.setBold(True)

                blockff = QWidget(self.centralwidget)
                blockff.setObjectName(f'{num}')
                blockff.setFixedSize(280,380)
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
                title_label_name_des.setGeometry(0, 155, 140, 30)

                title_label_wr = QLabel("Water Rate\t:", blockff)
                title_label_wr.setFont(font)
                title_label_wr.setGeometry(0, 205, 120, 30)
                temp = str(i.rate_extinguish)
                title_label_wr_des = QLabel(temp, blockff)
                title_label_wr_des.setFont(font)
                title_label_wr_des.setGeometry(0, 245, 150, 30)

                # title_label_mr = QLabel("Move Rate\t:", blockff)
                # title_label_mr.setFont(font)
                # title_label_mr.setGeometry(0, 295, 120, 30)
                # temp = str(i.move_man)
                # title_label_mr_des = QLabel(temp, blockff)
                # title_label_mr_des.setFont(font)
                # title_label_mr_des.setGeometry(0, 335, 150, 30)

        return blockff

    def generateblockFF_gameWindow(self):
        self.blocklist = []
        for i in self.firefighterList:
            block = self.blockFFContent_gameWindow(i.getNum())
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

    '''def checkAllReady(self):
        templist = []
        for i in self.firefighterList:
            templist.append(i.nextRound)
        if(False in templist):
            self.ready = False
        else:
            self.ready = True'''

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
    def backMenu(self):
        from titleScreen import titleScreen
        self.menu = titleScreen()
        self.menu.show()
        self.close()
        self.deleteLater()



