from node import Node
from PyQt5.QtCore import pyqtSignal, QObject
import math
from nodeButtonController import NodeController
class Fire(QObject):
    fireSignal = pyqtSignal(str, float, int)
    def __init__(self, network, depot, time):
        super().__init__()
        self.__firePos : NodeController = network.nodeList[depot-1]
        self.__startBurningTime = time
        self.__finishBurn = False
        self.finishSpread = False
        self.pos = self.__firePos.pos
        self.arcs = []
        for i in self.__firePos.getArcs():
            self.arcs.append({"node" : i["node"], "length": i["length"], "fire-travel": 0, "travel-time": i["travel-time"]})

    def burn(self):
        self.__firePos.onFire()
        self.fireSignal.emit("burn", 0, self.__firePos.getNum())

    def fire_spread(self, timer): #火焰傳遞邏輯
        if(self.finishSpread):
            return
        if(self.__finishBurn):
            all_arc_burned = True
            for j in self.arcs:
                if(j["travel-time"] > j["fire-travel"]):    
                    self.__calculateCurrentFireArrive(j)
                    if(self.__statusDetection(j)):
                        all_arc_burned = False
                else:
                    if(self.__statusDetection(j)):
                        j["node"].onFire()
                        print("node {} is burned at time {}".format(j["node"].getNum(), timer))
                        self.fireSignal.emit("burn", 0, j["node"].getNum())
            if(all_arc_burned):
                self.finishSpread = True            
        else:
            self.__calculateCurrentCapacity()
            self.__burningVisualize()

    def __statusDetection(self, node): #check assigned node's status
        return not (node["node"].isProtected() or node["node"].isBurned())

    def __calculateCurrentCapacity(self): #更新該node的grass量
        self.__firePos.updateValue()
        self.__firePos.fireProgress += 1
        self.__finishBurn = (self.__firePos.fireProgress == self.__firePos.burningTime)

    def __calculateCurrentFireArrive(self, arc): #更新火在arc上的移動情況
        arc["fire-travel"] += 1

    def minTimeFireArrival(self):
        self.__firePos.fireMinArrivalTime = self.__startBurningTime
        tempList = [self.__firePos]
        
        while(tempList):
            tempTime = tempList[0].fireMinArrivalTime + tempList[0].burningTime
            for j in tempList[0].getArcs():
                if(self.__statusDetection(j) and j["node"].fireMinArrivalTime > math.ceil(tempTime + j["travel-time"])):              
                    j["node"].fireMinArrivalTime = math.ceil(tempTime + j["travel-time"])
                    #print("node {} turn to: {}".format(j["node"].getNum(),j["node"].fireMinArrivalTime))
                    tempList.append(j["node"])             
            tempList.remove(tempList[0])
            tempList.sort(key= lambda x: x.fireMinArrivalTime)

    def __burningVisualize(self): #UI設定
        opacity = 1 - self.__firePos.getNodePercentage_Fire()
        self.fireSignal.emit("visual", opacity, self.__firePos.getNum())

    def getArcPercentage_Fire(self, arc): #獲得火在arc上的移動進度
        return arc["fire-travel"]/ arc["travel-time"] if (arc in self.arcs) else -1
