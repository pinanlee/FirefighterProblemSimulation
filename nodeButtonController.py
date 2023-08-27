from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal,QRect
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
import math

class NodeController():
    customSignal = pyqtSignal(str)
    leaveSignal = pyqtSignal(str)
    def __init__(self, i, pos: QtCore.QRect):
        self.pos = pos
        #variables
        self.no = i
        self.value = 100
        self.fireMinArrivalTime = 10000
        self.initialWaterAmount = 20   #消防員需澆多少水才能保護
        self.initialGrassAmount = 20   #火需要燒多少量才能移動
        self.water_amount = 20
        self.grass_amount = 20
        self.__neighbors = [] #表示與那些node有相鄰關係
        self.__adjArc = [] #以dict紀錄arc {node: 相鄰節點, length: 之間arc的長度, fire-travel: 火在arc上已移動多少, FF-travel: FF在arc上已移動多少}
        self.burned = False
        self.protected = False
        self.depot = False
        self.idle = False
        self.__neighbors = []
        self.__adjArc = []
        self.status = "Normal"

    #設置node狀態
    def onFire(self):
        #onFire setting
        self.burned = True

    def defend(self):
        self.protected = True
        self.idle = False

    def depotSetting(self):
        self.protected = True
        self.depot = True
        
    def isDepot(self):
        return self.depot

    def ffidle(self):
        self.idle = True
        self.protected = False

    #update變數
    def updateGrassAmount(self, remain):
        remain = 0 if remain < 0 else remain
        self.grass_amount = remain

    def updateWaterAmount(self, remain):
        remain = 0 if remain < 0 else remain
        self.water_amount = remain

    #get functions
    def isBurned(self):
        return self.burned

    def isProtected(self):
        return self.protected

    def isIdle(self):
        return self.idle

    def getNeighbors(self):
        return self.__neighbors

    def getArc(self, node):
        for i in self.__adjArc:
            if(i["node"] == node):
                return i
        return -1

    def getNum(self):
        return self.no

    def getWaterAmount(self):
        return self.water_amount

    def getGrassAmount(self):
        return self.grass_amount

    def getArcs(self):
        return self.__adjArc
    def getStatus(self):
        return self.status

    #get function (計算獲得)
    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        ratio = self.grass_amount/self.initialGrassAmount
        return ratio if ratio >= 0 else 0
    
    def getNodePercentage_FF(self): #獲得消防員在該node的燃燒進度
        ratio = self.water_amount/self.initialWaterAmount
        return ratio if ratio >= 0 else 0

    def updateStatus(self):
        if (self.idle == True):
            self.status = "FF Idle"
        elif(self.protected == True and self.water_amount > 0):
            self.status = "Protected"
        elif (self.protected == True and self.water_amount <= 0):
            self.status = "Safe"
        elif (self.burned == True and self.grass_amount > 0):
            self.status = "Burned"
        elif (self.burned == True and self.grass_amount <= 0):
            self.status = "Damaged"
        else:
            self.status = "Normal"


    #一開始建立網路時使用
    def connectNode(self, node, length):
        self.__neighbors.append(node)
        self.__adjArc.append({"node": node, "length": length, "fire-travel": 0})