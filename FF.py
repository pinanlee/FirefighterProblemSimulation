from PyQt5.QtGui import QPixmap
from node import Node

'''
calculateCurrentCapacity和wateringVisualize沒用到 (processing未實作完成)
'''

class FireFighter:
    def __init__(self, num, depot):
        self.__name = "firefighter " + str(num) #消防員編號
        self.__path = [depot] #紀錄FF經過的node
      
        #變數
        self.__arrivalTime = 0 #下一個arc所需移動時間
        self.__cumArrivalTime = 0 #消防員抵達目的預計時間
        self.__select = False #是否被指派
        self.__travel = False #是否在移動
        self.__process = False #是否在澆水
        self.rate_extinguish = 2 #澆水速率
        self.move_man = 1 #移動速率
        self.destNode = depot #下一個目的

        #UI設定
        self.pixmap = QPixmap("firefighter.png")
        self.curPos().defend()
        self.curPos().setImage(self.pixmap)  

    def reset(self):
        self.__select = False 
        self.__travel = False 
        self.__process = False
        self.destNode = None
        self.__arrivalTime = 0

    def move(self, timer): #開始移動至目的地
        self.__cumArrivalTime += self.__arrivalTime
        if(self.isProcess()):
            self.curPos().defend()
        self.checkArrival(timer)

    def idle(self, timer):
        self.__cumArrivalTime += 1
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
        if(self.__cumArrivalTime<=timer):
            self.__cumArrivalTime = timer
            self.destNode = self.curPos() if self.destNode == None else self.destNode
            self.curPos().setImage(QPixmap())
            prev = self.curPos()
            self.__path.append(self.destNode)
            if(prev != self.curPos()):
                self.curPos().setStyleSheet("")
            if(self.curPos().isDepot()):
                self.curPos().setStyleSheet("background-color: black;")
            self.curPos().setImage(self.pixmap)
            self.reset()
            return True
        else:
            self.__calculateCurrentCapacity()
            self.__wateringVisualize()
        return False

    def curPos(self) -> Node: #回傳現在位置
        return self.__path[-1]

    
    def next_Pos_Accessment(self, node): #判斷消防員是否可以指派去給定的目的地 
        if(self.__statusDetection(node) and self.__distanceDetection(node) and self.__safeDetection(node)):
            self.selected()
            node.preDefend()
            self.destNode = node
            self.__arrivalTime = self.curPos().getArc(node)["length"] / self.move_man
            return "vaild choose"
        elif (not self.__statusDetection(node)):
            return "cannot choose this vertex: (burned)"
        elif (not self.__distanceDetection(node)):
            return "this vertex doesn't meet distance restrictions"
        elif (not self.__safeDetection(node)):
            return "fire will arrive early"
        else:
            return ""
    def __safeDetection(self, node: Node):
        if(node.fireMinArrivalTime >= self.curPos().getArc(node)["length"] / self.move_man):
            return True
        return False

    def process_Accessment(self): #判斷消防員是否可以指派去給定的目的地 
        if(not self.curPos().isProtected()):
            self.selected()
            self.process()
            self.destNode = self.curPos()
            self.__arrivalTime = self.curPos().getWaterAmount() / self.rate_extinguish
            return "vaild choose!"
        elif(self.curPos().isProtected()):
            return "this vertex is already protected"
        else:
            return ""

    def __statusDetection(self, node): #check assigned node's status (burned or not burned)
        return not node.isBurned()
    
    def __distanceDetection(self, node): #check if assigned node is adjacent to selected FireFighter
        return node in self.curPos().getNeighbors()

    def __calculateCurrentCapacity(self): #更新消防員在該node上的保護情況
        if(self.isProcess()):
            remain = self.curPos().getWaterAmount() - self.rate_extinguish
            self.curPos().updateWaterAmount(remain)
            
        #print("node: ",i.getNum()+1,end="")
        #print(" at time", timer,end="")
        #print(": ",i.getAmount())

    def __wateringVisualize(self): #UI設定
        if(self.isProcess()):
            opacity = 1 - self.curPos().getNodePercentage_FF()
            print(opacity)
            self.curPos().setStyleSheet(f'background-color: rgba(0, 255, 0, {opacity}); color: white;')
    
