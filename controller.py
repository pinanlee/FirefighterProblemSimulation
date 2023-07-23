#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import random

from example_ui import Ui_MainWindow
from FF import Node, FireFighter

#parameter settings
rate_extinguish = 2
rate_fireburn = 2
move_fire=2
move_man=1
#下午: 地點總量matrix(check->改初始設定就定義), 地點總量dynamic matrix,distance matrix, checkmove matrix, dynamic distance matrix for fire & man
#0722
initial_Capacity = [0]
dynamic_Capacity = [0]
dynamic_fireArriveCountdown = [[],
    [[2,20],[4,7],[5,8]],#1
    [[1,20],[3,10],[5,10],[6,10],[10,10]],#2
    [[2,10],[6,10],[7,10],[11,10]],#3
    [[1,7],[5,10],[8,10],[9,10]],#4
    [[1,8],[2,10],[4,10],[9,7],[10,10]],#5
    [[2,10],[3,10],[10,10],[11,10]],#6
    [[3,10],[11,10],[14,10]],#7
    [[4,10],[9,10],[12,10]],#8
    [[4,10],[5,7],[8,10],[10,10],[12,10],[13,10],[15,10]],#9
    [[2,10],[5,10],[6,10],[9,10],[13,10],[15,10]],#10
    [[3,10],[6,10],[7,10],[13,10],[14,10],[15,10]],#11
    [[8,10],[9,10],[13,10],[15,10]],#12
    [[9,10],[10,10],[11,10],[12,10],[14,10],[15,10]],#13
    [[7,10],[11,10],[13,10],[15,10]],#14
    [[6,10],[9,10],[10,10],[11,10],[12,10],[13,10],[14,10]],#15
]

#Data structure settings
nodeList = [] #store all existing Node except Depot (class: Node)
fireList = [] #store all Node affected by fire (class: Node)
firefighterList = [] #store all firefighter (class: FireFighter)
selectList =[] #store list[FireFighter, Node] to show user selects which FireFighter travels to which Node 
selectedFF=[] #store FireFighter selected by user (class: FireFighter)
maxfirefighter = 2
firefighterNum = 2
timer = 0

nodeUI = []

#firefighter arc distance (initial)
travel_time = [[],
    [[2,1],[4,1],[5,1]],#1
    [[1,1],[3,1],[5,1],[6,1],[10,1]],#2
    [[2,1],[6,1],[7,1],[11,1]],#3
    [[1,1],[5,1],[8,1],[9,1]],#4
    [[1,1],[2,1],[4,1],[9,1],[10,1]],#5
    [[2,1],[3,1],[10,1],[11,1]],#6
    [[3,1],[11,1],[14,1]],#7
    [[4,1],[9,1],[12,1]],#8
    [[4,1],[5,1],[8,1],[10,1],[12,1],[13,1],[15,1]],#9
    [[2,1],[5,1],[6,1],[9,1],[13,1],[15,1]],#10
    [[3,1],[6,1],[7,1],[13,1],[14,1],[15,1]],#11
    [[8,1],[9,1],[13,1],[15,1]],#12
    [[9,1],[10,1],[11,1],[12,1],[14,1],[15,1]],#13
    [[7,1],[11,1],[13,1],[15,1]],#14
    [[6,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1]],#15  
]
#fire arc distance (initial)
fire_spread_time = [[],
    [[2,10],[4,10],[5,10]],#1
    [[1,10],[3,10],[5,10],[6,10],[10,10]],#2
    [[2,10],[6,10],[7,10],[11,10]],#3
    [[1,10],[5,10],[8,10],[9,10]],#4
    [[1,10],[2,10],[4,10],[9,10],[10,10]],#5
    [[2,10],[3,10],[10,10],[11,10]],#6
    [[3,10],[11,10],[14,10]],#7
    [[4,10],[9,10],[12,10]],#8
    [[4,10],[5,10],[8,10],[10,10],[12,10],[13,10],[15,10]],#9
    [[2,10],[5,10],[6,10],[9,10],[13,10],[15,10]],#10
    [[3,10],[6,10],[7,10],[13,10],[14,10],[15,10]],#11
    [[8,10],[9,10],[13,10],[15,10]],#12
    [[9,10],[10,10],[11,10],[12,10],[14,10],[15,10]],#13
    [[7,10],[11,10],[13,10],[15,10]],#14
    [[6,10],[9,10],[10,10],[11,10],[12,10],[13,10],[14,10]],#15
]


