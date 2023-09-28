from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal,QRect
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
import math

class NodeController():
    def __init__(self, i, pos: QtCore.QRect, value, burnTime, quantity):
        self.pos = pos
        #variables
        self.__no = i
        self.__initValue = value
        self.value = value
        self.fireMinArrivalTime = 10000
        self.burningTime = burnTime
        self.fireProgress = 0
        self.ffProgress = 0
        self.quantity = quantity
        self.__neighbors = [] #表示與那些node有相鄰關係
        self.__adjArc = [] #以dict紀錄arc {node: 相鄰節點, length: 之間arc的長度, fire-travel: 火在arc上已移動多少, FF-travel: FF在arc上已移動多少}
        self.__burned = False
        self.protected = False
        self.depot = False
        self.idle = False
        self.__neighbors : NodeController = []
        self.__adjArc : dict = []
        self.status = "Normal"
        self.style = ""


    #設置node狀態
    def onFire(self):
        #onFire setting
        self.__burned = True
        self.style = f'background-color: rgba(255, 0, 0, {0.1});'

    def defend(self):
        self.protected = True
        self.idle = False

    def depotSetting(self):
        self.protected = True
        self.depot = True
        self.style = "background-color: black;"

    def getStyle(self):
        return self.style
    
    def setStyle(self, style):
        self.style = style

    def isDepot(self):
        return self.depot

    def ffidle(self):
        self.idle = True
        #self.protected = False

    def updateValue(self):
        self.value = self.__initValue * self.getNodePercentage_Fire()

    #get functions
    def isBurned(self):
        return self.__burned

    def isProtected(self):
        return self.protected

    def isIdle(self):
        return self.idle

    def getNeighbors(self):
        return self.__neighbors

    def getArc(self, node):
        return next((i for i in self.__adjArc if i["node"] == node), None)

    def getNum(self):
        return self.__no

    def getArcs(self):
        return self.__adjArc

    def getStatus(self):
        return self.status
    
    def getFireMinArrivalTime(self):
        return self.fireMinArrivalTime

    #get function (計算獲得)
    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        ratio = 1 - (self.fireProgress / self.burningTime)
        return ratio if ratio >= 0 else 0
    
    def getNodePercentage_FF(self, rate): #獲得消防員在該node的燃燒進度
        ratio = self.ffProgress / (self.burningTime * self.quantity / rate)
        return ratio if ratio >= 0 else 0

    def updateStatus(self):
        if (self.idle == True):
            self.status = "FF Idle"
        elif(self.protected == True and self.ffProgress > 0):
            self.status = "Protected"
        elif (self.protected == True and self.ffProgress <= 0):
            self.status = "Safe"
        elif (self.__burned == True and self.fireProgress > 0):
            self.status = "Burned"
        elif (self.__burned == True and self.fireProgress == self.burningTime):
            self.status = "Damaged"
        else:
            self.status = "Normal"


    #一開始建立網路時使用
    def connectNode(self, node, length, time):
        self.__neighbors.append(node)
        self.__adjArc.append({"node": node, "nodeButton": None, "length": length, "fire-travel": 0, "travel-time": time})
    
    def connectButton(self, button):
        for i in self.__adjArc:
            if(button.getNum() == i["node"].getNum()):
                i["nodeButton"] = button