from node import Node
import math
'''
問題:
mintimearrival和calculatemintime未完成 
'''


class Fire:
    def __init__(self, begin):
        self.fireList = [begin] #燃燒中的node

        self.burnedList = [] #已經擴散完成的node
        self.rate_fireburn = 2 #火燃燒速率
        self.move_fire=2 #火擴散速率

        self.fireList[0].onFire()

    def getBurningList(self):
        return burnedList

    def fire_spread(self, timer): #火焰傳遞邏輯
        tempList = [] #暫存新增的火點
        for i in self.fireList: #對於每個火點
            ctr = 0
            for j in i.getArcs(): #對於每個火點的相鄰點
                if(i.arc_finish_spread(j)): #判斷火點是否完成移動
                    if(self.__statusDetection(j)): #若該點未被保護或未燒起來, 起火
                        j["node"].onFire()
                        tempList.append(j["node"])
                    ctr+=1
                else: #還沒抵達，繼續移動
                    self.__calculateCurrentCapacity(i, timer)
                    self.__calculateCurrentFireArrive(i, j)
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
    
    def minTimeFireArrival(self, node):
        global min_node
        minTimeFireArrival = 1000
        choice = []
        for i in self.fireList:
            choice.append(__calculateMinTime(i, node, 0))
            for j in i.adjArc:
                if(not j["node"] != node):
                    tempTimeFireArrival = math.ceil(j["length"]/self.move_fire) + math.ceil(i.getGrassAmount()/self.rate_fireburn )
                    
                    # print("dynamic_fireArriveCountdown correct",j[1] )
                    # print("fire travel time",math.ceil(j[1]/move_fire))
                    # print("fire burn time",math.ceil(i.getAmount()/rate_fireburn ))
                    # print("tempTimeFireArrival",tempTimeFireArrival)
                    if(tempTimeFireArrival <= minTimeFireArrival):
                        min_node = i #node
                        minTimeFireArrival = tempTimeFireArrival
                        # print("result",minTimeFireArrival)
        return minTimeFireArrival

    def __calculateMinTime(self, start, end, time):
        for i in start.adjArc:
            tempTimeFireArrival = time + math.ceil(i["length"]/self.move_fire) + math.ceil(start.getGrassAmount()/self.rate_fireburn)
            if(i["node"] != end):
                self.calculateMinTime(i["node"], end, time)
            else:
                return tempTimeFireArrival

    def __burningVisualize(self): #UI設定
        for i in self.fireList:
            if(i.isBurned()):
                print(i.getGrassAmount())
                opacity = 1 - i.getNodePercentage_Fire()
                print(opacity)
                i.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
                #nodeUI[i.getNum()-1].setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
    '''
    def simulationOver(self):#done yet
        burnedNode = 0
        burnedNodecheck = 0
        for i in fireList:
            for j in nodeList:
                if(j.onFire() == 1):
                    burnedNode = burnedNode+1
                for k in dynamic_fireArriveCountdown[i.getNum()]:
                    if (j.getNum() == k[0] and not j.isProtected() and i.getAmount() <= 0 and not j.isBurned() and k[1] <= 0):
                        #gameOvercheck[1] = 0
                        print("spread mother fucker")
                    else:
                        #gameOvercheck[1] = 1
                        print("no spread")

        # for i in gameOvercheck:
        #     if(gameOvercheck[1] == 1):
        #         burnedNodecheck = burnedNodecheck+1
        #
        # if(burnedNodecheck == burnedNode):
        #     print("game over")
    '''