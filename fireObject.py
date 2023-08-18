from node import Node
from PyQt5.QtCore import pyqtSignal, QObject
import copy
class Fire(QObject):
    burnedSignal = pyqtSignal(int)
    #updateSignal = pyqtSignal()
    opacitySignal = pyqtSignal(float, int)
    def __init__(self, network, depot):
        super().__init__()
        #self.fireNetwork = network
        self.firePos = network.nodeList[depot-1]
        self.rate_fireburn = 10 #火燃燒速率
        self.move_fire=10 #火擴散速率
        self.finishBurn = False
        self.finishSpread = False
        self.arcs = []
        for i in self.firePos.getArcs():
            self.arcs.append({"node" : i["node"], "length": i["length"], "fire-travel": 0})
        self.arcCtr = 0

    def burn(self):
        self.firePos.onFire()
        self.burnedSignal.emit(self.firePos.getNum())

    def fire_spread(self, timer): #火焰傳遞邏輯
        if(self.finishSpread):
            return
        elif(self.finishBurn):
            for i in self.firePos.getArcs():
                for j in self.arcs:
                    if(i["node"]==j["node"]):
                        if(i["length"] > j["fire-travel"]):
                            self.__calculateCurrentFireArrive(j)
                        else:
                            if(self.__statusDetection(j)): #若該點未被保護或未燒起來, 起火
                                j["node"].onFire()
                                print("burnnnm")
                                self.arcCtr+=1
                                if(self.arcCtr == len(self.arcs)):
                                    self.finishSpread = True
                                    print("finish")
                                self.burnedSignal.emit(j["node"].getNum())
        else:
            self.__calculateCurrentCapacity(timer)
            self.__burningVisualize()

    def __statusDetection(self, node): #check assigned node's status
        return not (node["node"].isProtected() or node["node"].isBurned())

    def __calculateCurrentCapacity(self, timer): #更新該node的grass量
        remain = self.firePos.getGrassAmount() - self.rate_fireburn
        if(remain <= 0):
            self.finishBurn = True
        self.firePos.updateGrassAmount(remain)

    def __calculateCurrentFireArrive(self, arc): #更新火在arc上的移動情況
        arc["fire-travel"] += self.move_fire
    
    def minTimeFireArrival(self, time):
        self.__calculateMinTime(time)
        #self.updateSignal.emit()

    def __calculateMinTime(self, time):
        self.firePos.fireMinArrivalTime = time
        tempList = [copy.copy(self.firePos)]
        while(tempList):
            tempTime = tempList[0].fireMinArrivalTime
            tempTime += tempList[0].getGrassAmount() / self.rate_fireburn

            if(tempList[0] == self.firePos):
                for j in self.arcs:
                    if(j["node"].fireMinArrivalTime > tempTime + (j["length"] - j["fire-travel"]) / self.move_fire):
                        j["node"].fireMinArrivalTime = tempTime + (j["length"] - j["fire-travel"]) / self.move_fire
                        tempList.append(copy.copy(j["node"]))
            else:
                for j in tempList[0].getArcs():
                    if(j["node"].fireMinArrivalTime > tempTime + j["length"] / self.move_fire):                     
                        j["node"].fireMinArrivalTime = tempTime + (j["length"] - j["fire-travel"]) / self.move_fire
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