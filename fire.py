from node import Node
<<<<<<< HEAD
from PyQt5.QtCore import pyqtSignal, QObject
class Fire(QObject):
    burnedSignal = pyqtSignal(int)
    updateSignal = pyqtSignal()
    opacitySignal = pyqtSignal(float, int)
    def __init__(self, network, depot):
        super().__init__()
        self.fireList = [network.nodeList[depot-1]]
        self.burnedList = [] #已經擴散完成的node
        self.rate_fireburn = 10 #火燃燒速率
        self.move_fire=10 #火擴散速率

=======
import math



class Fire:
    def __init__(self, begin):
        self.fireList = [begin] #燃燒中的node

        self.burnedList = [] #已經擴散完成的node
        self.rate_fireburn = 2 #火燃燒速率
        self.move_fire=2 #火擴散速率

        self.fireList[0].onFire()
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

    def getBurningList(self):
        return self.burnedList

<<<<<<< HEAD
    def burn(self):
        self.fireList[0].onFire()
        self.burnedSignal.emit(self.fireList[0].no)

    def fire_spread(self, timer): #火焰傳遞邏輯
        tempList = [] #暫存新增的火點
        #print(self.fireList)
=======
    def fire_spread(self, timer): #火焰傳遞邏輯
        tempList = [] #暫存新增的火點
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
        for i in self.fireList: #對於每個火點
            ctr = 0
            for j in i.getArcs(): #對於每個火點的相鄰點
                if(i.arc_finish_spread(j)): #判斷火點是否完成移動
                    if(self.__statusDetection(j)): #若該點未被保護或未燒起來, 起火
                        j["node"].onFire()
<<<<<<< HEAD
                        print("node {} is burned at time {}".format(j["node"].getNum(), timer))
                        self.burnedSignal.emit(j["node"].getNum())
                        
=======
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
                        tempList.append(j["node"])
                    ctr+=1
                else: #還沒抵達，繼續移動
                    self.__calculateCurrentFireArrive(i, j)
<<<<<<< HEAD
                    #print("{}, {}: {}".format(i.getNum(),j["node"].getNum(),i.getArcPercentage_Fire(j["node"])))
=======
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
            self.__calculateCurrentCapacity(i, timer)
            if(ctr == len(i.getNeighbors())): #如果該火點的相鄰arc均已移動過，移除該火點
                self.burnedList.append(i)
                self.fireList.remove(i)
        self.__burningVisualize()
        if(tempList): #加入新增的火點
            for i in tempList:
                self.fireList.append(i)

    def __statusDetection(self, node): #check assigned node's status
        return not (node["node"].isProtected() or node["node"].isBurned())

    def __calculateCurrentCapacity(self, fireNode, timer): #更新該node的grass量
        remain = fireNode.getGrassAmount() - self.rate_fireburn
        fireNode.updateGrassAmount(remain)

    def __calculateCurrentFireArrive(self, fireNode, arc): #更新火在arc上的移動情況
        if(fireNode.getGrassAmount() <= 0 ):
            if(arc["fire-travel"] < arc["length"]):
                arc["fire-travel"] += self.move_fire
    
<<<<<<< HEAD
    def minTimeFireArrival(self, node):
=======
    def minTimeFireArrival(self, node: Node):
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
        if(node.isProtected() or node.isBurned()):
            return
        for i in self.fireList:
            self.__calculateMinTime(i, node, 0)
<<<<<<< HEAD
        self.updateSignal.emit()
    def __calculateMinTime(self, start, end, time):
        for arc in start.getArcs():
            if(arc["node"].isProtected() or arc["node"].isBurned()):
=======
        # print("node: ",node.getNum(),end="")
        # print(node.fireMinArrivalTime)
        

    def __calculateMinTime(self, start, end, time):
        for arc in start.getArcs():
            if(arc["node"].isProtected() or arc["node"].isBurned()):
                if (arc["node"].fireMinArrivalTime<=0):
                    return 0
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
                return
            temp = time + start.getGrassAmount() / self.rate_fireburn + (arc["length"] - arc["fire-travel"]) / self.move_fire
            if(arc["node"].fireMinArrivalTime > temp):
                arc["node"].fireMinArrivalTime = temp
                if(arc["node"] != end):
                    self.__calculateMinTime(arc["node"], end, temp)
        

    def __burningVisualize(self): #UI設定
        for i in self.fireList:
            if(i.isBurned()):
<<<<<<< HEAD
                opacity = 1 - i.getNodePercentage_Fire()
                self.opacitySignal.emit(opacity, i.no)
                #i.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
=======
                print(i.getGrassAmount())
                opacity = 1 - i.getNodePercentage_Fire()
                #print(opacity)
                i.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
                #nodeUI[i.getNum()-1].setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
