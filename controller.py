#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QMainWindow, QApplication
import random
import math

from example_ui import Ui_MainWindow
from FF import FireFighter
from node import Node 
from fire import Fire
from InformationWindow import InformationWindow
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
labelList = [] #store all existing Label (class: Node)
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
        self.ui.timeButton.clicked.connect(self.showInformationWindow)



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
        depot.depotSetting()
        for i in range(firefighterNum):
            ff = FireFighter(i+1, depot)
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

    def selectFireFighter(self): #選擇消防員
        global FFindex
        FFindex = (FFindex + 1) % firefighterNum
        former_FFindex = (FFindex - 1) % firefighterNum

        self.ui.FFlabel.setText("selected FireFighter: {}".format(FFindex+1))

        #Flash effect
        for i in nodeList:
            i.stopFlashing()
        firefighterList[former_FFindex].curPos().stopFlashing()
        firefighterList[FFindex].curPos().startFlashing()
        print(FFindex + 1," Flash!!")
        print(former_FFindex + 1," Stop!!")

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
        return 0

    def nextTime(self): #跳轉至下一個時間點
        global timer
        for i in firefighterList:
            i.move(timer) 
        spreading = True
        while(spreading):
            fire.fire_spread(timer)
            timer+=1
            for i in firefighterList:
                if(i.checkArrival(timer)):
                    spreading =  False
        self.ui.timeIndexLabel.setText("t= "+str(timer))

    def showInformationWindow(self):
        self.nw = InformationWindow()
        temp = self.nw.updateOutputMatrix(nodeList)
        temp2 =self.nw.setSetupMatrix(nodeList,firefighterNum,firefighterList[FFindex].rate_extinguish,firefighterList[FFindex].move_man,fire.rate_fireburn,fire.move_fire)
        self.nw.inputmatrix = temp
        self.nw.setupmatrix = temp2
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        self.nw.ui()
        self.nw.show()










