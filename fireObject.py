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
        self.__finishSpread = False
        self.__arcs = []
        for i in self.__firePos.getArcs():
            self.__arcs.append({"node" : i["node"], "length": i["length"], "fire-travel": 0, "travel-time": i["travel-time"]})
    def getPos(self):
        return self.__firePos.getPos()
    def x(self):
        return self.__firePos.getPos().x()
    def y(self):
        return self.__firePos.getPos().y()
    def width(self):
        return self.__firePos.getPos().width()
    def height(self):
        return self.__firePos.getPos().height()

    def isComplete(self):
        return self.__finishSpread

    def burn(self):
        self.__firePos.onFire()
        self.fireSignal.emit("burn", 0, self.__firePos.getNum())

    def fire_spread(self): #火焰傳遞邏輯
        # if(self.__finishSpread):
        #     return
        if(self.__finishBurn):
            all_arc_burned = True
            for arc in self.__arcs:
                if(arc["travel-time"] > arc["fire-travel"]):    
                    self.__fireSpreadContinuation(arc)
                    if(self.__fireExpandDetection(arc)):
                        all_arc_burned = False
                else:
                    if(self.__fireExpandDetection(arc)):
                        arc["node"].onFire()
                        #print("node {} is burned at time {}".format(arc["node"].getNum(), timer))
                        self.fireSignal.emit("burn", 0, arc["node"].getNum())
            if(all_arc_burned):
                self.__finishSpread = True            
        else:
            self.__fireBurnContinuation()
            self.__burningVisualize()

    def __fireExpandDetection(self, arc): #check assigned node's status
        return not (arc["node"].isProtected() or arc["node"].isBurned())

    def __fireBurnContinuation(self): #更新該node的grass量
        self.__firePos.fireProgressing()
        self.__firePos.updateValue()
        self.__finishBurn = (self.__firePos.getFireProgress() == self.__firePos.getBurningTime())

    def __fireSpreadContinuation(self, arc): #更新火在arc上的移動情況
        arc["fire-travel"] += 1

    def minTimeFireArrival(self):
        self.__firePos.setFireMinArrivalTime(self.__startBurningTime)
        tempList = [self.__firePos]
        
        while(tempList):
            selectedNode = tempList.pop(0)
            tempTime = selectedNode.getFireMinArrivalTime() + selectedNode.getBurningTime()
            for arc in selectedNode.getArcs():
                if(self.__fireExpandDetection(arc) and self.__minTimeIsIteratable(arc, tempTime)):              
                    arc["node"].setFireMinArrivalTime(math.ceil(tempTime + arc["travel-time"]))
                    tempList.append(arc["node"])             
            tempList.sort(key= lambda node: node.getFireMinArrivalTime())

    def __minTimeIsIteratable(self, arc, time):
        return arc["node"].getFireMinArrivalTime() > math.ceil(time + arc["travel-time"])

    def __burningVisualize(self): #UI設定
        opacity = 1 - self.__firePos.getNodePercentage_Fire()
        self.fireSignal.emit("visual", opacity, self.__firePos.getNum())

    def getArcPercentage_Fire(self, arc): #獲得火在arc上的移動進度
        return arc["fire-travel"] / arc["travel-time"] if (arc in self.__arcs) else -1

    def getArcs(self):
        return self.__arcs