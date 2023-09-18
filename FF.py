from PyQt5.QtGui import QPixmap
from node import Node
<<<<<<< HEAD
from PyQt5.QtCore import QTimer, pyqtSignal, QRect
from PyQt5.QtWidgets import QLabel
import math

class FireFighter(QLabel):
    FFdoneSignal = pyqtSignal(str)
    FFprotectSignal = pyqtSignal(int)
    FFidleSignal = pyqtSignal(int)
    def __init__(self, widget, num, depot):
        super().__init__(widget)
        self.num = num
        self.__name = "firefighter " + str(num) #消防員編號
        self.__path = [depot] #紀錄FF經過的node
        self.newPos()
=======
from PyQt5.QtCore import QTimer, pyqtSignal,QObject
'''
calculateCurrentCapacity和wateringVisualize沒用到 (processing未實作完成)
'''

class FireFighter(QObject):
    doneSignal = pyqtSignal(str)
    def __init__(self, num, depot):
        super().__init__()
        self.num = num
        self.__name = "firefighter " + str(num) #消防員編號
        self.__path = [depot] #紀錄FF經過的node
      
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
        #變數
        self.__arrivalTime = 0 #下一個arc所需移動時間
        self.__cumArrivalTime = 0 #消防員抵達目的預計時間
        self.__select = False #是否被指派
        self.__travel = False #是否在移動
        self.__process = False #是否在澆水
        self.rate_extinguish = 2 #澆水速率
<<<<<<< HEAD
        self.move_man = 20 #移動速率
        self.destNode = depot #下一個目的
        self.curMovingArc : dict = None
        self.pathProgress = 0
        self.idleLock = False
        #UI設定
        self.setPixmap(QPixmap("./image/firefighter.png"))
        self.pixmaploc = "./image/firefighter.png"
        self.curPos().defend()

    def newPos(self):
        self.setGeometry(QRect(self.curPos().x()+20, self.curPos().y(),self.curPos().width()+ 20, self.curPos().height()+20))
=======
        self.move_man = 1 #移動速率
        self.destNode = depot #下一個目的

        #UI設定
        self.pixmap = QPixmap("./image/firefighter.png")
        self.curPos().defend()
        self.curPos().setImage(self.pixmap)  
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

    def reset(self):
        self.__select = False 
        self.__travel = False 
        self.__process = False
<<<<<<< HEAD
        self.destNode = None
        self.__arrivalTime = 0
        self.curMovingArc = None
        self.pathProgress = 0

    def lock(self):
        self.idleLock = not self.idleLock
=======
        self.destNode.setText("")
        self.destNode = None
        self.__arrivalTime = 0

>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

    def finishTimeSet(self):
        if(self.isIdle()):
            self.__arrivalTime = 1
<<<<<<< HEAD
            self.FFidleSignal.emit(self.curPos().getNum())
        self.__cumArrivalTime += self.__arrivalTime

    def getcumArrivalTime(self):
        return self.__cumArrivalTime

    def move(self, timer): #開始移動至目的地
        if(self.destNode == self.curPos()):
            self.curPos().defend()
            self.process()
            self.curPos().nodeController.burned = False
            self.FFprotectSignal.emit(self.curPos().getNum())
        elif(self.destNode != None):
            self.traveling()
        #self.checkArrival(timer)
=======
        self.__cumArrivalTime += self.__arrivalTime


    def move(self, timer): #開始移動至目的地
        #self.__cumArrivalTime += self.__arrivalTime
        if(self.destNode == self.curPos()):
            self.curPos().defend()
            self.process()
        else:
            self.traveling()
            for i in self.curPos().getArcs(): #對於現在位置的相鄰點
                if(i["node"] == self.destNode):
                    self.__calculateCurrentFFArrive(i)

        self.checkArrival(timer)

    def idle(self, timer):
        self.__cumArrivalTime += 1
        self.checkArrival(timer)
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

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
<<<<<<< HEAD
        self.destNode = self.curPos() if self.destNode == None else self.destNode
        if(self.idleLock):
            return False
        if(self.__cumArrivalTime <= timer):
            self.__cumArrivalTime = timer
