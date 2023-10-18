from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal,QRect
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
import math

class NodeController():
    def __init__(self, i, pos: QtCore.QRect, value, burnTime, quantity):
        self.__pos = pos
        #variables
        
        self.__no = i
        self.__initValue = value
        self.__value = value
        self.__fireMinArrivalTime = 10000
        self.__burningTime = burnTime
        self.__fireProgress = 0
        self.__ffProgress = 0
        self.__burned = False
        self.__protected = False
        self.__depot = False
        self.__adjArc : dict = []
        self.__status = "Normal"
        self.__style = ""
        self.__grassAmount = int(quantity * self.__burningTime)

    def getPos(self):
        return self.__pos
    def x(self):
        return self.__pos.x()
    def y(self):
        return self.__pos.y()
    def width(self):
        return self.__pos.width()
    def height(self):
        return self.__pos.height()

    #設置node狀態
    def onFire(self):
        #onFire setting
        self.__burned = True
        self.__style = f'background-color: rgba(255, 0, 0, {0.1});'

    def defend(self):
        self.__protected = True

    def depotSetting(self):
        self.__protected = True
        self.__depot = True
        self.__style = "background-color: black;"

    def getStyle(self):
        return self.__style

    def getGrassAmount(self):
        return self.__grassAmount
    
    def setStyle(self, style):
        self.__style = style

    def isDepot(self):
        return self.__depot

    def fireProgressing(self):
        self.__fireProgress+=1
        
    def ffProgressing(self):
        self.__ffProgress+=1

    def getFireProgress(self):
        return self.__fireProgress

    def updateValue(self):
        self.__value = self.__initValue * self.getNodePercentage_Fire()

    def getBurningTime(self):
        return self.__burningTime

    def getValue(self):
        return self.__value

    #get functions
    def isBurned(self):
        return self.__burned

    def isProtected(self):
        return self.__protected

    def getNeighbors(self):
        return [arc["node"] for arc in self.__adjArc]

    def getArc(self, node):
        return next((i for i in self.__adjArc if i["node"] == node), None)

    def getNum(self):
        return self.__no

    def getArcs(self):
        return self.__adjArc

    def getStatus(self):
        return self.__status
    
    def getFireMinArrivalTime(self):
        return self.__fireMinArrivalTime

    def setFireMinArrivalTime(self, time):
        self.__fireMinArrivalTime = time

    #get function (計算獲得)
    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        ratio = 1 - (self.__fireProgress / self.__burningTime)
        return ratio if ratio >= 0 else 0
    
    def getNodePercentage_FF(self, rate): #獲得消防員在該node的燃燒進度
        ratio = self.__ffProgress / (self.__grassAmount / rate)
        return ratio if ratio >= 0 else 0

    def updateStatus(self):
        if(self.__protected == True and self.__ffProgress > 0):
            self.__status = "Protected"
        elif (self.__protected == True and self.__ffProgress <= 0):
            self.__status = "Safe"
        elif (self.__burned == True and self.__fireProgress > 0):
            self.__status = "Burned"
        elif (self.__burned == True and self.__fireProgress == self.__burningTime):
            self.__status = "Damaged"
        else:
            self.__status = "Normal"

    def arcAddTime(self, node, no, time):
        for i in self.__adjArc:
            if i["node"] == node:
                i["travel-time"][f"{int(no)}"] = time

    #一開始建立網路時使用
    def connectNode(self, node, length, no, time):
        if(no==None):
            self.__adjArc.append({"node": node, "nodeButton": None, "length": length, "fire-travel": 0, "travel-time": time})
        else:
            self.__adjArc.append({"node": node, "nodeButton": None, "length": length, "fire-travel": 0, "travel-time": {f"{int(no)}":time}})
    def connectButton(self, button):
        for i in self.__adjArc:
            if(button.getNum() == i["node"].getNum()):
                i["nodeButton"] = button

    def getNeighborButton(self):
        return [arc["nodeButton"] for arc in self.__adjArc]