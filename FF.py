from PyQt5.QtGui import QPixmap, QCursor
from node import Node
from PyQt5.QtCore import QTimer, pyqtSignal, QRect, Qt
from PyQt5.QtWidgets import QLabel
import math

class FireFighter(QLabel):
    FFSignal = pyqtSignal(str, int)
    def __init__(self, widget, num, depot):
        super().__init__(widget)
        self.__widget = widget
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
        #self.__ready = False #是否已準備好
        self.rate_extinguish = 3#澆水速率
        self.move_man = 4 #移動速率
        self.__destNode = None #下一個目的
        self.__pathProgress = 0
        self.__status = "Not Ready"
        #UI設定
        self.setStyleSheet("border: none; background: transparent;")
        self.setPixmap(QPixmap("./image/firefighter.png"))
        self.pixmaploc = "./image/firefighter.png"
        self.curPos().defend()
        self.arrowLabel = QLabel(self.__widget)
        self.timer_arrow = QTimer(self)

    def getNum(self):
        return self.__num

    def newPos(self):
        self.setGeometry(QRect(self.curPos().x()+20, self.curPos().y(),self.curPos().width()+ 20, self.curPos().height()+20))

    def reset(self):
        self.__select = False 
        self.__travel = False 
        self.__process = False
        self.__destNode = None
        self.__arrivalTime = 0
        self.__pathProgress = 0

    def finishTimeSet(self, value):
        if(self.isIdle()):
            self.__arrivalTime = value
        self.__cumArrivalTime += self.__arrivalTime

    def destination(self):
        return self.__destNode

    def getcumArrivalTime(self):
        return self.__cumArrivalTime

    def move(self): #開始移動至目的地
        if(self.__destNode == self.curPos()):
            self.curPos().defend()
            self.process()
            self.FFSignal.emit("protect",self.curPos().getNum())
        if(self.__destNode != None):
            self.traveling()

    def process(self): #消防員標記為澆水中
        self.__process = True

    def isProcess(self): #回傳是否消防員在澆水
        return self.__process

    def isTraveling(self): #消防員標記為移動中
        return self.__travel

    def traveling(self): #回傳是否消防員在移動
        self.__travel = True

    def selected(self): #消防員標記為被指派
        self.__select = True

    '''def ready(self):
        self.__ready = True

    def cancelReady(self):
        self.__ready = False'''

    def isSelected(self): #回傳是否消防員被指派
        return self.__select
    
    def isIdle(self):
        return not (self.__select or self.__process or self.__travel or self.__destNode != None)

    # def isReady(self):
    #     return self.__ready

    def checkArrival(self, timer): #是否在timer時抵達目的地
        self.__destNode = self.curPos() if self.__destNode == None else self.__destNode
        if(self.__cumArrivalTime <= timer):
            self.__cumArrivalTime = timer
            self.__path.append(self.__destNode)
            self.newPos()
            self.reset()
            self.FFSignal.emit("done", 0)
            return True
        else:
            self.__calculateCurrentCapacity()
            self.__wateringVisualize()
            self.setGeometry(QRect(self.curPos().x() + int(self.getArcPercentage_FF(self.__destNode)*(self.__destNode.x() - self.curPos().x())), self.curPos().y() + int(self.getArcPercentage_FF(self.__destNode)*(self.__destNode.y() - self.curPos().y())),self.curPos().width()+ 20, self.curPos().height()+20))
            for i in self.curPos().getArcs(): #對於現在位置的相鄰點
                if(i["nodeButton"] == self.__destNode):
                    self.__calculateCurrentFFArrive(i)
        return False

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
        earliestTime = timer + math.ceil(self.curPos().getArc(node)["travel-time"])
        return True if node.getFireMinArrivalTime() >= earliestTime else False

    def processCheck(self, node: Node) -> str:
        self.selected()
        self.__destNode = node
        if(node != self.curPos()):
            self.__arrivalTime = self.curPos().getArc(self.__destNode)["travel-time"]
            return "{} move to vertex {}".format(self.getName(), node.getNum())
        else:
            self.__arrivalTime = self.curPos().getProcessingTime() / self.rate_extinguish
            return "{} choose defend".format(self.getName()) if not self.curPos().isProtected() else "already protected"

    def __statusDetection(self, node) -> bool: #check assigned node's status (burned or not burned)
        return not node.isBurned()
    
    def __distanceDetection(self, node) -> bool: #check if assigned node is adjacent to selected FireFighter
        if(node == self.curPos()):
            return True
        return node in self.curPos().getNeighbors()

    def __calculateCurrentCapacity(self): #更新消防員在該node上的保護情況
        if(self.isProcess()):
            self.curPos().nextFFProgress()

    def __calculateCurrentFFArrive(self, arc): #更新消防員在arc上的移動情況
        if(self.__pathProgress < arc["travel-time"]):
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
        self.arrowLabel = QLabel(self.__widget)
        if(self.__num == 1):
            arrow = QPixmap("image/arrow_redr.png")
        else:
            arrow = QPixmap("image/arrow.png")
        self.arrowLabel.setPixmap(arrow)
        self.arrowLabel.show()
        self.arrowLabel.setGeometry(self.x()-5,self.y()-110,50,70)
        self.timer_arrow = QTimer(self)
        self.timer_arrow.timeout.connect(arrowAnimation)
        self.timer_arrow.start(200)

        if(not self.isTraveling() or not self.isProcess()):
            for i in (self.curPos().getNeighbors()):
                i.setFlat(False)
                if (i.isBurned() == False and i.isProtected() == False):
                    if (i.getFireMinArrivalTime() >= timer + math.ceil(self.curPos().getArc(i)["travel-time"])):
                        i.timer_nodeOpacity.start(100)
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
                ratio = self.__pathProgress/i["travel-time"]
                return ratio if ratio <= 1 else 1 
        return 0

    def getStatus(self):
        return self.__status

    def updateStatus(self):
        # if(self.isReady()):
        #     self.__status = "Ready"
        if(self.isProcess()):
            self.__status = "Processing"
        elif(self.isTraveling()):
            self.__status = "Traveling"
        elif(self.isIdle()):
            self.__status = "Not Ready"
        elif(self.isSelected()):
            self.__status = "Assigned!"
        else:
            self.__status = "Not Ready"