=======
        if(self.__cumArrivalTime<=timer):
            self.__cumArrivalTime = timer
            self.destNode = self.curPos() if self.destNode == None else self.destNode
            self.curPos().setImage(QPixmap())
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
            prev = self.curPos()
            self.__path.append(self.destNode)
            if(prev != self.curPos()):
                self.curPos().setStyleSheet("")
            if(self.curPos().isDepot()):
<<<<<<< HEAD
                self.curPos().style = "background-color: black;"
                self.curPos().setStyleSheet(self.curPos().style)
            self.newPos()
            self.reset()
            self.FFdoneSignal.emit("done")
=======
                self.curPos().setStyleSheet("background-color: black;")
            self.curPos().setImage(self.pixmap)
            self.reset()
            self.doneSignal.emit("done")
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
            return True
        else:
            self.__calculateCurrentCapacity()
            self.__wateringVisualize()
<<<<<<< HEAD
            self.setGeometry(QRect(self.curPos().x() + int(self.getArcPercentage_FF(self.destNode)*(self.destNode.x() - self.curPos().x())), self.curPos().y() + int(self.getArcPercentage_FF(self.destNode)*(self.destNode.y() - self.curPos().y())),self.curPos().width()+ 20, self.curPos().height()+20))
            for i in self.curPos().nodeController.getArcs(): #對於現在位置的相鄰點
                if(i["node"] == self.destNode.nodeController):
                    self.__calculateCurrentFFArrive(i)
=======
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
        return False

    def curPos(self) -> Node: #回傳現在位置
        return self.__path[-1]

    def getName(self):
        return self.__name

<<<<<<< HEAD
    def next_Pos_Accessment(self, node: Node, timer): #判斷消防員是否可以指派去給定的目的地 
        if(self.__statusDetection(node) and self.__distanceDetection(node) and self.__safeDetection(node, timer)):
=======
    def getFFnum(self):
        return self.num


    def next_Pos_Accessment(self, node): #判斷消防員是否可以指派去給定的目的地 
        
        if(self.__statusDetection(node) and self.__distanceDetection(node) and self.__safeDetection(node)):
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
            return "vaild choose"
        elif (not self.__statusDetection(node)):
            return "Error(burned)"
        elif (not self.__distanceDetection(node)):
            return "Error(not neighbor)"
<<<<<<< HEAD
        elif (not self.__safeDetection(node, timer)):
=======
        elif (not self.__safeDetection(node)):
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
            return "Error(will burned)"
        else:
            return ""

<<<<<<< HEAD
    def __safeDetection(self, node: Node, timer):
        if(node.getFireMinArrivalTime() >= timer + math.ceil(self.curPos().getArc(node)["length"] / self.move_man)):
            return True
        return False

    def processCheck(self, node: Node):
        self.selected()
        node.preDefend()
        self.destNode = node
        if(node != self.curPos()):
            self.curMovingArc = self.curPos().getArc(node)
            self.__arrivalTime = math.ceil(self.curPos().getArc(node)["length"] / self.move_man) 
            return "{} move to vertex {}".format(self.getName(), node.getNum())
        else:
            self.__arrivalTime = self.curPos().getWaterAmount() / self.rate_extinguish
            return "{} choose defend".format(self.getName()) if not self.curPos().isProtected() else "already protected"
=======
    def processAccept(self, node, text):
        if(text == "vaild choose"):
            self.selected()
            node.preDefend()
            self.destNode = node
            self.__arrivalTime = self.curPos().getArc(node)["length"] / self.move_man

    def __safeDetection(self, node: Node):
        if(node.fireMinArrivalTime >= self.curPos().getArc(node)["length"] / self.move_man):
            return True
        return False

    def process_Accessment(self): #判斷消防員是否可以指派去給定的目的地 
        if(not self.curPos().isProtected()):
            self.selected()
            #self.process()
            self.curPos().preDefend()
            self.destNode = self.curPos()
            self.__arrivalTime = self.curPos().getWaterAmount() / self.rate_extinguish
            return "vaild choose!"
        elif(self.curPos().isProtected()):
            return "already protected"
        else:
            return ""
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

    def __statusDetection(self, node): #check assigned node's status (burned or not burned)
        return not node.isBurned()
    
    def __distanceDetection(self, node): #check if assigned node is adjacent to selected FireFighter
