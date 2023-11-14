from PyQt5 import uic
from instruction import Instruction
from PyQt5.QtGui import QPixmap
from network import Network
import json
import os
from functools import partial
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
from dataBase import DataBase
from results import resultsWindow
import sys
from PIL import ImageGrab

class AnimationTimer(QTimer):
    def __init__(self) -> None:
        super().__init__()
        self.setInterval(300)

class flashTimer(QTimer):
    def __init__(self, widget) -> None:
        super().__init__()
        self.opa = 0.1
        self.ctr = 0
        self.up = True
        self.boss = widget
        self.style = self.boss.styleSheet()
        def flash():
            if self.boss == None:
                self.stop()
                return
            if self.ctr==3:
                self.opa = 0.1
                self.ctr = 0
                self.up = True
                self.boss.setStyleSheet(self.style)
                self.stop()
                return
            if not self.up:
                self.opa -= 0.1
                if self.opa <= 0.1:
                    self.up = True
                    self.ctr+=1
            else:    
                self.opa += 0.1
                if self.opa == 0.5:
                    self.up = False
            if self.boss != None:
                self.boss.setStyleSheet(self.style[:-1] + f"\tbackground-color: rgba(255, 170, 0, {self.opa});" + "}")
                return
            # self.boss.setStyleSheet(self.style[:-1] + f"\tbackground-color: rgba(255, 170, 0, {self.opa});" + "}")
        #self.boss.setStyleSheet(f"background-color: rgba(255, 170, 0, {self.opa});")        
        self.setInterval(100)
        self.timeout.connect(flash)


