#!/usr/bin/env python
# coding: utf-8
import json
import os
from functools import partial
import pandas as pd
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QSizePolicy, QPushButton, QWidget
from PyQt5 import QtWidgets, QtCore, QtGui
import math
from FFSettingsWindow import FFnumWindow
from FF import FireFighter
from node import Node 
from fireObject import Fire
from network import Network
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QCursor, QColor, QIcon, QBrush, QRegion
from dataBase import DataBase
from results import resultsWindow
import sys
from PIL import ImageGrab
from controllerUtils import Controller_Utils
import pygetwindow as gw

class MainWindow_controller(QtWidgets.QMainWindow):
    modelTest : bool = False
    fire : list[Fire] = []
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 1
    FFindex = 0 
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
    screenshot_range = (290, 60, 1900, 751)
    gameTerminated = False
    model_dir = "./network/FF2test/FFP_n20_no5"
    mode=1

    def __init__(self,mode):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.mode = mode

        Controller_Utils.UIInitialize(self)

        if os.path.exists("FFInfo.json"):
            with open("FFInfo.json", 'r') as file:
                data = json.load(file)
            self.firefighterNum = int(data["FFnumber"])
        self.subwindows = []
        if os.path.exists("filename.json"):
            with open("filename.json", 'r') as file:
                data = json.load(file)
            self.model_dir = data["filename"][:-5]
        self.setup_control()
        self.window_FFnum = FFnumWindow()
        self.window_FFnum.window_FF.updateFFnumSignal.connect(self.newFFnum)
        self.block_completelist = []


    '''------------------------------------初始化--------------------------------------------------------'''
    def setup_control(self):
        Controller_Utils.createNetworkInfrastructures(self)
        Controller_Utils.nodeListInitialize(self)
        Controller_Utils.nodeConnection(self)
        Controller_Utils.depotInitialize(self)
        Controller_Utils.UIInformationInitialization(self)
        
    def modelTimeSet(self):
        Controller_Utils.getModelSolution(self)
        self.modelTime = QTimer()
        self.modelTime.timeout.connect(self.modelAuto)
        self.modelTime.setInterval(1500)
        self.modelTime.start()

    def modelAuto(self):
        if(self.currentTime >= DataBase.T):
            self.finish()
            self.modelTime.stop()
            return
        if(self.gameTerminated):
            self.modelTime.stop()
            return
        (i, j, k, t)=(1,1,1,100000)

        ss=0
        for s in DataBase.K:
            (i1,j1,k1,t1) = (self.temp[s-1][0][0],self.temp[s-1][0][1],self.temp[s-1][0][2],self.temp[s-1][0][3])
            if(t1 < t):
                ss=s
                (i,j,k,t) = (i1,j1,k1,t1)
            print("{}: {}".format((i,j,k,t),DataBase.X[f"({i1}, {j1}, {k1}, {t1})"]))
        self.focusIndex = j-1
        self.FFindex = k-1
        if t == self.currentTime:
            if i != j: 
                self.choose()
                print("消防員 {}在時刻 {} 從node {} 移動到 node {} ,travel time: {}".format(k, t, i, j, DataBase.tau[f"({i}, {j}, {float(k)})"]))
                self.consoleLabel.setText("在時刻 {} 從node {} 移動到 node {} ,travel time: {}".format(t, i, j, DataBase.tau[f"({i}, {j}, {float(k)})"]))
            else:         
                if DataBase.u_bar[f"({i}, {k}, {t})"] > DataBase.epsilon:
                    self.choose()
                    print("消防員 {}在時刻 {} 對node {} 進行保護, processing time: {}".format(k,t,i, math.ceil(DataBase.Q[f"{i}"] * DataBase.b[f"{i}"] / self.firefighterList[self.FFindex].rate_extinguish)))
                    self.consoleLabel.setText("在時刻 {} 對node {} 進行保護, processing time: {}".format(t,i, math.ceil(DataBase.Q[f"{i}"] * DataBase.b[f"{i}"] / self.firefighterList[self.FFindex].rate_extinguish)))
                else:
                    self.assignIdle()
                    print("消防員 {}在時刻 {} 在node {} idle".format(k,t,i))
                    self.consoleLabel.setText("在時刻 {} 在node {} idle".format(t,i))  

            if(self.currentTime >= DataBase.T):
                self.modelTime.stop()
                self.timer.stop()
                self.finish()
                return
            if(t == self.currentTime):
                self.temp[ss-1].pop(0)

    def howManyAvail(self):
        self.availFF = len([ff for ff in self.firefighterList if ff.getcumArrivalTime() == self.currentTime])
        
    def showProblem(self):
        self.inst.show()

    def assignIdle(self):
        if(self.firefighterList[self.FFindex].isSelected()):
            return "this firefighter is busy"
        
        if(self.firefighterList[self.FFindex].curPos().getFireMinArrivalTime() < self.currentTime + self.spinBox.value()):
            self.hintAnimate("fire will arrive during idle")
            return

        self.availFF -= 1
        if(not self.modelTest):
            self.hintAnimate("firefighter available: {}".format(self.availFF))
        for i in self.firefighterList:
            if not i.isSelected():
                self.selectFireFighter(i.getNum())
                break
        self.updateFFStatus()
        self.descriptionAnimate("{} idle for {} time step(s)".format(self.firefighterList[self.FFindex].getName(), self.spinBox.value()))
        self.nextTime()
        return "assign idle"

    def idleLock(self):
        if(self.checkBox.isChecked()):
            self.spinBox.setValue(300)
        self.spinBox.setEnabled(not self.checkBox.isChecked())


    '''---------------------------------------firefighter signal-----------------------------------------'''
    def ffSignalDetermination(self, text, no):
        if(text == "done"):
            self.updateFFStatus()
        if(text == "protect"):
            self.networkUpdate(no)
        if(text == "trapped"):
            self.criticalMessage = f"firefighter {no} can't move to other nodes, please assign protect or idle to the end"
            self.hintAnimate(self.criticalMessage)

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


    '''------------------------------------------fire signal---------------------------------------------'''
    def fireSignalDetermination(self, text, opacity = 0, no = 0):
        if(text == "burn"):
            self.networkUpdateF(no)
        if(text == "visual"):
            self.fireVisualize(opacity, no)
    
    def networkUpdateF(self,no): #當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        self.nodeList[no - 1].onFire()
        self.fire.append(Fire(self.fireNetwork, no, self.currentTime))
        if self.mode == 1:
            self.listWidget.addItem(f"At time {self.currentTime}, node {no} had burned")
            self.listWidget.scrollToItem(self.listWidget.item(self.listWidget.count() - 1))
        self.fire[-1].fireSignal.connect(self.fireSignalDetermination)

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        self.fireNetwork.nodeList[no-1].updateStatus()
        self.nodeList[no-1].setStyle(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
        if(opacity==1):
            self.nodeList[no - 1].setStyle(f'background-color: rgba(139, 0, 0, {opacity}); color: white;')
        self.nodeList[no-1].setStyleSheet(self.nodeList[no-1].getStyle())
        self.nodeList[no-1].updateStatus()
        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)

    def finish(self):
        self.timer.stop()
        self.result = resultsWindow(self.nodeList, self.currentTime)
        self.result.show()
        if os.path.exists("filename.json"):
            os.remove("filename.json")

    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if(a0.key() == Qt.Key_S):
            self.networkChange()
        if(a0.key() == Qt.Key_N):
            self.newNetwork()
        if(a0.key() == Qt.Key_Q):
            self.finish()
        if(a0.key() == Qt.Key_X):
            self.showProperty(1)
        if(a0.key() == Qt.Key_Z):
            self.showProperty(0)
        if(a0.key() == Qt.Key_A):
            self.modelTimeSet()
        self.updateFFStatus()
        self.refreshBlock()

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        for i in self.nodeList:
            i.grassVisualize.hide()

    def showProperty(self, key):
        for i in self.nodeList:
            if(key):
                i.grassVisualize.showGrassValue()
                i.grassVisualize.setText(str(math.ceil(i.getProcessingTime()/self.firefighterList[self.FFindex].rate_extinguish)))
            else:
                i.grassVisualize.showValue()
                i.grassVisualize.setText(str(i.getValue()))
            i.grassVisualize.show()

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
            self.comboBox_network.setCurrentIndex(2)
        elif(self.showFFnetwork and not self.showFireNetwork):
            self.showFFnetwork, self.showFireNetwork = False, True
            self.networkLabel.setText("Fire network")
            self.comboBox_network.setCurrentIndex(1)
        elif(not self.showFFnetwork and self.showFireNetwork):
            self.showFFnetwork = True
            self.networkLabel.setText("Hybrid network")
            self.comboBox_network.setCurrentIndex(0)

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
            self.anim.setStartValue(QPoint(2200, 600))
            self.anim.setEndValue(QPoint(750, 600))
            self.anim.setDuration(250)
            
        initAnim(self)
        # self.anim.finished.connect(self.__nextAnim)
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
        self.timeHint.setInterval(5)
        self.timeHint.timeout.connect(self.__nextHintAnim)
        self.timeHint.start()        

    def InfoShow(self,no): #查看node資訊
        #處理顯示文字
        if(no==-1):
            self.hintAnimate(self.criticalMessage)
            return
        if(self.sender().isProtected()):
            status="Protected"
        elif(self.sender().isBurned()):
            status="Burned"
        else:
            status="Normal"

        text = "Node: {} ({}), \nEarlist burn time: {}, \nTravel time: ".format(self.sender().getNum(), status, self.sender().getFireMinArrivalTime())
        if(self.firefighterList[self.FFindex].curPos().getArc(self.sender()) != None):
            text+= str(self.firefighterList[self.FFindex].curPos().getArc(self.sender())["travel-time"][f"{self.FFindex+1}"])
        else:
            text+="not neighbor"
        if(not self.modelTest):
            self.hintAnimate(text)

    def selectFireFighter(self, index): #切換選擇消防員
        self.firefighterList[self.FFindex].closeaccessibleVisualize(self.nodeList)
        self.FFindex = index - 1
        self.__opacitySet()
        self.firefighterList[self.FFindex].setPixmap(self.firefighterList[self.FFindex].grab())
        self.firefighterList[self.FFindex].accessibleVisualize(self.currentTime, self.nodeList)
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
            if(ff.isSelected()):
                return
            else:
                text = func(self)
                self.availFF -= text[1]
                if(not self.modelTest):
                    self.criticalMessage = "firefighter available: {}".format(self.availFF)
                    self.hintAnimate(self.criticalMessage)
                for i in self.firefighterList:
                    if not i.isSelected() and text[1] == 1:
                        self.selectFireFighter(i.getNum())
                        break
            self.updateFFStatus()
            self.descriptionAnimate(text[0])
            self.nextTime()
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        send = None
        if(not self.modelTest):
            self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
            send = self.firefighterList[self.FFindex].curPos() if self.sender().objectName() == "defendButton" else self.sender()
        else:
            send = self.nodeList[self.focusIndex]
        text = self.checkStatus(send)
        if(text == "vaild choose"):
            if(self.firefighterList[self.FFindex].destination() == send): #是否選擇取消(再次點擊同node)
                self.firefighterList[self.FFindex].reset()
                send.setStyleSheet("")
                return ("{} reset".format(self.firefighterList[self.FFindex].getName()), -1)
            text = self.firefighterList[self.FFindex].processCheck(send)
            self.firefighterList[self.FFindex].updateStatus()
            self.refreshBlock()
            return (text, 1)
        return (text, 0)

    def refreshBlock(self):
        self.clear_layout(self.verticalLayout)
        self.generateblockFF_gameWindow()

    def checkStatus(self, node):
        if(self.firefighterList[self.FFindex].isProcess()):
            return "this firefighter is busy"
        if(self.firefighterList[self.FFindex].isTraveling()):
            return "this firefighter is busy"
        if(node == self.firefighterList[self.FFindex].curPos()):
            return "vaild choose"
            #check if selected FireFighter can move to assigned Node
        text = self.firefighterList[self.FFindex].next_Pos_Accessment(node, self.currentTime)
        return text
        
    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():           
            screenshot = ImageGrab.grab(self.screenshot_range)
            screenshot.save(f"image/timescreenshot/time00{self.currentTime:03d}.png")
            self.gameTerminated = all(i.isComplete() for i in self.fire)
            if self.gameTerminated:
                self.finish()
                if(self.modelTest):
                    self.modelTime.stop()
                return
            self.currentTime+=1

            for i in self.nodeList:
                i.updateStatus()
            finishList = []
            for i in self.firefighterList:
                i.updateStatus()
                (check ,text) = i.checkArrival(self.currentTime)
                if(check):
                    finishList.append(i.getNum())
                    self.timer.stop()
                    self.listWidget.addItem(text)
                    self.listWidget.scrollToItem(self.listWidget.item(self.listWidget.count() - 1))
                    self.howManyAvail()
                    
                    if(not self.modelTest):
                        self.criticalMessage ="firefighter available: {}".format(self.availFF) 
                        self.hintAnimate(self.criticalMessage)
                    self.defendButton.setEnabled(not i.curPos().isProtected())
            if(finishList):
                text = ""
                for i in finishList:
                    if(self.firefighterList[i-1].curPos().isBurned()):
                        self.criticalMessage = f"firefighter {i}'s position just burned, please protect it."
                    text += str(i) + " "
                self.selectFireFighter(finishList[0])
                self.descriptionAnimate("firefighter {}has finished task".format(text))
            for i in self.fire:
                i.fire_spread()
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

    def onSubWindowPageChanged(self, index):
        self.pageList = index
   

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
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))
                    elif self.mode == 2:
                        qpainter.drawLine(
                            QPointF(i.x()  +  2.1 * i.width() / 2, i.y() + 6 / 2 * i.height()),
                            QPointF(j.x()  +  2.1 * j.width() / 2, j.y() + 6 / 2 * j.height()))

            for i in self.nodeList:
                i.setText(str(i.getFireMinArrivalTime()))
        if(self.showFFnetwork):
            qpen = QPen(Qt.black, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                i.setText(str(i.getNum()))
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))
                    elif self.mode == 2:
                        qpen = QPen(Qt.black, 6, Qt.SolidLine)
                        qpainter.setPen(qpen)
                        qpainter.drawLine(
                            QPointF(i.x()  + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x()  + j.width() / 2, j.y() + 3 / 2 * j.height()))
                        if i.getNodePercentage_FF(self.firefighterList[self.FFindex].rate_extinguish)>=0.5 and j.getNodePercentage_FF(self.firefighterList[self.FFindex].rate_extinguish)>=0.5 :
                            qpen = QPen(Qt.yellow, 6, Qt.SolidLine)
                            qpainter.setPen(qpen)
                            qpainter.drawLine(
                                QPointF(i.x() + i.width() / 2, i.y() + 3 / 2 * i.height()),
                                QPointF(j.x() + j.width() / 2, j.y() + 3 / 2 * j.height()))

        for i in self.fire:
            for j in i.getArcs():
                    tempXpercent = (j["node"].x() + j["node"].width()/2 - i.x() - i.width()/2) * i.getArcPercentage_Fire(j)
                    tempYpercent = (j["node"].y() + 3/2*j["node"].height() - i.y() - 3/2*i.height()) * i.getArcPercentage_Fire(j)
                    qpen = QPen(Qt.darkRed, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.x() + self.gamewidget.x() + i.width()/2, i.y() + 5/2*i.height()), QPointF(i.x() + self.gamewidget.x() + i.width()/2 + tempXpercent, i.y() + 5/2*i.height() + tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.x() + 2.1 * i.width()/2, i.y() + 6/2*i.height()), QPointF(i.x()  + 2.1 * i.width()/2 + tempXpercent, i.y() + 6/2*i.height() + tempYpercent))
                        current_x = int(i.x() + tempXpercent - 4*i.width()/2)
                        current_y = int(i.y() + tempYpercent - 3*i.height()/2)
                        qpainter.setPen(Qt.NoPen)
                        qpainter.drawEllipse(current_x, current_y, 150, 150)
                        brush = QBrush(QColor(100, 0, 0, 2))
                        qpainter.setBrush(brush)
                        qpainter.drawEllipse(current_x, current_y, 150, 150)


        for i in self.firefighterList:
            if(i.destination() != None):
                    tempXpercent = (i.destination().x() + i.destination().width()/2 - i.curPos().x() - i.curPos().width()/2) * i.getArcPercentage_FF(i.destination())
                    tempYpercent = (i.destination().y() + 3/2*i.destination().height() - i.curPos().y() - 3/2*i.curPos().height()) * i.getArcPercentage_FF(i.destination())
                    qpen = QPen(Qt.darkGreen, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2, i.curPos().y() + 5/2*i.curPos().height()), QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 5/2*i.curPos().height()+tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.curPos().x()+ i.curPos().width()/2, i.curPos().y() + 3/2*i.curPos().height()), QPointF(i.curPos().x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 3/2*i.curPos().height()+tempYpercent))
        self.update()
        qpainter.end()

    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        # if os.path.exists("FFInfo.json"):
        #     os.remove("FFInfo.json")
        if os.path.exists("filename.json"):
            os.remove("filename.json")
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
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)

    def comboBoxEvent(self,text):
        if(text == "Hybrid network"):
            self.showFFnetwork = False
            self.showFireNetwork = True
        elif(text == "FF network"):
            self.showFFnetwork = True
            self.showFireNetwork = True
        elif(text == "Fire network"):
            self.showFFnetwork = True
            self.showFireNetwork = False
        self.networkChange()



