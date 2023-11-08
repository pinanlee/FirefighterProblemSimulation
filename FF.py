from PyQt5.QtGui import QPixmap
from node import Node
from PyQt5.QtCore import QTimer, pyqtSignal, QRect, Qt
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
import math
import os

class FireFighter(QLabel):
    FFSignal = pyqtSignal(str, int)
    def __init__(self, widget, num, depot):
        super().__init__(widget)
        self.__num = num
        self.__name = "firefighter " + str(num) #消防員編號
        self.__path = [depot] #紀錄FF經過的node
        self.newPos()
        #變數
        self.__arrivalTime = 0 #下一個arc所需移動時間
        self.__cumArrivalTime = 0 #消防員抵達目的預計時間
        self.__select = False #是否被指派
        self.__travel = False #是否在移動
        self.__process = False #是否在澆水
        self.rate_extinguish = 3#澆水速率
        self.move_man = 4 #移動速率
        self.__destinationNode = None #下一個目的
        self.__pathProgress = 0
        self.__status = "Not ready"
        #UI設定
        self.setStyleSheet("border: none; background: transparent;")

        self.folder_path = "image/firefighter/"
        for _, _, files in os.walk(self.folder_path):
            self.pixmaploc = self.folder_path + files[self.__num-1]
            
        self.setPixmap(QPixmap(self.pixmaploc).scaled(self.size()))
        # self.setFixedSize()
        self.lower()
        self.arrowLabel = QLabel(self.parentWidget())
        self.timer_arrow = QTimer(self)
        self.show()

    def deleteLater(self) -> None:
        self.arrowLabel.deleteLater()
        super().deleteLater()

    def setOpacity(self, num):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(num)
        self.setGraphicsEffect(opacity_effect)

    def getNum(self):
        return self.__num

    def newPos(self):
        self.setGeometry(QRect(self.curPos().x()+20, self.curPos().y(),self.curPos().width()+ 20, self.curPos().height()+20))

    def reset(self):
        self.__select = False 
        self.__travel = False 
        self.__process = False
        self.__destinationNode = None
        self.__arrivalTime = 0
        self.__pathProgress = 0
        self.__status = "Not ready"

    def finishTimeSet(self, value):
        if(self.isIdle()):
            self.__arrivalTime = value
            self.__status = "Idling"
        self.__cumArrivalTime += self.__arrivalTime

    def destination(self):
        return self.__destinationNode

    def getcumArrivalTime(self):
        return self.__cumArrivalTime

    def move(self): #開始移動至目的地
        if(self.__destinationNode == self.curPos()):
            self.curPos().defend()
            self.process()
            self.FFSignal.emit("protect",self.curPos().getNum())
            return
        if(self.__destinationNode != None):
            self.traveling()

    def process(self): #消防員標記為澆水中
        self.__process = True
        self.__status = "Processing"

    def isProcess(self): #回傳是否消防員在澆水
        return self.__process

    def isTraveling(self): #消防員標記為移動中
        return self.__travel

    def traveling(self): #回傳是否消防員在移動
        self.__travel = True
        self.__status = "Traveling"

    def selected(self): #消防員標記為被指派
        self.__select = True
        self.__status = "Assigned!"

    def isSelected(self): #回傳是否消防員被指派
        return self.__select
    
    def isIdle(self):
        return not (self.__select or self.__process or self.__travel)

    def checkArrival(self, timer): #是否在timer時抵達目的地
        self.__destinationNode = self.curPos() if self.__destinationNode == None else self.__destinationNode
        self.__calculateCurrentCapacity()
        self.__wateringVisualize()
        self.setGeometry(QRect(self.curPos().x() + int(self.getArcPercentage_FF(self.__destinationNode)*(self.__destinationNode.x() - self.curPos().x())), self.curPos().y() + int(self.getArcPercentage_FF(self.__destinationNode)*(self.__destinationNode.y() - self.curPos().y())),self.curPos().width()+ 20, self.curPos().height()+20))
        for i in self.curPos().getArcs(): #對於現在位置的相鄰點
            if(i["nodeButton"] == self.__destinationNode):
                self.__calculateCurrentFFArrive(i)
        
        if(self.__cumArrivalTime == timer):
            self.__cumArrivalTime = timer
            text = ""
            if(self.isProcess()):
                text = f"At time {timer}, firefighter {self.__num} had finished process on node {self.curPos().getNum()}"
            elif(self.isTraveling()):
                text = f"At time {timer}, firefighter {self.__num} had traveled from node {self.curPos().getNum()} to node {self.__destinationNode.getNum()}"
            else:
                text = f"At time {timer}, firefighter {self.__num} had idled on node {self.curPos().getNum()} for {self.__arrivalTime} time step(s)"
            self.__path.append(self.__destinationNode)
            self.newPos()
            self.reset()
            # self.FFSignal.emit("done", 0)
            return (True,text)
        if(self.__cumArrivalTime < timer):
            raise Exception("time didn't synchronized")
        return (False,"")

    def curPos(self) -> Node: #回傳現在位置
        return self.__path[-1]

    def getName(self) -> str: 
        return self.__name

    def next_Pos_Accessment(self, node: Node, timer) -> str: #判斷消防員是否可以指派去給定的目的地 
        if(self.__statusDetection(node) and self.__distanceDetection(node) and self.__safeDetection(node, timer)):
            return "vaild choose"
        elif (not self.__statusDetection(node)):
            return "Error(burned)"
        elif (not self.__distanceDetection(node)):
            return "Error(not neighbor)"
        elif (not self.__safeDetection(node, timer)):
            return "Error(will burned)"
        else:
            return ""

    def __safeDetection(self, node: Node, timer) -> bool:
        earliestTime = timer + math.ceil(self.curPos().getArc(node)["travel-time"][f"{self.__num}"])
        return True if node.getFireMinArrivalTime() >= earliestTime else False

    def processCheck(self, node: Node) -> str:
        from math import ceil
        self.selected()
        self.__destinationNode = node
        if(node != self.curPos()):
            self.__arrivalTime = self.curPos().getArc(self.__destinationNode)["travel-time"][f"{self.__num}"]
            return "Assign sucessful! : {} move to vertex {}".format(self.getName(), node.getNum())
        else:
            self.__arrivalTime = ceil(self.curPos().getProcessingTime() / self.rate_extinguish)
            return "Assign sucessful! : {} choose defend".format(self.getName()) if not self.curPos().isProtected() else "already protected"

    def __statusDetection(self, node) -> bool: #check assigned node's status (burned or not burned)
        return not node.isBurned()
    
    def __distanceDetection(self, node) -> bool: #check if assigned node is adjacent to selected FireFighter
        if(node == self.curPos()):
            return True
        return node in self.curPos().getNeighbors()

    def __calculateCurrentCapacity(self): #更新消防員在該node上的保護情況
        if(self.isProcess()):
            self.curPos().nextFFProgress(self.rate_extinguish)

    def __calculateCurrentFFArrive(self, arc): #更新消防員在arc上的移動情況
        if(self.__pathProgress < arc["travel-time"][f"{self.__num}"]):
            self.__pathProgress += 1
            
    def __wateringVisualize(self): #UI設定
        if(self.isProcess()):
            opacity = self.curPos().getNodePercentage_FF(self.rate_extinguish)
            opacity = 1 if opacity > 1 else opacity
            self.curPos().setStyle(f'background-color: rgba(0, 255, 0, {opacity}); color: white;')
            self.curPos().setStyleSheet(self.curPos().getStyle())
    
    def accessibleVisualize(self, timer,lst): #消防員可以前往的點可視化
        self.closeaccessibleVisualize(lst)
        self.arrowdirection = 1

        def arrowAnimation():
            current_pos = self.arrowLabel.pos()
            new_y = current_pos.y() + 2 * self.arrowdirection
            if new_y >= self.y()-100:
                self.arrowdirection = -1
            elif new_y <= self.y()-110:
                self.arrowdirection = 1
            self.arrowLabel.move(current_pos.x(), new_y)
        # self.arrowLabel = QLabel(self.parentWidget())
        if(self.__num == 1):
            arrow = QPixmap("image/arrow_redr.png")
        else:
            arrow = QPixmap("image/arrow.png")
        self.arrowLabel.setPixmap(arrow)
        self.arrowLabel.show()
        self.arrowLabel.lower()
        self.arrowLabel.setGeometry(self.x()-5,self.y()-110,50,70)
        self.timer_arrow = QTimer(self)
        self.timer_arrow.timeout.connect(arrowAnimation)
        self.timer_arrow.start(200)

        if(not self.isTraveling() or not self.isProcess()):
            accessibleNeighbors = [neighbor for neighbor in self.curPos().getNeighbors() if not neighbor.isBurned()]
            if(not accessibleNeighbors):
                self.FFSignal.emit("trapped", self.__num)
            for i in accessibleNeighbors:
                if (i.getFireMinArrivalTime() >= timer + math.ceil(self.curPos().getArc(i)["travel-time"][f"{self.__num}"])):
                    i.timer_nodeOpacity.start(100)                
            for i in (self.curPos().getNeighbors()):
                i.setFlat(False)

            if(not self.curPos().isProtected()):
                self.curPos().timer_nodeOpacity.start(100)

    def closeaccessibleVisualize(self, lst): #用於清除前一個消防員可以前往點的顏色
        self.arrowLabel.setText("")
        self.arrowLabel.setPixmap(QPixmap())
        self.arrowLabel.lower()
        self.timer_arrow.stop()

        for i in lst:
            if not i.isBurned:
                i.setFlat(False)
            i.setStyleSheet(i.getStyle())
            i.timer_nodeOpacity.stop()


    def getArcPercentage_FF(self, node): #獲得消防員在arc上的移動進度    
        for i in self.curPos().getArcs():
            if(i["nodeButton"] == node): 
                ratio = self.__pathProgress/i["travel-time"][f"{self.__num}"]
                return ratio if ratio <= 1 else 1 
        return 0

    def getStatus(self):
        return self.__status
