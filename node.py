from PyQt5.QtGui import QPixmap, QCursor, QResizeEvent
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets,QtCore,QtGui
from nodeButtonController import NodeController
from nodePropertyVisualization import nodePropertyVis

class Node(QtWidgets.QPushButton):
    showSignal = pyqtSignal(int)
    def __init__(self, widgets, __nodeController: NodeController):
        super().__init__(widgets)
        self.__nodeController = __nodeController
        self.__UIsettings(self.__nodeController.getPos())
        # UI設定
        self.__node_opa_value = 0.3
        self.__node_opa_shift = 1
        self.timer_nodeOpacity = QTimer()
        self.timer_nodeOpacity.timeout.connect(self.opacityAffect)
        self.grassVisualize = nodePropertyVis(widgets,self.__nodeController)
    

    #UI設定
    def __UIsettings(self, pos):
        #設定位置
        self.setGeometry(pos)
        self.setText(str(self.__nodeController.getNum()))

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.showSignal.emit(self.getNum())
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def getFireMinArrivalTime(self):
        return self.__nodeController.getFireMinArrivalTime()

    def opacityAffect(self):
        self.__node_opa_value += 0.1 * self.__node_opa_shift
        if self.__node_opa_value >= 0.8:
            self.__node_opa_shift = -1
        elif self.__node_opa_value <= 0.3:
            self.__node_opa_shift = 1
        self.setStyleSheet(f'background-color: rgba(0, 255, 255, {self.__node_opa_value}); color: white;')

    #設置node狀態
    def onFire(self):
        #onFire setting
        self.__nodeController.onFire()
        self.setStyleSheet(self.__nodeController.getStyle())

    def defend(self):
        self.__nodeController.defend()
        self.setStyleSheet(f'background-color: rgba(0, 255, 0, {0.1});' + "border: 2px solid blue;")

    def depotSetting(self):
        self.__nodeController.depotSetting()
        self.setStyleSheet("background-color: black;")
        
    def isDepot(self):
        return self.__nodeController.isDepot()

    def ffidle(self):
        self.__nodeController.ffidle()

    def setStyle(self, style) -> None:
        return self.__nodeController.setStyle(style)

    def nextFFProgress(self):
        self.__nodeController.ffProgressing()

    #get functions

    def getValue(self):
        return self.__nodeController.getValue()

    def isBurned(self):
        return self.__nodeController.isBurned()

    def isProtected(self):
        return self.__nodeController.isProtected()

    '''def isIdle(self):
        return self.__nodeController.idle'''

    def getNeighbors(self):
        return self.__nodeController.getNeighborButton()

    def getArc(self, node):
        return self.__nodeController.getArc(node.__nodeController)

    def getNum(self):
        return self.__nodeController.getNum()

    def getArcs(self):
        return self.__nodeController.getArcs()

    def getStatus(self):
        return self.__nodeController.getStatus()

    def getProcessingTime(self):
        return self.__nodeController.getGrassAmount()

    def getStyle(self):
        return self.__nodeController.getStyle()

    #get function (計算獲得)

    def getNodePercentage_Fire(self): #獲得火在該node的燃燒進度
        return self.__nodeController.getNodePercentage_Fire()
    
    def getNodePercentage_FF(self, rate): #獲得消防員在該node的燃燒進度
        return self.__nodeController.getNodePercentage_FF(rate)

    def updateStatus(self):
        self.__nodeController.updateStatus()

    #一開始建立網路時使用
    def connectNode(self, node):
        self.__nodeController.connectButton(node)
