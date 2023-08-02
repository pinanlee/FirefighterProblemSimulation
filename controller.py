#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
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

timer = 0
FFindex = 0
labelList = []

#Data structure settings
nodeList = [] #store all existing Node except Depot (class: Node)
firefighterList = [] #store all firefighter (class: FireFighter)
fire = None
selectedNode = None
FFNum = 2
travel_time = [[],
    [[2,20],[4,7],[5,8]],#1
    [[1,20],[3,5],[5,17],[6,21],[10,30]],#2
    [[2,5],[6,25],[7,9],[11,10]],#3
    [[1,7],[5,10],[8,10],[9,10]],#4
    [[1,8],[2,17],[4,10],[9,7],[10,10]],#5
    [[2,21],[3,25],[10,19],[11,27]],#6
    [[3,9],[11,10],[14,3]],#7
    [[4,10],[9,13],[12,10]],#8
    [[4,10],[5,7],[8,13],[10,16],[12,14],[13,29],[15,6]],#9
    [[2,30],[5,10],[6,19],[9,16],[13,12],[15,10]],#10
    [[3,10],[6,27],[7,10],[13,6],[14,10],[15,10]],#11
    [[8,10],[9,14],[13,10],[15,10]],#12
    [[9,29],[10,12],[11,6],[12,10],[14,22],[15,10]],#13
    [[7,3],[11,10],[13,22],[15,10]],#14
    [[6,10],[9,6],[10,10],[11,10],[12,10],[13,10],[14,10]],#15
]


class MainWindow_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.nodeUI = [self.ui.nodeButton_1, self.ui.nodeButton_2, self.ui.nodeButton_3, 
        self.ui.nodeButton_4, self.ui.nodeButton_5, self.ui.nodeButton_6, 
        self.ui.nodeButton_7, self.ui.nodeButton_8, self.ui.nodeButton_9, 
        self.ui.nodeButton_10, self.ui.nodeButton_11, self.ui.nodeButton_12, 
        self.ui.nodeButton_13, self.ui.nodeButton_14, self.ui.nodeButton_15 ]
        global FFNum

        self.firefighterNum = FFNum
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
        for i in self.nodeUI:
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
        #init depot
        depot = self.ui.nodeButton_15
        for i in range(self.firefighterNum):
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
        #former_FFindex = FFindex 
        FFindex = (FFindex + 1) % self.firefighterNum
        
        self.ui.FFlabel.setText("selected FireFighter: {}".format(FFindex+1))
        self.__opacitySet()
        global selectedNode
        selectedNode = None

        #Flash effect
        '''for i in nodeList:
            i.stopFlashing()
        firefighterList[former_FFindex].curPos().stopFlashing()
        firefighterList[FFindex].curPos().startFlashing()
        print(FFindex + 1," Flash!!")
        print(former_FFindex + 1," Stop!!")'''
    
    def __opacitySet(self):
        for i in firefighterList:
            i.curPos().setOpacity(0.3)
        firefighterList[FFindex].curPos().setOpacity(1)


    def printStatus(func):
        print(func)
        def aa(self):
            text = func(self)
            #self.choose()
            self.ui.descriptionLabel.setText(text)
            print("hi")
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        '''global selectedNode
        if(selectedNode == None):
            self.ui.descriptionLabel.setText("you haven't select node")
            return
        if(not firefighterList[FFindex].isProcess()):
            fire.minTimeFireArrival(selectedNode)
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
            self.ui.descriptionLabel.setText("this firefighter is processing")'''
        global selectedNode
        if(selectedNode == None):
            return "you haven't select node"
            
        if(not firefighterList[FFindex].isProcess()):
            fire.minTimeFireArrival(selectedNode)
            if(not firefighterList[FFindex].isSelected()):
                print("Firefighter : ",[firefighterList[FFindex], selectedNode.getNum()])
                #check if selected FireFighter can move to assigned Node
                print("distanceDetection Verify" + str(firefighterList[FFindex].curPos().getArc(selectedNode)))
                text = firefighterList[FFindex].next_Pos_Accessment(selectedNode)
                return text
            else:
                return "this firefighter is moving"
        else:
            return "this firefighter is processing"
    def moveVertify(self):
        global selectedNode
        if(selectedNode == None):
            return "you haven't select node"
            
        if(not firefighterList[FFindex].isProcess()):
            fire.minTimeFireArrival(selectedNode)
            if(not firefighterList[FFindex].isSelected()):
                print("Firefighter : ",[firefighterList[FFindex], selectedNode.getNum()])
                #check if selected FireFighter can move to assigned Node
                print("distanceDetection Verify" + str(firefighterList[FFindex].curPos().getArc(selectedNode)))
                text = firefighterList[FFindex].next_Pos_Accessment(selectedNode)
                return text
            else:
                return "this firefighter is moving"
        else:
            return "this firefighter is processing"

    def tryDefend(self): #指派消防員在原地澆水
        if(not firefighterList[FFindex].isSelected()):
            text = firefighterList[FFindex].process_Accessment()
            self.ui.descriptionLabel.setText(text)


    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():
            text = "moving"
            global timer
            timer+=1
            fire.fire_spread(timer)
            for i in firefighterList:
                if(i.checkArrival(timer)):
                    time.stop()
            self.__opacitySet()
            self.ui.timeIndexLabel.setText("t= "+str(timer))
            self.ui.descriptionLabel.setText("moving.")
        global timer
        for i in firefighterList:
            if(i.isIdle()):
                i.idle(timer)
            i.move(timer) 
        time = QTimer()
        time.setInterval(500)
        time.timeout.connect(timeSkip)
        time.start()




    def showInformationWindow(self):
        self.nw = InformationWindow()
        temp = self.nw.updateOutputMatrix(nodeList)
        temp2 =self.nw.setSetupMatrix(nodeList,self.firefighterNum,firefighterList[FFindex].rate_extinguish,firefighterList[FFindex].move_man,fire.rate_fireburn,fire.move_fire)
        self.nw.inputmatrix = temp
        self.nw.setupmatrix = temp2
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        self.nw.ui()
        self.nw.show()


