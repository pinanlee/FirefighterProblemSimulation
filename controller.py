#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QGraphicsOpacityEffect
import random
import math

from example_ui import Ui_MainWindow
from FF import FireFighter
from node import Node 
from fire import Fire

'''
choose function需要再改
trydefend function實作 (processing)
information table跑不出來 
可以試試自訂網路(?)
'''


#parameter settings
firefighterNum = 2
timer = 0
FFindex = 0


#Data structure settings
nodeList = [] #store all existing Node except Depot (class: Node)
#fireList = [] #store all Node affected by fire (class: Node)
firefighterList = [] #store all firefighter (class: FireFighter)
#initial_Capacity = [0]
#dynamic_Capacity = [0]
fire = None
selectedNode = None
nodeUI = []
travel_time = [[],
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



class MainWindow_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global nodeUI
        nodeUI = [self.ui.nodeButton_1, self.ui.nodeButton_2, self.ui.nodeButton_3, 
        self.ui.nodeButton_4, self.ui.nodeButton_5, self.ui.nodeButton_6, 
        self.ui.nodeButton_7, self.ui.nodeButton_8, self.ui.nodeButton_9, 
        self.ui.nodeButton_10, self.ui.nodeButton_11, self.ui.nodeButton_12, 
        self.ui.nodeButton_13, self.ui.nodeButton_14, self.ui.nodeButton_15 ]
        self.setup_control()

    def setup_control(self):
        # init UI
        self.initUIFunction()

        # init network
        self.initNode()
        self.randomFireAndDepot()
        self.NodeConnection()
        #self.showAllRoute()

    def initUIFunction(self):
        self.setWindowTitle("Firefighter Problem Simulation")
        self.ui.descriptionLabel.setText("select 2 vertices and push \" t++\"")
        self.ui.moveFF.clicked.connect(self.selectFireFighter)
        self.ui.moveButton.clicked.connect(self.choose)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText('Information Window')
        self.btn.setStyleSheet('font-size:16px;')
        self.btn.setGeometry(20,680,200,40)
        self.btn.clicked.connect(self.showInformationWindow)
        self.ui.processButton.clicked.connect(self.tryDefend)

    def initNode(self):
        for i in nodeUI:
            temp = random.randrange(5,11)
            i.clicked.connect(self.viewProperty)
            #i.updateAmount(temp)
            nodeList.append(i)
            #initial_Capacity.append(temp)
            #print("node ",nodeList[-1].getNum(),end="")
            #print(" amount ",nodeList[-1].getAmount())
        self.ui.timeButton.clicked.connect(self.nextTime)
        '''for i in travel_time:
            for j in i:
                j[1]=random.randrange(2,4)'''

    def randomFireAndDepot(self):
        #random fire depot
        a = random.randint(0,13)
        global fire
        fire = Fire(nodeList[a])
        #for i in nodeList:
        #    print("{}: {}".format(i.getNum(), i.isBurned()))
        #fireList.append(a[0])
        #init depot
        depot = self.ui.nodeButton_15
        for i in range(firefighterNum):
            ff = FireFighter(i+1, depot)
            depot.depotSetting()
            firefighterList.append(ff)

    def NodeConnection(self):
        for i in nodeList:
            for j in travel_time[i.getNum()]:           
                i.connectNode(nodeList[j[0]-1], j[1])

    def viewProperty(self): #查看node資訊
        global selectedNode
        selectedNode = self.sender()
        text = "node: {}\nwater needed: {}\narc length: ".format(selectedNode.getNum(), selectedNode.getWaterAmount())
        for j in firefighterList[FFindex].curPos().getNeighbors():
            if(j == selectedNode):
                text += str(firefighterList[FFindex].curPos().getArc(j)["length"])
        self.ui.node_info_label.setText(text)

    def showAllRoute(self):
        for i in (firefighterList[FFindex].curPos().getNeighbors()):
            if (not i.isBurned()):
                i.preDefend()

    def selectFireFighter(self): #選擇消防員
        global FFindex
        FFindex = (FFindex + 1) % firefighterNum
        self.ui.FFlabel.setText("selected FireFighter: {}".format(FFindex+1))
        self.opacitySet()
    
    def opacitySet(self):
        for i in firefighterList:
            i.curPos().setOpacity(0.3)
        firefighterList[FFindex].curPos().setOpacity(1)

    def choose(self): #指派消防員移動至給定node
        global selectedNode
        if(selectedNode == None):
            self.ui.descriptionLabel.setText("you haven't select node")
            return
        temp_currentnode = firefighterList[FFindex].curPos().getWaterAmount()
        if(not firefighterList[FFindex].isProcess()):
            ff_to_selectednode = math.ceil(temp_currentnode/ firefighterList[FFindex].rate_extinguish) +  math.ceil(firefighterList[FFindex].curPos().getArc(selectedNode)["length"] / firefighterList[FFindex].move_man)
            #fire_to_selectednode = fire.minTimeFireArrival(selectedNode)
            print(ff_to_selectednode)
            #print(fire_to_selectednode)
            #if(fire_to_selectednode >= ff_to_selectednode):
            if(True):
                if(not firefighterList[FFindex].isSelected()):
                    print("Firefighter : ",[firefighterList[FFindex], selectedNode.getNum()])
                    #check if selected FireFighter can move to assigned Node
                    print("distanceDetection Verify" + str(firefighterList[FFindex].curPos().getArc(selectedNode)))
                    text = firefighterList[FFindex].next_Pos_Accessment(selectedNode)
                    self.ui.descriptionLabel.setText(text)
                    selectedNode = None
                else:
                    self.ui.descriptionLabel.setText("this firefighter is moving")
            else:
                self.ui.descriptionLabel.setText("Fire will arrive early")
        else:
            self.ui.descriptionLabel.setText("this firefighter is processing") 

    def tryDefend(self): #指派消防員在原地澆水
        if(not firefighterList[FFindex].isSelected()):
            text = firefighterList[FFindex].process_Accessment()
            self.ui.descriptionLabel.setText(text)


    def nextTime(self): #跳轉至下一個時間點
        global timer
        for i in firefighterList:
            if(i.isIdle()):
                i.idle(timer)
            i.move(timer) 
        spreading = True
        while(spreading):
            fire.fire_spread(timer)
            timer+=1
            for i in firefighterList:
                if(i.checkArrival(timer)):
                    spreading =  False
        self.opacitySet()
        self.ui.timeIndexLabel.setText("t= "+str(timer))

    def showInformationWindow(self):
        self.nw = InformationWindow()
        temp = self.calculateMatrix()
        self.nw.matrix = temp
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        # self.nw.move(x + 100, y + 100)
        self.nw.show()
        self.nw.ui()


    def calculateMatrix(self):
        temp = []
        for i in range(0, 15):
            temp.append(["", "", ""])

        for i in nodeList:
            matrix[i.getNum()-1][0] = i.isProtected()
            matrix[i.getNum()-1][1] = i.isBurned()
            matrix[i.getNum()-1][2] = i.getGrassAmount()
            temp[i.getNum()-1][1] = i.getGrassAmount()
            if(matrix[i.getNum()-1][0] == 1):
                temp[i.getNum() - 1][1] = i.initialGrassAmount - i.getGrassAmount()
                temp_percent = round((i.initialGrassAmount - i.getGrassAmount() )/ i.initialGrassAmount ,4)
                temp[i.getNum() - 1][2] = str(temp_percent*100) + "%"
            elif(matrix[i.getNum()-1][1] == 1):
                temp[i.getNum() - 1][1] = i.getGrassAmount()
                temp_percent = round((i.initialGrassAmount  - i.getGrassAmount()) / i.initialGrassAmount ,4)
                temp[i.getNum() - 1][2] = str(temp_percent*100) + "%"
            elif (matrix[i.getNum()-1][1] == 0 and matrix[i.getNum()-1][0] == 0):
                temp[i.getNum() - 1][2] = "0 %"

        for i in nodeList:
            if (matrix[i.getNum()-1][0] == 1 and matrix[i.getNum()-1][2] <= 0  ):
                temp[i.getNum() - 1][0] = "Save Success"
            elif (matrix[i.getNum()-1][0] == 1 and matrix[i.getNum()-1][2] < i.initialGrassAmount ):
                temp[i.getNum() - 1][0] = "Protecting..."
            elif(matrix[i.getNum()-1][1] == 1 and matrix[i.getNum()-1][2] <= 0):
                temp[i.getNum() - 1][0] = "Damage"
            elif (matrix[i.getNum()-1][1] == 1 and matrix[i.getNum()-1][2] < i.initialGrassAmount ):
                temp[i.getNum() - 1][0] = "Burning..."
            elif (matrix[i.getNum()-1][1] == 0 and matrix[i.getNum()-1][0] == 0):
                temp[i.getNum() - 1][0] = "Normal"
        return temp


class InformationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Information Window')
        global matrix
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
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
                if (value == "Burning..."):
                    item.setBackground(QColor(255, 192, 203))
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                elif (value == "Protecting..."):
                    item.setBackground(QColor("lightgreen"))
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                elif (value == "Save Success"):
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("darkgreen"))
                    item.setForeground(QColor("white"))
                elif (value == "Damage"):
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("darkred"))
                    item.setForeground(QColor("white"))

                table_widget.setItem(i, j, item)

        title_name=["Status","Amount","Burned/Recovery Percentage"]  # 這裡可以更換您想要的標題名稱
        table_widget.setHorizontalHeaderLabels(title_name)

        self.setCentralWidget(table_widget)
        self.resize(400, 800)
