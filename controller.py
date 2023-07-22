#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import random

from example_ui import Ui_MainWindow
from FF import FF

nodeList = []
fireList = []
firefighterList = []
selectList =[]
#FFpath=[]
maxfirefighter = 2
firefighterNum = 2
timer = 0

image_path = "firefighter.png"  # Replace with the actual path to your image

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

fire_spread_time = [[],
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
        nodeList.append(FF(self.ui.pushButton, self.ui.image_1))
        nodeList.append(FF(self.ui.pushButton_2, self.ui.image_2))
        nodeList.append(FF(self.ui.pushButton_3, self.ui.image_3))
        nodeList.append(FF(self.ui.pushButton_4, self.ui.image_4))
        nodeList.append(FF(self.ui.pushButton_5, self.ui.image_5))
        nodeList.append(FF(self.ui.pushButton_6, self.ui.image_6))
        nodeList.append(FF(self.ui.pushButton_7, self.ui.image_7))
        nodeList.append(FF(self.ui.pushButton_8, self.ui.image_8))
        nodeList.append(FF(self.ui.pushButton_9, self.ui.image_9))
        nodeList.append(FF(self.ui.pushButton_10, self.ui.image_10))
        nodeList.append(FF(self.ui.pushButton_11, self.ui.image_11))
        nodeList.append(FF(self.ui.pushButton_12, self.ui.image_12))
        nodeList.append(FF(self.ui.pushButton_13, self.ui.image_13))
        nodeList.append(FF(self.ui.pushButton_14, self.ui.image_14))
        nodeList.append(FF(self.ui.pushButton_15, self.ui.image_15))
        for i in range(len(nodeList)):
            nodeList[i].pushButton.clicked.connect(self.choose)
            nodeList[i].pushButton.setProperty("no.", i+1)
            nodeList[i].pushButton.setProperty("burned", 0)
            nodeList[i].pushButton.setProperty("protected", 0)
        self.ui.pushButton_16.clicked.connect(self.nextTime)

    def randomFireAndDepot(self):
        a = random.sample(nodeList,1)
        a[0].pushButton.setStyleSheet("background-color: red;")
        a[0].pushButton.setProperty("burned", 1)
        fireList.append(a[0].pushButton)
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
                    if(i.pushButton.property("no.") in travel_time[selectedFF[0].property("no.")] and i.pushButton.property("burned")==0):
                        i.pushButton.setStyleSheet("background-color: grey")
                    break

        for i in selectList:
            if(self.sender()==i):
                self.sender().setStyleSheet("background-color: white")
                selectList.remove(i)
                return
        if(self.statusDetection() and self.distanceDetection()):
            if(len(selectList)<firefighterNum):
                #self.ui.label_2.setText("select vertex " + str(self.sender().property("no.")))
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
                for k in fire_spread_time[i.property("no.")]:
                    if(j.pushButton.property("no.")==k[0] and j.pushButton.property("protected")==0):
                        j.pushButton.setProperty("burned",1)
                        j.pushButton.setStyleSheet("background-color: red")
                        tempList.append(j.pushButton)
        if(len(tempList)==0):
            self.ui.label_2.setText("finished")
        for k in tempList:
            fireList.append(k)
        return 0

    def nextTime(self):
        if(len(selectList) == firefighterNum and self.deploymentCheck()):
            for i in range(firefighterNum):
                firefighterList[i][1].setPixmap(QPixmap())
            firefighterList.clear()
            for i in selectList:
                i.setProperty("protected",1)
                i.setStyleSheet("background-color: green")
                for k in nodeList:
                    if(i==k.pushButton):
                        global image_path
                        pixmap = QPixmap(image_path)
                        k.label.setPixmap(pixmap)
                        firefighterList.append([i,k.label])
            for i in range(firefighterNum):
                 selectList.pop()
            self.fire_spread()
                #self.nextTime()
            selectCtr = 0        
        global timer
        timer+=1
        self.ui.label.setText("t= "+str(timer))





