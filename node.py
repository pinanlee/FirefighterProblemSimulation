from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
import math
from nodeButtonController import NodeController

class Node(QtWidgets.QPushButton):
    def __init__(self, widgets, label, nodeController: NodeController):
        super().__init__(widgets)
        self.nodeController = nodeController
        self.UIsettings(label, self.nodeController.pos)

        self.__neighbors = [] #表示與那些node有相鄰關係
        self.__adjArc = [] #以dict紀錄arc {node: 相鄰節點, length: 之間arc的長度, fire-travel: 火在arc上已移動多少, FF-travel: FF在arc上已移動多少}

    #UI設定
    def UIsettings(self, label : QtWidgets.QLabel, pos):
        #設定位置
        self.setGeometry(pos)
        self.setText(str(self.nodeController.no))
        
        self.__label = label
        self.__label.setGeometry(pos)
        self.image = label
        self.image.raise_()


    def setImage(self, image):
        self.__label.setPixmap(image)

    def getFireMinArrivalTime(self):
        return self.nodeController.fireMinArrivalTime

    def updateGrassAmount(self, remain):
        self.nodeController.updateGrassAmount(remain)

    def updateWaterAmount(self, remain):
        self.nodeController.updateWaterAmount(remain)

    #設置node狀態
    def onFire(self):
        #onFire setting
        self.nodeController.burned = True
        self.setStyleSheet(f'background-color: rgba(255, 0, 0, {0.1});')

    def preDefend(self):
        self.setStyleSheet("background-color: grey;" + "border: 2px solid blue;")

    def defend(self):
        self.nodeController.protected = True
        self.nodeController.idle = False
        self.setStyleSheet(f'background-color: rgba(0, 255, 0, {0.1});' + "border: 2px solid blue;")

    def depotSetting(self):
        self.setStyleSheet("background-color: black;")
        self.nodeController.depotSetting()

    def isDepot(self):
        return self.nodeController.depot

    def ffidle(self):
        self.nodeController.idle = True
        self.nodeController.protected = False



    #get functions
    def isBurned(self):
        return self.nodeController.burned

    def isProtected(self):
        return self.nodeController.protected

    def isIdle(self):
        return self.nodeController.idle

    def getNeighbors(self):
        return self.__neighbors

    def getArc(self, node):
        for i in self.__adjArc:
            if(i["node"] == node):
                return i
        return -1

    def getNum(self):
        return self.nodeController.no

    def getWaterAmount(self):
        return self.nodeController.getWaterAmount()

    def getGrassAmount(self):
        return self.nodeController.getGrassAmount()

    def getArcs(self):
        return self.nodeController.getArcs()

    def getLabel(self):
        return self.__label

    #get function (計算獲得)

    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        ratio = self.nodeController.grass_amount/self.nodeController.initialGrassAmount
        return ratio if ratio >= 0 else 0
    
    def getNodePercentage_FF(self): #獲得消防員在該node的燃燒進度
        ratio = self.nodeController.water_amount/self.nodeController.initialWaterAmount
        return ratio if ratio >= 0 else 0

    #一開始建立網路時使用
    def connectNode(self, node, length):
        self.__neighbors.append(node)
        self.__adjArc.append({"node": node, "length": length})
