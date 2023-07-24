#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QMainWindow, QApplication
import random

from example_ui import Ui_MainWindow
from FF import Node, FireFighter

#parameter settings
maxfirefighter = 2
firefighterNum = 2
rate_extinguish = 2
rate_fireburn = 2
move_fire=2
move_man=1
timer = 0
FFindex = 0


#Data structure settings
nodeList = [] #store all existing Node except Depot (class: Node)
fireList = [] #store all Node affected by fire (class: Node)
firefighterList = [] #store all firefighter (class: FireFighter)
selectList =[] #store list[FireFighter, Node] to show user selects which FireFighter travels to which Node 
selectedFF=[] #store FireFighter selected by user (class: FireFighter)
initial_Capacity = [0]
dynamic_Capacity = [0]
nodeUI = []
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
travel_time = [[[0,0]],
    [[1,1],[2,1],[4,1],[5,1]],#1
    [[1,1],[2,1],[3,1],[5,1],[6,1],[10,1]],#2
    [[2,1],[3,1],[6,1],[7,1],[11,1]],#3
    [[1,1],[4,1],[5,1],[8,1],[9,1]],#4
    [[1,1],[2,1],[4,1],[5,1],[9,1],[10,1]],#5
    [[2,1],[3,1],[6,1],[10,1],[11,1]],#6
    [[3,1],[7,1],[11,1],[14,1]],#7
    [[4,1],[8,1],[9,1],[12,1]],#8
    [[4,1],[5,1],[8,1],[9,1],[10,1],[12,1],[13,1],[15,1]],#9
    [[2,1],[5,1],[6,1],[9,1],[10,1],[13,1],[15,1]],#10
    [[3,1],[6,1],[7,1],[11,1],[13,1],[14,1],[15,1]],#11
    [[8,1],[9,1],[12,1],[13,1],[15,1]],#12
    [[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1]],#13
    [[7,1],[11,1],[13,1],[14,1],[15,1]],#14
    [[6,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1]],#15  
]
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
gameOvercheck = [[],
    [[2,0],[4,0],[5,0]],#1
    [[1,0],[3,0],[5,0],[6,0],[10,0]],#2
    [[2,0],[6,0],[7,0],[11,0]],#3
    [[1,0],[5,0],[8,0],[9,0]],#4
    [[1,0],[2,0],[4,0],[9,0],[10,0]],#5
    [[2,0],[3,0],[10,0],[11,0]],#6
    [[3,0],[11,0],[14,0]],#7
    [[4,0],[9,0],[12,0]],#8
    [[4,0],[5,0],[8,0],[10,0],[12,0],[13,0],[15,0]],#9
    [[2,0],[5,0],[6,0],[9,0],[13,0],[15,0]],#10
    [[3,0],[6,0],[7,0],[13,0],[14,0],[15,0]],#11
    [[8,0],[9,0],[13,0],[15,0]],#12
    [[9,0],[10,0],[11,0],[12,0],[14,0],[15,0]],#13
    [[7,0],[11,0],[13,0],[15,0]],#14
    [[6,0],[9,0],[10,0],[11,0],[12,0],[13,0],[14,0]],#15
]


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
        self.setWindowTitle("Firefighter Problem Simulation")
        self.ui.label_3.setPixmap(QPixmap("network.png"))
        self.ui.label.setText("t= "+ str(timer))
        self.ui.label_2.setText("select 2 vertices and push \" t++\"")
        self.initNode()
        self.randomFireAndDepot()

        self.ui.moveFF.clicked.connect(self.selectFireFighter)
        self.ui.moveButton.clicked.connect(self.choose)

        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText('Information Window')
        self.btn.setStyleSheet('font-size:16px;')
        self.btn.setGeometry(20,680,200,40)
        self.btn.clicked.connect(self.showInformationWindow)

    def initNode(self):
        ctr = 1
        for i in nodeUI:
            temp = random.randrange(5,11)
            nodeList.append(Node(i[0], i[1], ctr, self.viewProperty, temp))
            ctr+=1
            initial_Capacity.append(temp)
            print("node ",nodeList[-1].getNum(),end="")
            print(" amount ",nodeList[-1].getAmount())
        self.ui.pushButton_16.clicked.connect(self.nextTime)
        for i in travel_time:
            for j in i:
                j[1]=random.randrange(2,4)

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
            ff.move(depot, 0, timer)
            firefighterList.append(ff)

    def viewProperty(self):
        global selectedNode
        text=""
        for i in nodeList:
            if(i.has(self.sender())):
                selectedNode = i
                text += "node: {}\nprocessing time: {}\narc length: ".format(i.getNum(), i.getProcessingTime())
                for j in travel_time[firefighterList[FFindex].curPos().getNum()]:
                    if(j[0] == i.getNum()):
                        text += str(j[1])
        self.ui.label_4.setText(text)
    
    def selectFireFighter(self):
        global FFindex
        FFindex += 1
        if (FFindex == len(firefighterList)):
            FFindex = 0
        self.ui.label_5.setText("selected FireFighter: {}".format(FFindex+1))


    def choose(self):
        global selectList, firefighterNum, selectedFF, firefighterList
        selectedFF.append(firefighterList[FFindex])
        print("Firefighter : ",[selectedFF, selectedNode.getNum()])

        #check if selected FireFighter can move to assigned Node
        for i in nodeList:
            print(i==selectedNode)
            if(i==selectedNode):
                dd = self.distanceDetection(i)
                print("distanceDetection Verify" + str(dd[1]))
                if(self.statusDetection(i) and dd[0]):
                    selectedNode.preDefend()
                    selectList.append({"firefighter": selectedFF[0], "node": i, "distance": dd[1]})
                    selectedFF.clear()   
    '''def choose(self):
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
                dd = self.distanceDetection(i)
                print("dd" + str(dd[1]))
                if(self.statusDetection(i) and dd[0]):
                    self.sender().setStyleSheet("background-color: grey")
                    selectList.append({"firefighter": selectedFF[0], "node": i, "distance": dd[1]})
                    selectedFF.clear()   '''        

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
                return [1, i[1]]
        self.ui.label_2.setText("this vertex doesn't meet distance restrictions")      
        return [0, 0]

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
            print(" at time", timer,end="")
            print(": ",nodeList[i].getAmount())
    def calculateCurrentFireArrive(self):
        for i in fireList:
            for j in nodeList:
                for k in dynamic_fireArriveCountdown[i.getNum()]:
                    if (j.getNum() == k[0] and not j.isProtected() and i.getAmount() <= 0 ): #有連結且沒有消防員且本身燃燒完且沒有燃燒過(每個火容量不同要加上去不然出錯)
                        if(k[1]>0):
                            k[1] = k[1] - move_fire
                            print("node ", i.getNum(),end="")
                            print(" -> ",j.getNum(),end="")
                            print(" remain time : ",k[1])
                        else:
                            k[1] = 0
    def burningVisualize(self):
        for i in nodeList:
            if(i.isBurned()):
                opacity = ((initial_Capacity[i.getNum()] - i.getAmount() ) / initial_Capacity[i.getNum()] )*255
                nodeUI[i.getNum()-1][0].setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
            elif(i.isProtected()):
                opacity = ((initial_Capacity[i.getNum()] - i.getAmount()) / initial_Capacity[i.getNum()]) * 255
                nodeUI[i.getNum() - 1][0].setStyleSheet(f'background-color: rgba(0, 255, 0, {opacity}); color: white;')

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
    def nextTime(self):
        global timer
        for i in selectList:
            #i["node"].preDefend()
            i["firefighter"].move(i["node"], i["distance"],timer)
        selectList.clear()
        #self.fire_spread()     
        spreading = True
        while(spreading):
            self.fire_spread()
            timer+=1
            for i in firefighterList:
                if(i.checkArrival(timer)):
                    spreading =  False
        self.calculateCurrentCapacity(timer)
        self.calculateCurrentFireArrive()
        self.burningVisualize()
        #self.simulationOver()
        self.ui.label.setText("t= "+str(timer))

    def showInformationWindow(self):
        self.nw = InformationWindow()
        self.nw.show()
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x+100, y+100)



class InformationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Information Window')

        matrix = [
            [1, 2, 3],
            [2, 5, 6],
            [3, 8, 9],
            [4, 0, 0],
            [5, 0, 0],
            [6, 0, 0],
            [7, 0, 0],
            [8, 0, 0],
            [9, 0, 0],
            [10, 0, 0],
            [11, 0, 0],
            [12, 0, 0],
            [13, 0, 0],
            [14, 0, 0],
        ]


        self.matrix = matrix

        self.ui()

    def ui(self):
        table_widget = QTableWidget()
        table_widget.setRowCount(len(self.matrix))
        table_widget.setColumnCount(len(self.matrix[0]))
        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget.setItem(i, j, item)

        title_name=["Status","Amount","Remain"]  # 這裡可以更換您想要的標題名稱
        table_widget.setHorizontalHeaderLabels(title_name)

        self.setCentralWidget(table_widget)
        self.resize(400, 800)