#travel_time fire spread可以整合成distance matrix
#解決消防員各自node選擇問題
class MainWindow_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global nodeUI
        nodeUI = [[self.ui.pushButton, self.ui.image_1], [self.ui.pushButton_2, self.ui.image_2],
        [self.ui.pushButton_3, self.ui.image_3], [self.ui.pushButton_4, self.ui.image_4],
        [self.ui.pushButton_5, self.ui.image_5], [self.ui.pushButton_6, self.ui.image_6],
        [self.ui.pushButton_7, self.ui.image_7], [self.ui.pushButton_8, self.ui.image_8],
        [self.ui.pushButton_9, self.ui.image_9], [self.ui.pushButton_10, self.ui.image_10],
        [self.ui.pushButton_11, self.ui.image_11], [self.ui.pushButton_12, self.ui.image_12],
        [self.ui.pushButton_13, self.ui.image_13], [self.ui.pushButton_14, self.ui.image_14]]
        self.setup_control()

    def setup_control(self):
        # TODO
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        self.ui.label_3.setPixmap(QPixmap("network.png"))
        self.ui.label.setText("t= "+ str(timer))
        self.ui.label_2.setText("select 2 vertices and push \" t++\"")
        self.initNode()
        self.randomFireAndDepot()

    def initNode(self):
        ctr = 1
        for i in nodeUI:
            temp = random.randrange(5,11)
            nodeList.append(Node(i[0], i[1], ctr, self.choose, temp))
            ctr+=1
            initial_Capacity.append(temp)
            print("node ",nodeList[-1].getNum(),end="")
            print(nodeList[-1].getAmount())
        self.ui.pushButton_16.clicked.connect(self.nextTime)

    def randomFireAndDepot(self):
        #random fire depot
        a = random.sample(nodeList,1)
        a[0].onFire()
        fireList.append(a[0])
        #init depot
        depot = Node(self.ui.pushButton_15, self.ui.image_15, 15, self.choose, 0)
        depot.depotSetting()
        for i in range(firefighterNum):
            ff = FireFighter(i+1)
            ff.move(depot)
            firefighterList.append(ff)


    def choose(self):
        global selectList, firefighterNum, selectedFF, firefighterList

        #check if FireFighter is selected before choosing Node to travel
        if(not selectedFF):
            for i in firefighterList:
                if(i.curPos().has(self.sender()) and not i.isSelected()):
                    selectedFF.append(i)
                    i.curPos().mark("O")
                    i.selected()
                    return

        #check if selected FireFighter can move to assigned Node
        for i in nodeList:
            if(i.has(self.sender())):
                if(self.statusDetection(i) and self.distanceDetection(i)):
                    self.sender().setStyleSheet("background-color: grey")
                    selectList.append({"firefighter": selectedFF[0], "node": i})
                    selectedFF.clear()           

    #check assigned node's status (burned or not burned)
    def statusDetection(self, node):
        if(node.isBurned()):
            self.ui.label_2.setText("cannot choose this vertex: (burned)")
            return 0
        return 1
    
    #check if assigned node is adjacent to selected FireFighter
    def distanceDetection(self, node):
        for i in travel_time[selectedFF[0].curPos().getNum()]:
            if(node.getNum() == i[0]):
                return 1
        self.ui.label_2.setText("this vertex doesn't meet distance restrictions")      
        return 0

    def fire_spread(self):
        tempList=[]
        for i in fireList:
            for j in nodeList:
                for k in dynamic_fireArriveCountdown[i.getNum()]:
                    if(j.getNum() == k[0] and not j.isProtected() and i.getAmount()<=0 and not j.isBurned() and k[1] <= 0 ):
                        j.onFire()
                        tempList.append(j)
        if(not tempList):
            self.ui.label_2.setText("finished")
        for k in tempList:
            fireList.append(k)
        return 0

    def calculateCurrentCapacity(self,timer):
        dynamic_Capacity = []
        dynamic_Capacity.append(0)
        for i in range(len(nodeList)):
            if (nodeList[i].isProtected()):
                if(nodeList[i].getAmount() <= 0):
                    remain = 0
                else:
                    remain = nodeList[i].getAmount() - rate_extinguish
                    if (remain<0):
                        remain = 0
            elif(nodeList[i].isBurned()):
                if(nodeList[i].getAmount() <= 0):
                    remain = 0
                else:
                    remain = nodeList[i].getAmount() - rate_fireburn
                    if (remain<0):
                        remain = 0
            else:
                remain = nodeList[i].getAmount()
            nodeList[i].updateAmount(remain)
            dynamic_Capacity.append(remain)
            print("node: ",i+1,end="")
            print(" in time", timer,end="")
            print(": ",nodeList[i].getAmount())
    def calculateCurrentFireArrive(self):
        for i in fireList:
            for j in nodeList:
                for k in dynamic_fireArriveCountdown[i.getNum()]:
                    if (j.getNum() == k[0] and not j.isProtected() and i.getAmount() <= 0 ): #有連結且沒有消防員且本身燃燒完且沒有燃燒過(每個火容量不同要加上去不然出錯)
                        if(k[1]>0):
                            k[1] = k[1] - move_fire
                            print("this is node ", i.getNum(),end="")
                            print("-> ",j.getNum(),end="")
                            print(" countdown: ",k[1])
                        else:
                            k[1] = 0
    def fireDamageVisualize(self,button):
        #opacity = (initial_Capacity[i[0].property("no.")] - i[0].property("amount") / initial_Capacity[i[0].property("no.")])*255
            opacity = 0.2
            self.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')

    def nextTime(self):
        if(len(selectList) == firefighterNum):
            for i in selectList:
                i["node"].defend()
                i["firefighter"].move(i["node"])
            for i in range(firefighterNum):
                 selectList.pop()
            #self.fire_spread()     
        self.fire_spread()
        global timer
        timer+=1
        self.calculateCurrentCapacity(timer)
        self.calculateCurrentFireArrive()
        #self.fireDamageVisualize()
        self.ui.label.setText("t= "+str(timer))





