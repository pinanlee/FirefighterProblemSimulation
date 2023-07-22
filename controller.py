#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import random

from example_ui import Ui_MainWindow

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
nodeList = []
fireList = []
firefighterList = []
selectList =[]
#FFpath=[]
maxfirefighter = 2
firefighterNum = 2
timer = 0
image_path = "firefighter.png"  # Replace with the actual path to your image
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
        nodeList.append([self.ui.pushButton, self.ui.image_1])
        nodeList.append([self.ui.pushButton_2, self.ui.image_2])
        nodeList.append([self.ui.pushButton_3, self.ui.image_3])
        nodeList.append([self.ui.pushButton_4, self.ui.image_4])
        nodeList.append([self.ui.pushButton_5, self.ui.image_5])
        nodeList.append([self.ui.pushButton_6, self.ui.image_6])
        nodeList.append([self.ui.pushButton_7, self.ui.image_7])
        nodeList.append([self.ui.pushButton_8, self.ui.image_8])
        nodeList.append([self.ui.pushButton_9, self.ui.image_9])
        nodeList.append([self.ui.pushButton_10, self.ui.image_10])
        nodeList.append([self.ui.pushButton_11, self.ui.image_11])
        nodeList.append([self.ui.pushButton_12, self.ui.image_12])
        nodeList.append([self.ui.pushButton_13, self.ui.image_13])
        #nodeList.append([self.ui.pushButton_14, self.ui.image_14])
        nodeList.append([self.ui.pushButton_15, self.ui.image_15])
        for i in range(len(nodeList)):
            nodeList[i][0].clicked.connect(self.choose)
            nodeList[i][0].setProperty("no.", i+1)
            nodeList[i][0].setProperty("burned", 0)
            nodeList[i][0].setProperty("protected", 0)
            temp = random.randrange(5,11)
            nodeList[i][0].setProperty("amount", temp )
            initial_Capacity.append(temp)
            print("node ",i+1,end="")
            print(nodeList[i][0].property("initial amount"))

        self.ui.pushButton_16.clicked.connect(self.nextTime)
    def randomFireAndDepot(self):
        a = random.sample(nodeList,1)
        a[0][0].setStyleSheet("background-color: red;")
        a[0][0].setProperty("burned", 1)
        fireList.append(a[0][0])
        self.ui.pushButton_14.setStyleSheet("background-color: black;")
        self.ui.pushButton_14.setProperty("protected", 1)
        self.ui.pushButton_14.setProperty("depot", 1)
        for i in range(firefighterNum):
            firefighterList.append([self.ui.pushButton_14,self.ui.image_14])
        self.ui.pushButton_14.clicked.connect(self.choose)
        self.ui.pushButton_14.setProperty("no.", 15)
        self.ui.pushButton_14.setProperty("burned", 0)
        global image_path
        pixmap = QPixmap(image_path)
        self.ui.image_14.setPixmap(pixmap)
    def choose(self):
        global selectList, firefighterNum, selectedFF,firefighterList
        #print(self.sender())
        for j in firefighterList:
            if(self.sender().property("no.") == j[0].property("no.")):
                selectedFF.append(self.sender())
                for i in nodeList:
                    if(i[0].property("no.") in travel_time[selectedFF[0].property("no.")] and i[0].property("burned")==0 ):
                        i[0].setStyleSheet("background-color: blue")
                        #不知道幹嘛用的
                    break
        for i in selectList:
            if(self.sender()==i):
                self.sender().setStyleSheet("background-color: white")
                selectList.remove(i)
                return
        if(self.statusDetection() and self.distanceDetection()):
            if(len(selectList)<firefighterNum):
                self.ui.label_2.setText("select vertex " + str(self.sender().property("no.")))
                self.sender().setStyleSheet("background-color: grey")
                selectList.append(self.sender())
    def statusDetection(self):
        if(self.sender().property("burned")==1):
            self.ui.label_2.setText("cannot choose this vertex: (burned)")
            return 0
        elif(self.sender().property("depot")==1):
            self.ui.label_2.setText("this vertex is depot")
            return 0
        else:
            return 1
    def distanceDetection(self):
        tempList=[]
        for i in firefighterList:
            for k in travel_time[i[0].property("no.")]:
                if(self.sender().property("no.")== k[0]):
                    return 1
        self.ui.label_2.setText("this vertex doesn't meet distance restrictions")
        return 0
    def deploymentCheck(self):
        for i in firefighterList:
            ctr=0
            for j in selectList:
                for k in travel_time[i[0].property("no.")]:
                    if(k[0]==j.property("no.")):
                        ctr+=1
            if(ctr==0):
                self.ui.label_2.setText("selection of vertex error, please try again")
                for k in selectList:
                    k.setStyleSheet("background-color: white")
                for l in range(firefighterNum):
                    selectList.pop()
                return 0
        return 1
    def fire_spread(self):
        tempList=[]
        for i in fireList:
            for j in nodeList:
                for k in dynamic_fireArriveCountdown[i.property("no.")]:
                    if(j[0].property("no.")==k[0] and j[0].property("protected")==0 and i.property("amount")<=0 and j[0].property("burned")==0 and k[1] <= 0 ):
                        j[0].setProperty("burned",1)
                        j[0].setStyleSheet("background-color: red")
                        tempList.append(j[0])
        if(len(tempList)==0):
            self.ui.label_2.setText("finished")
        for k in tempList:
            fireList.append(k)
        return 0
    def calculateCurrentCapacity(self,timer):
        dynamic_Capacity = []
        dynamic_Capacity.append(0)
        for i in range(len(nodeList)):
            if (nodeList[i][0].property("protected") == 1 ):
                if(nodeList[i][0].property("amount") <= 0):
                    remain = 0
                else:
                    remain = nodeList[i][0].property("amount") - rate_extinguish
                    if (remain<0):
                        remain = 0
            elif(nodeList[i][0].property("burned") == 1):
                if(nodeList[i][0].property("amount") <= 0):
                    remain = 0
                else:
                    remain = nodeList[i][0].property("amount") - rate_fireburn
                    if (remain<0):
                        remain = 0
            else:
                remain = nodeList[i][0].property("amount")
            nodeList[i][0].setProperty("amount", remain)
            dynamic_Capacity.append(remain)
            print("node: ",i+1,end="")
            print(" in time", timer,end="")
            print(": ",nodeList[i][0].property("amount"))
    def calculateCurrentFireArrive(self):
        for i in fireList:
            for j in nodeList:
                for k in dynamic_fireArriveCountdown[i.property("no.")]:
                    if (j[0].property("no.") == k[0] and j[0].property("protected") == 0 and i.property(
                            "amount") <= 0 ): #有連結且沒有消防員且本身燃燒完且沒有燃燒過(每個火容量不同要加上去不然出錯)
                        if(k[1]>0):
                            k[1] = k[1] - move_fire
                            print("this is node ", i.property("no."),end="")
                            print("-> ",j[0].property("no."),end="")
                            print(" countdown: ",k[1])
                        else:
                            k[1] = 0
    def fireDamageVisualize(self,button):
        #opacity = (initial_Capacity[i[0].property("no.")] - i[0].property("amount") / initial_Capacity[i[0].property("no.")])*255
            opacity = 0.2
            self.setStyleSheet(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')

    def nextTime(self):
        self.fire_spread()
        if(len(selectList) == firefighterNum and self.deploymentCheck()):
            for i in range(firefighterNum):
                firefighterList[i][1].setPixmap(QPixmap())
            firefighterList.clear()
            for i in selectList:
                i.setProperty("protected",1)
                i.setStyleSheet("background-color: green")
                for k in nodeList:
                    if(i==k[0]):
                        global image_path
                        pixmap = QPixmap(image_path)
                        k[1].setPixmap(pixmap)
                        firefighterList.append([i,k[1]])
            for i in range(firefighterNum):
                 selectList.pop()
            #self.fire_spread()
                #self.nextTime()
            selectCtr = 0
        global timer
        timer+=1
        self.calculateCurrentCapacity(timer)
        self.calculateCurrentFireArrive()
        #self.fireDamageVisualize()
        self.ui.label.setText("t= "+str(timer))







