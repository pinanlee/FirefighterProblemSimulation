from node import Node
from PyQt5.QtCore import pyqtSignal, QObject
import math
import copy
class Fire(QObject):
    burnedSignal = pyqtSignal(int)
    opacitySignal = pyqtSignal(float, int)
    terminateSignal = pyqtSignal()
    def __init__(self, network, depot, time):
        super().__init__()
        self.firePos = network.nodeList[depot-1]
        self.startBurningTime = time
        self.rate_fireburn = 4 #火燃燒速率
        self.move_fire = 4 #火擴散速率
        self.finishBurn = False
        self.finishSpread = False
        self.arcs = []
        for i in self.firePos.getArcs():
            self.arcs.append({"node" : i["node"], "length": i["length"], "fire-travel": 0})

    def burn(self):
        self.firePos.onFire()
        self.burnedSignal.emit(self.firePos.getNum())

    def fire_spread(self, timer): #火焰傳遞邏輯
        if(self.finishSpread):
            return
        elif(self.finishBurn):
            ctr = 0
            for j in self.arcs:
                if(self.__statusDetection(j)): #若該點未被保護或未燒起來, 起火
                    if(j["length"] > j["fire-travel"]):
                        self.__calculateCurrentFireArrive(j)
                    else:
                        j["node"].onFire()
                        print("node {} is burned at time {}".format(j["node"].getNum(), timer))
                        self.burnedSignal.emit(j["node"].getNum())
                else:
                    ctr+=1

                if(ctr == len(self.arcs)):
                    self.finishSpread = True
        else:
            self.__calculateCurrentCapacity()
            self.__burningVisualize()

    def __statusDetection(self, node): #check assigned node's status
        return not (node["node"].isProtected() or node["node"].isBurned())

    def __calculateCurrentCapacity(self): #更新該node的grass量
        remain = self.firePos.getGrassAmount() - self.rate_fireburn
        if(remain <= 0):
            self.finishBurn = True
        self.firePos.updateGrassAmount(remain)

    def __calculateCurrentFireArrive(self, arc): #更新火在arc上的移動情況
        arc["fire-travel"] += self.move_fire
    
    def minTimeFireArrival(self, time):
        self.__calculateMinTime(time)

    def __calculateMinTime(self, time):
        self.firePos.fireMinArrivalTime = self.startBurningTime
        tempList = [copy.copy(self.firePos)]
        while(tempList):
            tempTime = tempList[0].fireMinArrivalTime
            tempTime += tempList[0].initialGrassAmount / self.rate_fireburn
            
            for j in tempList[0].getArcs():
                if(self.__statusDetection(j)):
                    if(j["node"].fireMinArrivalTime > math.ceil(tempTime + j["length"] / self.move_fire)):               
                        j["node"].fireMinArrivalTime = math.ceil(tempTime + j["length"] / self.move_fire)
                        tempList.append(copy.copy(j["node"]))             
            tempList.remove(tempList[0])
            for i in range(len(tempList)):
                for j in range(len(tempList)):
                    if(tempList[i].fireMinArrivalTime > tempList[j].fireMinArrivalTime):
                        temp = tempList[i]
                        tempList[i] = tempList[j]
                        tempList[j] = temp
                    

    def __burningVisualize(self): #UI設定
        opacity = 1 - self.firePos.getNodePercentage_Fire()
        self.opacitySignal.emit(opacity, self.firePos.no)

    def getArcPercentage_Fire(self, arc): #獲得火在arc上的移動進度
        if(arc in self.arcs):
                return arc["fire-travel"]/ arc["length"]
        return -1