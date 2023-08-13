from PyQt5.QtGui import QPixmap
from node import Node
from PyQt5.QtCore import QTimer, pyqtSignal,QObject

class FireFighter(QObject):
    FFdoneSignal = pyqtSignal(str)
    FFprotectSignal = pyqtSignal(int)
    def __init__(self, num, depot):
        super().__init__()
        self.num = num
        self.__name = "firefighter " + str(num) #消防員編號
        self.__path = [depot] #紀錄FF經過的node
      
        #變數
        self.__arrivalTime = 0 #下一個arc所需移動時間
        self.__cumArrivalTime = 0 #消防員抵達目的預計時間
        self.__select = False #是否被指派
        self.__travel = False #是否在移動
        self.__process = False #是否在澆水
        self.rate_extinguish = 2 #澆水速率
        self.move_man = 10 #移動速率
        self.destNode = depot #下一個目的

        #UI設定
        self.pixmap = QPixmap("./image/firefighter.png")
        self.curPos().defend()
        self.curPos().setImage(self.pixmap)  

    def reset(self):
        self.__select = False 
        self.__travel = False 
        self.__process = False
        self.destNode.setText("")
        self.destNode = None
        self.__arrivalTime = 0


    def finishTimeSet(self):
        if(self.isIdle()):
            self.__arrivalTime = 1
        self.__cumArrivalTime += self.__arrivalTime


    def move(self, timer): #開始移動至目的地
        if(self.destNode == self.curPos()):
            self.curPos().defend()
            self.process()
            self.FFprotectSignal.emit(self.curPos().getNum())
        else:
            self.traveling()
        self.checkArrival(timer)

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

    def isSelected(self): #回傳是否消防員被指派
        return self.__select
    
    def isIdle(self):
        return not (self.__select or self.__process or self.__travel or self.destNode != None)

    def checkArrival(self, timer): #是否在timer時抵達目的地
        self.destNode = self.curPos() if self.destNode == None else self.destNode
        if(self.__cumArrivalTime <= timer):
            self.__cumArrivalTime = timer
            self.curPos().setImage(QPixmap())
            prev = self.curPos()
            self.__path.append(self.destNode)
            if(prev != self.curPos()):
                self.curPos().setStyleSheet("")
            if(self.curPos().isDepot()):
                self.curPos().setStyleSheet("background-color: black;")
            self.curPos().setImage(self.pixmap)
            self.reset()
            self.FFdoneSignal.emit("done")
            return True
        else:
            self.__calculateCurrentCapacity()
            self.__wateringVisualize()
            for i in self.curPos().nodeController.getArcs(): #對於現在位置的相鄰點
                if(i["node"] == self.destNode.nodeController):
                    self.__calculateCurrentFFArrive(i)
        return False

    def curPos(self) -> Node: #回傳現在位置
        return self.__path[-1]

    def getName(self):
        return self.__name

    def next_Pos_Accessment(self, node: Node): #判斷消防員是否可以指派去給定的目的地 
        if(self.__statusDetection(node) and self.__distanceDetection(node) and self.__safeDetection(node)):
            return "vaild choose"
        elif (not self.__statusDetection(node)):
            return "Error(burned)"
        elif (not self.__distanceDetection(node)):
            return "Error(not neighbor)"
        elif (not self.__safeDetection(node)):
            return "Error(will burned)"
        else:
            return ""

    def __safeDetection(self, node: Node):
        if(node.getFireMinArrivalTime() >= self.curPos().getArc(node)["length"] / self.move_man):
            return True
        return False

    def processCheck(self, node: Node):
        self.selected()
        node.preDefend()
        self.destNode = node
        if(node != self.curPos()):
            self.__arrivalTime = self.curPos().getArc(node)["length"] / self.move_man 
            return "{} move to vertex {}".format(self.getName(), node.getNum())
        else:
            self.__arrivalTime = self.curPos().getWaterAmount() / self.rate_extinguish
            return "{} choose defend".format(self.getName()) if not self.curPos().isProtected() else "already protected"

    def __statusDetection(self, node): #check assigned node's status (burned or not burned)
        return not node.isBurned()
    
    def __distanceDetection(self, node): #check if assigned node is adjacent to selected FireFighter
        if(node == self.curPos()):
            return True
        return node in self.curPos().getNeighbors()

    def __calculateCurrentCapacity(self): #更新消防員在該node上的保護情況
        if(self.isProcess()):
            remain = self.curPos().getWaterAmount() - self.rate_extinguish
            self.curPos().updateWaterAmount(remain)

    def __calculateCurrentFFArrive(self, arc): #更新消防員在arc上的移動情況
        if(arc["FF-travel"] < arc["length"]):
            arc["FF-travel"] += self.move_man

    def __wateringVisualize(self): #UI設定
        if(self.isProcess()):
            opacity = 1 - self.curPos().getNodePercentage_FF()
            self.curPos().setStyleSheet(f'background-color: rgba(0, 255, 0, {opacity}); color: white;')
    
    def accessibleVisualize(self,nodelist): #消防員可以前往的點可視化
        for i in nodelist[:14]:
            if(not i.isBurned() and not i.isProtected()):
                i.setStyleSheet("")

        for i in (self.curPos().getNeighbors()):
            if (i.isBurned() == False and i.isProtected() == False):
                if (i.getFireMinArrivalTime() >= self.curPos().getArc(i)["length"] / self.move_man):
                    i.setStyleSheet(f'background-color: rgba(0, 255, 255, {0.3}); color: white;')

    def closeaccessibleVisualize(self): #用於清除前一個消防員可以前往點的顏色
        for i in (self.curPos().getNeighbors()):
            if (i.isBurned() == False and i.isProtected() == False):
                if (i.getFireMinArrivalTime() >= self.curPos().getArc(i)["length"] / self.move_man):
                    i.setStyleSheet("")