class Controller_Utils:
    def UIInitialize(controller):
        if controller.mode == 1:
            uic.loadUi("UIv4.ui", controller)
            controller.inst = Instruction(controller.centralWidget())
            controller.button_guide.clicked.connect(controller.showProblem)
            controller.button_guide.setFlat(True)

        elif controller.mode == 2:
            uic.loadUi("case1.ui",controller)
            pixmap = QPixmap("image/case1.jpg")
            controller.label_background.setPixmap(pixmap)
        elif controller.mode == 3:
            uic.loadUi("simulateWindow.ui", controller)
            controller.focusIndex = len(controller.nodeList) - 1
            controller.actionNew.triggered.connect(controller.newNetwork)
            controller.button_play.clicked.connect(controller.modelTimeSet)
            controller.button_stop.clicked.connect(controller.stopSimulation)
            controller.button_temp.clicked.connect(controller.startSimulation)
            controller.buttonlist.append(controller.button_user)
            controller.buttonlist.append(controller.button_model)
            controller.buttonlist.append(controller.button_aco)
            controller.buttonlist.append(controller.button_ga)
            controller.buttonlist.append(controller.button_ra)
            for i in controller.buttonlist:
                i.setCheckable(True)
                i.clicked.connect(controller.buttonClicked)
            controller.button_model.setChecked(True)

        controller.button_menu.clicked.connect(controller.backMenu)
        controller.button_menu.setFlat(True)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.7)
        if controller.mode != 3:
            controller.descriptionLabel.setGraphicsEffect(opacity_effect)
            controller.actionAnimation.triggered.connect(controller.showFFWindow)
        controller.idleButton.clicked.connect(controller.assignIdle)
        controller.defendButton.clicked.connect(controller.choose)
        controller.checkBox.toggled.connect(controller.idleLock)
        controller.lcd_time.display(controller.currentTime)
        controller.comboBox_network.activated[str].connect(controller.comboBoxEvent)

    
    def createNetworkInfrastructures(controller):
        if controller.mode == 1 or 3:
            controller.FFnetwork =Network(f"{controller.model_dir}.xlsx", depot="N_D")
            controller.fireNetwork = Network(f"{controller.model_dir}.xlsx", depot="N_F")

        elif controller.mode == 2:
            controller.FFnetwork = Network("./network/case1/FFP_case1.xlsx", depot="N_D")
            controller.fireNetwork = Network("./network/case1/FFP_case1.xlsx", depot="N_F") 

    def nodeListInitialize(controller):
        for i in controller.FFnetwork.nodeList:
            node = Node(controller.gamewidget, i)
            node.raise_()
            if controller.mode == 2:
                node.setFlat(True)
                tentList = [1,2,4,6,8,9,10,15,17,18,23]
                forestList = [3,5,7,11,12,13,14,16,19,20,21,22]
                if i.getNum() in tentList:
                    node.setFixedSize(60,50)
                    image1 = QIcon("image/tent.png")
                    node.setIcon(image1)
                    node.setIconSize(QtCore.QSize(50, 50))
                elif i.getNum() in forestList:
                    node.setFixedSize(60,60)
                    image = QIcon("image/tree.png")
                    node.setIcon(image)
                    node.setMask(QRegion(0, 0, 60, 60, QRegion.Ellipse))
                    node.setIconSize(QtCore.QSize(60, 50))
                    # node.setIconSize(controller.size())
            node.clicked.connect(controller.choose)
            node.showSignal.connect(controller.InfoShow)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(5)
            shadow.setXOffset(5)
            shadow.setYOffset(5)
            node.setGraphicsEffect(shadow)
            controller.nodeList.append(node)
            controller.totalValue+=node.getValue()    

    def nodeConnection(controller):
        for sourceNode in controller.nodeList:
            for arc in sourceNode.getArcs():
                destNode = controller.nodeList[arc["node"].getNum()-1]
                sourceNode.connectNode(destNode)

    def depotInitialize(controller):
        #初始化火
        fireDepot = next((i.getNum() for i in controller.fireNetwork.nodeList if i.isDepot()), None)
        controller.fire.append(Fire(controller.fireNetwork, fireDepot, controller.currentTime))
        controller.fire[-1].burn()
        controller.nodeList[fireDepot-1].onFire()
        controller.fire[-1].fireSignal.connect(controller.fireSignalDetermination)
        #初始化消防員
        controller.updateMinTime()
        depot = next((i for i in controller.nodeList if i.isDepot()), None)
        controller.networkUpdate(depot.getNum())
        controller.firefighterNum=int(controller.FFnetwork.ffNum)
        if os.path.exists("FFInfo.json"): #若有自定義的情況
                with open("FFInfo.json", 'r') as file:
                    data = json.load(file)
                controller.FFInfoDict = data["FFinfo"]
                for i in range(controller.firefighterNum):
                    ff = FireFighter(controller.gamewidget, i+1, depot)
                    df = pd.read_excel(f"{controller.model_dir}.xlsx", sheet_name=None)
                    ff.rate_extinguish = df["ff_source"]["P"][i]
                    ff.FFSignal.connect(controller.ffSignalDetermination)
                    depot.depotSetting()
                    controller.firefighterList.append(ff)
                for i in controller.firefighterList:
                    tempNum = i.getNum()
                    pixmap = QPixmap(controller.FFInfoDict[tempNum-1]["img"])
                    controller.labels.append(pixmap)
                    scaled_pixmap = pixmap.scaled(controller.labels[tempNum-1].size(), aspectRatioMode=Qt.KeepAspectRatio,
                                                  transformMode=Qt.SmoothTransformation)
                    i.setPixmap(scaled_pixmap)
                    i.rate_extinguish = int(controller.FFInfoDict[tempNum-1]["er"])
                    i.move_man = int(controller.FFInfoDict[tempNum-1]["ts"])
        else:
                for i in range(controller.firefighterNum):
                    ff = FireFighter(controller.gamewidget, i+1, depot)
                    df = pd.read_excel(f"{controller.model_dir}.xlsx", sheet_name=None)
                    ff.rate_extinguish = df["ff_source"]["P"][i]
                    ff.FFSignal.connect(controller.ffSignalDetermination)
                    depot.depotSetting()
                    controller.firefighterList.append(ff)

    def UIInformationInitialization(controller):
        
        controller.progressBar.setMaximum(controller.totalValue)
        controller.progressBar.setValue(controller.totalValue)

        controller.label_selectedFF.setText(controller.firefighterList[controller.FFindex].getName()) #UI SETTING: put here because the order of initialization
        
        controller.firefighterList[controller.FFindex].accessibleVisualize(controller.currentTime, controller.nodeList)
        # controller.opacitySet()
        if controller.mode != 3:
            controller.generateblockFF_gameWindow()
        controller.availFF = controller.firefighterNum
        controller.criticalMessage = "firefighter available: {}".format(controller.availFF)
        controller.hintAnimate(controller.criticalMessage)
        controller.defendButton.setEnabled(not controller.firefighterList[controller.FFindex].curPos().isProtected())
        controller.lcd_time.display(controller.currentTime)
        controller.setFocus()

    def getModelSolution(controller):
        controller.modelTest = True
        if os.path.exists(f"{controller.model_dir}_data.json"): 
            with open(f"{controller.model_dir}_data.json", 'r') as file:
                data = json.load(file)
                
                DataBase.T = data["T"][-1]
                DataBase.tau = data["tau"]
                DataBase.Q = data["q"]
                DataBase.b = data["b"]
                DataBase.u_bar = data["u_bar"]
                DataBase.K = data["K"]
                DataBase.X = data["x"]
                import ast
                controller.temp = []
                for k in DataBase.K:
                    controller.temp.append([ast.literal_eval(elem) for elem in DataBase.X if ast.literal_eval(elem)[2] == k and DataBase.X[f"({ast.literal_eval(elem)[0]}, {ast.literal_eval(elem)[1]}, {ast.literal_eval(elem)[2]}, {ast.literal_eval(elem)[3]})"] > DataBase.epsilon])
    


    def screenshot(range, time):
        screenshot = ImageGrab.grab(range)
        screenshot.save(f"image/timescreenshot/time00{time:03d}.png")

    def firefighterMoveLogic(controller):
        finishList = []
        for i in controller.firefighterList:
            (check ,text) = i.checkArrival(controller.currentTime)
            if(check):
                finishList.append(i.getNum())
                controller.timer.stop()
                controller.listWidget.addItem(text)
                controller.listWidget.scrollToItem(controller.listWidget.item(controller.listWidget.count() - 1))
                if(not controller.modelTest):
                    controller.criticalMessage ="firefighter available: {}".format(controller.availFF) 
                    controller.hintAnimate(controller.criticalMessage)
                controller.defendButton.setEnabled(not i.curPos().isProtected())
        return finishList
    
    def fireSpreadLogic(fireList):
        for i in fireList:
            i.fire_spread()