<<<<<<< HEAD
        if(node == self.curPos()):
            return True
=======
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
        return node in self.curPos().getNeighbors()

    def __calculateCurrentCapacity(self): #更新消防員在該node上的保護情況
        if(self.isProcess()):
            remain = self.curPos().getWaterAmount() - self.rate_extinguish
            self.curPos().updateWaterAmount(remain)

    def __calculateCurrentFFArrive(self, arc): #更新消防員在arc上的移動情況
<<<<<<< HEAD
        if(self.pathProgress < arc["length"]):
            self.pathProgress += self.move_man
=======
        if(arc["FF-travel"] < arc["length"]):
            arc["FF-travel"] += self.move_man

>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

    def __wateringVisualize(self): #UI設定
        if(self.isProcess()):
            opacity = 1 - self.curPos().getNodePercentage_FF()
<<<<<<< HEAD
            self.curPos().nodeController.style = f'background-color: rgba(0, 255, 0, {opacity}); color: white;'
            self.curPos().setStyleSheet(self.curPos().nodeController.style)
    
    def accessibleVisualize(self, timer): #消防員可以前往的點可視化
        '''for i in self.curPos().getNeighbors():
            if(not i.isBurned() and not i.isProtected()):
                i.setStyleSheet("")'''
        if(not self.isTraveling() or not self.isProcess()):
            for i in (self.curPos().getNeighbors()):
                if (i.isBurned() == False and i.isProtected() == False):
                    if (i.getFireMinArrivalTime() >= timer + math.ceil(self.curPos().getArc(i)["length"] / self.move_man)):
                        i.setStyleSheet(f'background-color: rgba(0, 255, 255, {0.3}); color: white;')
            if(not self.curPos().isProtected()):
                self.curPos().setStyleSheet(f'background-color: rgba(0, 255, 255, {0.3}); color: white;')

    def closeaccessibleVisualize(self, lst): #用於清除前一個消防員可以前往點的顏色
        '''for i in (self.curPos().getNeighbors()):
            if (i.isBurned() == False and i.isProtected() == False):
                if (i.getFireMinArrivalTime() >= self.curPos().getArc(i)["length"] / self.move_man):
                    i.setStyleSheet("")'''
        for i in lst:
            i.setStyleSheet(i.nodeController.style)

    def getArcPercentage_FF(self, node): #獲得消防員在arc上的移動進度
        for i in self.curPos().getArcs():
            if(i["node"] == node.nodeController): 
                ratio = self.pathProgress/i["length"]
                return ratio if ratio <= 1 else 1 
        return 0
=======
            self.curPos().setStyleSheet(f'background-color: rgba(0, 255, 0, {opacity}); color: white;')
    
    def accessibleVisualize(self,nodelist): #消防員可以前往的點可視化
        for i in nodelist:
            if(not i.isBurned() and not i.isProtected()):
                i.setStyleSheet("")

        for i in (self.curPos().getNeighbors()):
            if (i.isBurned() == False and i.isProtected() == False):
                if (i.fireMinArrivalTime >= self.curPos().getArc(i)["length"] / self.move_man):
                    i.setStyleSheet(f'background-color: rgba(0, 255, 255, {0.3}); color: white;')

    def closeaccessibleVisualize(self): #用於清除可以前往點的顏色
        for i in (self.curPos().getNeighbors()):
            if (i.isBurned() == False and i.isProtected() == False):
                if (i.fireMinArrivalTime >= self.curPos().getArc(i)["length"] / self.move_man):
                    i.setStyleSheet("")
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
