#!/usr/bin/env python
# coding: utf-8
import json
import os
from functools import partial

import numpy as np
import pandas as pd
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel, QSizePolicy, QPushButton, QWidget, QGraphicsDropShadowEffect
from PyQt5 import QtWidgets, QtCore, QtGui
import math
from FFSettingsWindow import FFnumWindow
from FF import FireFighter
from node import Node
from fireObject import Fire
from network import Network
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QCursor, QColor, QIcon, QBrush, QRegion
from PyQt5 import uic
from dataBase import DataBase
import sys
from PIL import ImageGrab

FFNum = 1


class SimulationWindow(QtWidgets.QMainWindow):
    buttonlist = []
    modelTest: bool = False
    fire: list[Fire] = []
    nodeList: list[Node] = []
    firefighterList: list[FireFighter] = []  # store all firefighter (class: FireFighter)
    firefighterNum = 2
    nodeNum = len(nodeList)
    FFindex = 0
    # focusIndex = 14
    labels: QtWidgets.QLabel = []
    timer = QTimer()
    currentTime = 0
    pageList = -1
    FFnetwork: Network = None
    fireNetwork: Network = None
    showFFnetwork: bool = True
    showFireNetwork: bool = True
    FFInfoDict = []
    totalValue = 0
    availFF = 0
    screenshot_range = (290, 60, 1900, 751)
    gameTerminated = False
    model_dir = "./network/FF2test/FFP_n20_no5"


    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        global FFNum
        uic.loadUi("simulateWindow.ui", self)
        if os.path.exists("FFInfo.json"):
            with open("FFInfo.json", 'r') as file:
                data = json.load(file)
            FFNum = int(data["FFnumber"])
        self.firefighterNum = FFNum
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
        def initNetwork():  # 建立network class和node
            self.FFnetwork = Network(f"{self.model_dir}.xlsx", depot="N_D")
            self.fireNetwork = Network(f"{self.model_dir}.xlsx", depot="N_F")
            for i in self.FFnetwork.nodeList:
                node = Node(self.gamewidget, i)
                node.clicked.connect(self.choose)
                node.setEnabled(False)
                node.showSignal.connect(self.InfoShow)
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(5)
                shadow.setXOffset(5)
                shadow.setYOffset(5)
                node.setGraphicsEffect(shadow)
                self.nodeList.append(node)
                self.totalValue += node.getValue()
            self.progressBar.setMaximum(self.totalValue)
            self.progressBar.setValue(self.totalValue)

        initNetwork()
        self.nodeNum = len(self.nodeList)

        def initUI():  # UI設定(可略)
            self.focusIndex = len(self.nodeList) - 1
            self.button_menu.clicked.connect(self.backMenu)
            self.button_menu.setFlat(True)
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.7)
            self.actionNew.triggered.connect(self.newNetwork)
            self.idleButton.clicked.connect(self.assignIdle)
            self.defendButton.clicked.connect(self.choose)
            self.checkBox.toggled.connect(self.idleLock)
            self.lcd_time.display(self.currentTime)
            self.comboBox_network.activated[str].connect(self.comboBoxEvent)
            self.button_play.clicked.connect(self.modelTimeSet)
            self.button_stop.clicked.connect(self.stopSimulation)
            self.button_temp.clicked.connect(self.startSimulation)
            self.buttonsetTime.clicked.connect(self.setTime)
            self.buttonlist.append(self.button_user)
            self.buttonlist.append(self.button_model)
            self.buttonlist.append(self.button_aco)
            self.buttonlist.append(self.button_ga)
            self.buttonlist.append(self.button_ra)
            for i in self.buttonlist:
                i.setCheckable(True)
                i.clicked.connect(self.buttonClicked)
            self.button_model.setChecked(True)
        initUI()

        def NodeConnection():
            for sourceNode in self.nodeList:
                for arc in sourceNode.getArcs():
                    destNode = self.nodeList[arc["node"].getNum() - 1]
                    sourceNode.connectNode(destNode)

        NodeConnection()

        def randomFireAndDepot():  # 初始化火和消防員
            # 初始化火
            fireDepot = next((i.getNum() for i in self.fireNetwork.nodeList if i.isDepot()), None)
            self.fire.append(Fire(self.fireNetwork, fireDepot, self.currentTime))
            self.fire[-1].burn()
            self.nodeList[fireDepot - 1].onFire()
            self.fire[-1].fireSignal.connect(self.fireSignalDetermination)
            # 初始化消防員
            self.updateMinTime()
            depot = next((i for i in self.nodeList if i.isDepot()), None)
            self.networkUpdate(depot.getNum())
            self.firefighterNum = int(self.FFnetwork.ffNum)
            for i in range(self.firefighterNum):
                ff = FireFighter(self.gamewidget, i + 1, depot)
                df = pd.read_excel(f"{self.model_dir}.xlsx", sheet_name=None)
                ff.rate_extinguish = df["ff_source"]["P"][i]
                ff.FFSignal.connect(self.ffSignalDetermination)
                depot.depotSetting()
                self.firefighterList.append(ff)
        randomFireAndDepot()
        self.label_selectedFF.setText(
            self.firefighterList[self.FFindex].getName())  # UI SETTING: put here because the order of initialization
        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)
        self.selectFireFighter()
        self.selectFireFighter()
        self.updateFFStatus()

        self.howManyAvail()
        self.criticalMessage = "firefighter available: {}".format(self.availFF)
        self.hintAnimate(self.criticalMessage)

        self.defendButton.setEnabled(not self.firefighterList[self.FFindex].curPos().isProtected())

    def modelTimeSet(self):
        self.modelTest = True
        if os.path.exists(f"{self.model_dir}_data.json"):
            with open(f"{self.model_dir}_data.json", 'r') as file:
                data = json.load(file)
                DataBase.T = data["T"][-1]
                DataBase.tau = data["tau"]
                DataBase.Q = data["q"]
                DataBase.b = data["b"]
                DataBase.u_bar = data["u_bar"]
                DataBase.K = data["K"]
                DataBase.lamb = data["lamb"]
                DataBase.P = data["p"]
                DataBase.H = data["h"]
                self.epsilon = 1e-4
                self.X = data["x"]
                import ast
                self.temp = []
                self.back = []
                for k in DataBase.K:
                    self.temp.append([ast.literal_eval(elem) for elem in self.X if ast.literal_eval(elem)[2] == k])
        self.modelTime = QTimer()
        self.modelTime.timeout.connect(self.modelAuto)
        self.modelTime.setInterval(100)
        self.modelTime.start()

    def modelAuto(self):
        if (self.currentTime >= DataBase.T):
            self.finish()
            self.modelTime.stop()
            return
        if (self.gameTerminated):
            self.modelTime.stop()
            return
        print(self.back)
        print(f'CurrentTime{self.currentTime}')
        (i, j, k, t) = (1, 1, 1, 100000)
        ss = 0
        for s in DataBase.K:
            (i1, j1, k1, t1) = (self.temp[s - 1][0][0], self.temp[s - 1][0][1], self.temp[s - 1][0][2], self.temp[s - 1][0][3])
            while (self.X[f"({i1}, {j1}, {k1}, {t1})"] < self.epsilon):
                self.temp[s - 1].pop(0)
                (i1, j1, k1, t1) = (self.temp[s - 1][0][0], self.temp[s - 1][0][1], self.temp[s - 1][0][2], self.temp[s - 1][0][3])
            if (t1 < t):
                ss = s
                (i, j, k, t) = (i1, j1, k1, t1)
        self.focusIndex = j - 1
        self.FFindex = k - 1
        # print((i,j,k,t) )
        # print(f"t:{t}, cur: {self.currentTime}")
        if t == self.currentTime:
            self.back.append(self.temp[ss - 1][0])
            if i != j:
                self.choose()
                self.consoleLabel.setText("在時刻 {} 從node {} 移動到 node {} ,travel time: {}".format(t, i, j,DataBase.tau[f"({i}, {j}, {float(k)})"]))
            else:
                if DataBase.u_bar[f"({i}, {k}, {t})"] > self.epsilon:
                    self.choose()
                    self.consoleLabel.setText("在時刻 {} 對node {} 進行保護, processing time: {}".format(t, i,math.ceil(DataBase.Q[f"{i}"] *DataBase.b[f"{i}"] /self.firefighterList[self.FFindex].rate_extinguish)))
                else:
                    self.assignIdle()
                    self.consoleLabel.setText("在時刻 {} 在node {} idle".format(t, i))
            if (self.currentTime >= DataBase.T):
                self.modelTime.stop()
                self.timer.stop()
                self.finish()
                return
            if (t == self.currentTime):
                self.temp[ss - 1].pop(0)

    def howManyAvail(self):
        self.availFF = len([ff for ff in self.firefighterList if ff.getcumArrivalTime() == self.currentTime])

    def assignIdle(self):
        if (self.firefighterList[self.FFindex].isSelected()):
            return "this firefighter is busy"

        if (self.firefighterList[
            self.FFindex].curPos().getFireMinArrivalTime() < self.currentTime + self.spinBox.value()):
            self.hintAnimate("fire will arrive during idle")
            return
        self.availFF -= 1
        if (not self.modelTest):
            self.hintAnimate("firefighter available: {}".format(self.availFF))
        if (not self.firefighterList[(self.FFindex + 1) % self.firefighterNum].isSelected()):
            self.selectFireFighter()
        self.updateFFStatus()
        self.nextTime()
        return "assign idle"

    def idleLock(self):
        if (self.checkBox.isChecked()):
            self.spinBox.setValue(99)
        self.spinBox.setEnabled(not self.checkBox.isChecked())

    '''---------------------------------------firefighter signal-----------------------------------------'''

    def ffSignalDetermination(self, text, no):
        if (text == "done"):
            self.updateFFStatus()
        if (text == "protect"):
            self.networkUpdate(no)
        if (text == "trapped"):
            self.criticalMessage = f"firefighter {no} can't move to other nodes, please assign protect or idle to the end"
            self.hintAnimate(self.criticalMessage)

    def networkUpdate(self, no):  # FF network有節點被保護時呼叫，更新fire network
        self.fireNetwork.nodeList[no - 1].defend()
        self.updateMinTime()

    def updateMinTime(self):  # 更新FF network的fireMinArrivalTime
        for i in self.fireNetwork.nodeList:
            i.setFireMinArrivalTime(10000)

        [i.minTimeFireArrival() for i in self.fire]

        for i in self.FFnetwork.nodeList:
            i.setFireMinArrivalTime(self.fireNetwork.nodeList[i.getNum() - 1].getFireMinArrivalTime())

    def updateFFStatus(self):  # 消防員移動/澆水完成時呼叫，更新消防員的狀態
        for i in range(self.firefighterNum):
            self.firefighterList[i].updateStatus()

    '''------------------------------------------fire signal---------------------------------------------'''

    def fireSignalDetermination(self, text, opacity=0, no=0):
        if (text == "burn"):
            self.networkUpdateF(no)
        if (text == "visual"):
            self.fireVisualize(opacity, no)

    def networkUpdateF(self, no):  # 當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        self.nodeList[no - 1].onFire()
        self.fire.append(Fire(self.fireNetwork, no, self.currentTime))
        self.listWidget.addItem(f"At time {self.currentTime}, node {no} had burned")
        self.listWidget.scrollToItem(self.listWidget.item(self.listWidget.count() - 1))
        self.fire[-1].fireSignal.connect(self.fireSignalDetermination)

    def fireVisualize(self, opacity, no):  # 當fire network的節點正在燃燒時，更新ui上的opacity
        self.fireNetwork.nodeList[no - 1].updateStatus()
        self.nodeList[no - 1].setStyle(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
        if (opacity == 1):
            self.nodeList[no - 1].setStyle(f'background-color: rgba(139, 0, 0, {opacity}); color: white;')
        self.nodeList[no - 1].setStyleSheet(self.nodeList[no - 1].getStyle())
        self.nodeList[no - 1].updateStatus()
        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)

    def finish(self):
        self.timer.stop()
        if os.path.exists("filename.json"):
            os.remove("filename.json")

    '''------------------------------操作方式-----------------------------------'''

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if (a0.key() == Qt.Key_S):
            self.networkChange()
        if (a0.key() == Qt.Key_N):
            self.newNetwork()
        if (a0.key() == Qt.Key_Q):
            self.finish()
        if (a0.key() == Qt.Key_X):
            self.showProperty(1)
        if (a0.key() == Qt.Key_Z):
            self.showProperty(0)
        if (a0.key() == Qt.Key_A):
            self.modelTimeSet()
        self.updateFFStatus()

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        for i in self.nodeList:
            i.grassVisualize.hide()

    def showProperty(self, key):
        for i in self.nodeList:
            if (key):
                i.grassVisualize.showGrassValue()
                i.grassVisualize.setText(
                    str(math.ceil(i.getProcessingTime() / self.firefighterList[self.FFindex].rate_extinguish)))
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
        if (self.showFFnetwork and self.showFireNetwork):
            self.showFireNetwork = False
            self.comboBox_network.setCurrentIndex(2)
        elif (self.showFFnetwork and not self.showFireNetwork):
            self.showFFnetwork = False
            self.showFireNetwork = True
            self.comboBox_network.setCurrentIndex(1)
        elif (not self.showFFnetwork and self.showFireNetwork):
            self.showFFnetwork = True
            self.comboBox_network.setCurrentIndex(0)

    def __nextHintAnim(self):
        if self.index < len(self.text):
            self.consoleLabel.setText(self.text[:self.index + 1])
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

    def InfoShow(self, no):  # 查看node資訊
        # 處理顯示文字
        if (no == -1):
            self.hintAnimate(self.criticalMessage)
            return
        if (self.sender().isProtected()):
            status = "Protected"
        elif (self.sender().isBurned()):
            status = "Burned"
        else:
            status = "Normal"

        text = "Node: {} ({}), \nEarlist burn time: {}, \nTravel time: ".format(self.sender().getNum(), status,
                                                                                self.sender().getFireMinArrivalTime())
        if (self.firefighterList[self.FFindex].curPos().getArc(self.sender()) != None):
            text += str(
                self.firefighterList[self.FFindex].curPos().getArc(self.sender())["travel-time"][f"{self.FFindex + 1}"])
        else:
            text += "not neighbor"
        if (not self.modelTest):
            self.hintAnimate(text)

    def selectFireFighter(self):  # 切換選擇消防員
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].setPixmap(self.firefighterList[self.FFindex].grab())
        self.firefighterList[self.FFindex - 1].closeaccessibleVisualize(self.nodeList)
        self.firefighterList[self.FFindex].accessibleVisualize(self.currentTime, self.nodeList)
        image = self.firefighterList[self.FFindex].grab()
        scaled_pixmap = image.scaled(self.selectLabel.width(), self.selectLabel.height())
        self.selectLabel.setPixmap(scaled_pixmap)

    def __opacitySet(self):  # 調整FF的opacity
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
            if (ff.isSelected()):
                return
            else:
                text = func(self)
                self.availFF -= text[1]
                if (not self.modelTest):
                    self.criticalMessage = "firefighter available: {}".format(self.availFF)
                    self.hintAnimate(self.criticalMessage)
                if (not self.firefighterList[(self.FFindex + 1) % self.firefighterNum].isSelected() and text[1] == 1):
                    self.selectFireFighter()
            self.updateFFStatus()

            self.nextTime()

        return aa

    @printStatus
    def choose(self):  # 指派消防員移動至給定node
        send = None
        if (not self.modelTest):
            self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
            send = self.firefighterList[self.FFindex].curPos() if self.sender().objectName() == "defendButton" else self.sender()
        else:
            send = self.nodeList[self.focusIndex]
        text = self.checkStatus(send)
        if (text == "vaild choose"):
            if (self.firefighterList[self.FFindex].destination() == send):  # 是否選擇取消(再次點擊同node)
                self.firefighterList[self.FFindex].reset()
                send.setStyleSheet("")
                return ("{} reset".format(self.firefighterList[self.FFindex].getName()), -1)
            text = self.firefighterList[self.FFindex].processCheck(send)
            self.firefighterList[self.FFindex].updateStatus()
            return (text, 1)
        return (text, 0)


    def checkStatus(self, node):
        if (self.firefighterList[self.FFindex].isProcess()):
            return "this firefighter is busy"
        if (self.firefighterList[self.FFindex].isTraveling()):
            return "this firefighter is busy"
        if (node == self.firefighterList[self.FFindex].curPos()):
            return "vaild choose"
            # check if selected FireFighter can move to assigned Node
        text = self.firefighterList[self.FFindex].next_Pos_Accessment(node, self.currentTime)
        return text

    def nextTime(self):  # 跳轉至下一個時間點
        def timeSkip():
            screenshot = ImageGrab.grab(self.screenshot_range)
            screenshot.save(f"image/timescreenshot/time00{self.currentTime:03d}.png")
            self.gameTerminated = all(i.isComplete() for i in self.fire)
            if self.gameTerminated:
                self.finish()
                if (self.modelTest):
                    self.modelTime.stop()
                return
            self.currentTime += 1
            for i in self.nodeList:
                i.updateStatus()
            for i in self.fire:
                i.fire_spread()
            finishList = []
            for i in self.firefighterList:
                i.updateStatus()
                # print(f"{i.getcumArrivalTime()}, {self.currentTime}")
                (check, text) = i.checkArrival(self.currentTime)
                if (check):
                    finishList.append(i.getNum())
                    screenshot = ImageGrab.grab(self.screenshot_range)
                    screenshot.save(f"image/timescreenshot/time00{self.currentTime:03d}.png")
                    self.timer.stop()
                    self.listWidget.addItem(text)
                    self.listWidget.scrollToItem(self.listWidget.item(self.listWidget.count() - 1))
                    self.howManyAvail()

                    if (not self.modelTest):
                        self.criticalMessage = "firefighter available: {}".format(self.availFF)
                        self.hintAnimate(self.criticalMessage)
                    self.defendButton.setEnabled(not i.curPos().isProtected())
            if (finishList):
                text = ""
                for i in finishList:
                    text += str(i) + " "
                self.FFindex = finishList[0] - 2
                self.selectFireFighter()

            self.label_selectedFF.setText(self.firefighterList[self.FFindex].getName())
            self.__opacitySet()
            self.lcd_time.display(self.currentTime)

        if (not self.availFF):
            for ff in self.firefighterList:
                if (not (ff.isTraveling() or ff.isProcess())):
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
        qpainter = QPainter()
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        if (self.showFireNetwork):
            qpen = QPen(Qt.red, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    qpainter.drawLine(
                        QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                        QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))


            for i in self.nodeList:
                i.setText(str(i.getFireMinArrivalTime()))
        if (self.showFFnetwork):
            qpen = QPen(Qt.black, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                i.setText(str(i.getNum()))
                for j in i.getNeighbors():
                    qpainter.drawLine(
                        QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                        QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))

        for i in self.fire:
            for j in i.getArcs():
                tempXpercent = (j["node"].x() + j[
                    "node"].width() / 2 - i.x() - i.width() / 2) * i.getArcPercentage_Fire(j)
                tempYpercent = (j["node"].y() + 3 / 2 * j[
                    "node"].height() - i.y() - 3 / 2 * i.height()) * i.getArcPercentage_Fire(j)
                qpen = QPen(Qt.darkRed, 6, Qt.SolidLine)
                qpainter.setPen(qpen)
                qpainter.drawLine(QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                                  QPointF(i.x() + self.gamewidget.x() + i.width() / 2 + tempXpercent,
                                          i.y() + 5 / 2 * i.height() + tempYpercent))

        for i in self.firefighterList:
            if (i.destination() != None):
                tempXpercent = (
                                           i.destination().x() + i.destination().width() / 2 - i.curPos().x() - i.curPos().width() / 2) * i.getArcPercentage_FF(
                    i.destination())
                tempYpercent = (
                                           i.destination().y() + 3 / 2 * i.destination().height() - i.curPos().y() - 3 / 2 * i.curPos().height()) * i.getArcPercentage_FF(
                    i.destination())
                qpen = QPen(Qt.darkGreen, 6, Qt.SolidLine)
                qpainter.setPen(qpen)
                qpainter.drawLine(QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width() / 2,
                                          i.curPos().y() + 5 / 2 * i.curPos().height()), QPointF(
                    i.curPos().x() + self.gamewidget.x() + i.curPos().width() / 2 + tempXpercent,
                    i.curPos().y() + 5 / 2 * i.curPos().height() + tempYpercent))
        self.update()
        qpainter.end()

    def closeEvent(self, event):  # 當主視窗關閉時關閉全部視窗
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

    def backMenu(self):
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)

    def comboBoxEvent(self, text):
        if (text == "Hybrid network"):
            self.showFFnetwork = False
            self.showFireNetwork = True
        elif (text == "FF network"):
            self.showFFnetwork = True
            self.showFireNetwork = True
        elif (text == "Fire network"):
            self.showFFnetwork = True
            self.showFireNetwork = False
        self.networkChange()

    def stopSimulation(self):
        self.modelTime.stop()

    def startSimulation(self):
        self.modelTime.start()

    def setTime(self):
        # print(self.back)
        # self.temp.insert(0, self.back[-1])
        # self.currentTime = self.back[-1][3]
        # self.lcd_time.display(self.currentTime)
        for ff in self.firefighterList:
            if self.back[-1][2] == ff.getNum()+1:
                print(f'curpos{ff.curPos()}')
                # ff.__path.pop(-1)
                # ff.newPos()
                # self.back.pop(-1)

    def buttonClicked(self):
        sender_button = self.sender()
        for i in self.buttonlist:
            i.setChecked(False)
        sender_button.setChecked(True)
