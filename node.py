from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
import math

class Node(QtWidgets.QPushButton):
    customSignal = pyqtSignal(str)
    leaveSignal = pyqtSignal(str)

    def __init__(self, widgets, label, i, pos):
        super().__init__(widgets)
        self.UIsettings(label, pos)
        #variables
        self.setProperty("no.", i) #node編號
        self.fireMinArrivalTime = 10000
        self.setProperty("water-amount",20) #即時澆水量 (目前是用減法計算)
        self.initialWaterAmount = 20   #消防員需澆多少水才能保護
        self.setProperty("grass-amount", 20) #即時燃燒量
        self.initialGrassAmount = 20   #火需要燒多少量才能移動
        self.setProperty("burned", False) #是否燒起
        self.setProperty("protected", False) #是否被保護

        self.__neighbors = [] #表示與那些node有相鄰關係
        self.__adjArc = [] #以dict紀錄arc {node: 相鄰節點, length: 之間arc的長度, fire-travel: 火在arc上已移動多少, FF-travel: FF在arc上已移動多少}
        self.flashingtimer = QTimer(self)
        self.flashing_interval = 500


    #UI設定function
    def UIsettings(self, label, pos):
        self.__label = label
        self.setGeometry(pos)
        self.image = label
        self.image.raise_()

    def setImage(self, image):
        self.__label.setPixmap(image)
    
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.customSignal.emit("self")
    
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.leaveSignal.emit("self")

      

    #設置node狀態
    def onFire(self):
        #onFire setting
        self.setProperty("burned", True)
        self.setStyleSheet(f'background-color: rgba(255, 0, 0, {0.1});')

    def preDefend(self):
        self.setStyleSheet("background-color: grey;" + "border: 2px solid blue;")

    def defend(self):
        self.setProperty("protected",True)
        self.setStyleSheet(f'background-color: rgba(0, 255, 0, {0.1});' + "border: 2px solid blue;")

    def depotSetting(self):
        self.setStyleSheet("background-color: black;")
        self.setProperty("protected", True)
        self.setProperty("depot",True)
    def isDepot(self):
        return self.property("depot")

    #update變數
    def updateGrassAmount(self, remain):
        remain = 0 if remain < 0 else remain
        self.setProperty("grass-amount", remain)

    def updateWaterAmount(self, remain):
        remain = 0 if remain < 0 else remain
        self.setProperty("water-amount", remain)    
    #get functions
    def isBurned(self):
        return self.property("burned")

    def isProtected(self):
        return self.property("protected")

    def getNeighbors(self):
        return self.__neighbors

    def getArc(self, node):
        for i in self.__adjArc:
            if(i["node"] == node):
                return i
        return -1

    def getNum(self):
        return self.property("no.")

    def getWaterAmount(self):
        return self.property("water-amount")

    def getGrassAmount(self):
        return self.property("grass-amount")

    def getArcs(self):
        return self.__adjArc

    def getLabel(self):
        return self.__label

    def getXposition(self):
        return self.pos().x()

    def getYposition(self):
        return self.pos().y()
    
    def setLabelVisibility(self):
        if self.__label.isVisible():
            self.__label.setVisible(False)
        else:
            self.__label.setVisible(True)

    def startFlashing(self):
        self.flashingtimer.start(self.flashing_interval)
        self.flashingtimer.timeout.connect(self.setLabelVisibility)


    def stopFlashing(self):
        self.flashingtimer.stop()
        self.__label.setVisible(True) 
    #get function (計算獲得)

    def getArcPercentage_Fire(self, node): #獲得火在arc上的移動進度
        if(not node in self.__neighbors):
            return -1
        for i in self.__adjArc:
            if(i["node"] == node): 
                ratio = i["FF-travel"]/i["length"]
                return ratio if ratio <= 1 else 1 
    
    def getArcPercentage_FF(self, node): #獲得消防員在arc上的移動進度
        if(not node in self.__neighbors):
            return -1
        for i in self.__adjArc:
            if(i["node"] == node): 
                ratio = i["FF-travel"]/i["length"]
                return ratio if ratio <= 1 else 1 

    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        ratio = self.property("grass-amount")/self.initialGrassAmount
        return ratio if ratio >= 0 else 0
    
    def getNodePercentage_FF(self): #獲得消防員在該node的燃燒進度
        ratio = self.property("water-amount")/self.initialWaterAmount
        return ratio if ratio >= 0 else 0

    def arc_finish_spread(self, Arc): #回傳是否火在該arc已完成移動
        if(self.getGrassAmount() > 0):
            return False
        if(Arc in self.__adjArc):
            if(Arc["fire-travel"] >= Arc["length"]):
                return True
        return False

    #一開始建立網路時使用
    def connectNode(self, node, length):
        self.__neighbors.append(node)
        self.__adjArc.append({"node": node, "length": length, "fire-travel": 0, "FF-travel": 0})