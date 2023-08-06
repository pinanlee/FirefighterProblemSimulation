#!/usr/bin/env python
# coding: utf-8
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5 import QtWidgets, QtCore, QtGui
import random
import math
from UIv2_ui import Ui_MainWindow
#from example_ui import Ui_MainWindow
from FF import FireFighter
from node import Node 
from fire import Fire
from InformationWindow import InformationWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
'''
information table跑不出來 
可以試試自訂網路(?)
取消選取功能
提示視窗有誤
'''

#Data structure settings

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
    fire : Fire = None
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 2
    selectedStyle : str = "border: 2px solid blue;"
    FFindex = 0    
    focusIndex = 14
    labels : QtWidgets.QLabel = []
    timer = QTimer()
    currentTime = 0
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        self.ui.image_1 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_1.setGeometry(QtCore.QRect(230, 0, 101, 101))
        node1Pos = QtCore.QRect(310, 20, 61, 51)
        self.ui.nodeButton_1 = Node(self.ui.centralwidget, self.ui.image_1, 1, node1Pos)

        self.ui.image_2 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_2.setGeometry(QtCore.QRect(560, 0, 101, 101))
        node2Pos = QtCore.QRect(630, 40, 61, 51)
        self.ui.nodeButton_2 = Node(self.ui.centralwidget, self.ui.image_2, 2, node2Pos)

        self.ui.image_3 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_3.setGeometry(QtCore.QRect(810, 20, 101, 101))
        node3Pos = QtCore.QRect(870, 50, 61, 51)
        self.ui.nodeButton_3 = Node(self.ui.centralwidget, self.ui.image_3, 3, node3Pos)

        self.ui.image_4 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_4.setGeometry(QtCore.QRect(40, 110, 101, 101))
        node4Pos = QtCore.QRect(100, 130, 61, 61)
        self.ui.nodeButton_4 = Node(self.ui.centralwidget, self.ui.image_4, 4, node4Pos)

        self.ui.image_5 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_5.setGeometry(QtCore.QRect(450, 100, 101, 101))
        node5Pos = QtCore.QRect(430, 140, 61, 51)
        self.ui.nodeButton_5 = Node(self.ui.centralwidget, self.ui.image_5, 5, node5Pos)

        self.ui.image_6 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_6.setGeometry(QtCore.QRect(650, 160, 101, 101))
        node6Pos = QtCore.QRect(710, 190, 61, 51)
        self.ui.nodeButton_6 = Node(self.ui.centralwidget, self.ui.image_6, 6, node6Pos)

        self.ui.image_7 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_7.setGeometry(QtCore.QRect(910, 170, 101, 101))
        node7Pos = QtCore.QRect(980, 190, 61, 51)
        self.ui.nodeButton_7 = Node(self.ui.centralwidget, self.ui.image_7, 7, node7Pos)

        self.ui.image_8 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_8.setGeometry(QtCore.QRect(40, 300, 101, 101))
        node8Pos = QtCore.QRect(20, 330, 61, 51)
        self.ui.nodeButton_8 = Node(self.ui.centralwidget, self.ui.image_8, 8, node8Pos)

        self.ui.image_9 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_9.setGeometry(QtCore.QRect(320, 230, 101, 101))
        node9Pos = QtCore.QRect(300, 250, 61, 51)
        self.ui.nodeButton_9 = Node(self.ui.centralwidget, self.ui.image_9, 9, node9Pos)

        self.ui.image_10 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_10.setGeometry(QtCore.QRect(510, 240, 101, 101))
        node10Pos = QtCore.QRect(500, 270, 61, 51)
        self.ui.nodeButton_10 = Node(self.ui.centralwidget, self.ui.image_10, 10, node10Pos)

        self.ui.image_11 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_11.setGeometry(QtCore.QRect(750, 300, 101, 101))
        node11Pos = QtCore.QRect(820, 300, 61, 61)
        self.ui.nodeButton_11 = Node(self.ui.centralwidget, self.ui.image_11, 11, node11Pos)

        self.ui.image_12 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_12.setGeometry(QtCore.QRect(140, 450, 101, 101))
        node12Pos = QtCore.QRect(120, 480, 61, 51)
        self.ui.nodeButton_12 = Node(self.ui.centralwidget, self.ui.image_12, 12, node12Pos)

        self.ui.image_13 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_13.setGeometry(QtCore.QRect(360, 380, 101, 101))
        node13Pos = QtCore.QRect(350, 410, 61, 51)
        self.ui.nodeButton_13 = Node(self.ui.centralwidget, self.ui.image_13, 13, node13Pos)

        self.ui.image_14 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_14.setGeometry(QtCore.QRect(890, 420, 101, 101))
        node14Pos = QtCore.QRect(960, 430, 61, 51)
        self.ui.nodeButton_14 = Node(self.ui.centralwidget, self.ui.image_14, 14, node14Pos)

        self.ui.image_15 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.image_15.setGeometry(QtCore.QRect(560, 430, 101, 101))
        node15Pos = QtCore.QRect(620, 470, 61, 51)
        self.ui.nodeButton_15 = Node(self.ui.centralwidget, self.ui.image_15, 15, node15Pos)

        self.nodeList = [self.ui.nodeButton_1, self.ui.nodeButton_2, self.ui.nodeButton_3, 
        self.ui.nodeButton_4, self.ui.nodeButton_5, self.ui.nodeButton_6, 
        self.ui.nodeButton_7, self.ui.nodeButton_8, self.ui.nodeButton_9, 
        self.ui.nodeButton_10, self.ui.nodeButton_11, self.ui.nodeButton_12, 
        self.ui.nodeButton_13, self.ui.nodeButton_14, self.ui.nodeButton_15 ]

        global FFNum
        self.firefighterNum = FFNum
        self.setup_control()

    def setup_control(self):
        # init UI
        self.focusIndex = len(self.nodeList) - 1
        self.initUI()
        # init network
        self.initNode()
        self.randomFireAndDepot()
        self.NodeConnection()

        self.updateStatus()
        for i in self.firefighterList:
            i.doneSignal.connect(self.updateStatus)

    def initUI(self):
        self.ui.actionnodes.triggered.connect(self.showInformationWindow)
        self.descriptionAnimate("choose vertices to save")
        self.ui.node_info_label.setVisible(False)
        self.nodeList[self.focusIndex].setFocus()
        self.labels = [self.ui.FFlabel, self.ui.FFlabel_2]
        self.statusLabels = [self.ui.statuslabel,self.ui.statuslabel_2]
        self.ui.FFlabel.setPixmap(QPixmap("./image/firefighter.png"))
        self.ui.FFlabel_2.setPixmap(QPixmap("./image/fireman.png"))

    def updateStatus(self):
        for i in range(self.firefighterNum):
            if(self.firefighterList[i].isTraveling()):
                self.statusLabels[i].setText("Traveling")
            elif(self.firefighterList[i].isProcess()):
                self.statusLabels[i].setText("Processing")
            elif(self.firefighterList[i].isSelected()):
                self.statusLabels[i].setText("Selected")
            else:
                self.statusLabels[i].setText("Idle")

    def initNode(self):
        for i in self.nodeList:
            temp = random.randrange(5,11)
            i.clicked.connect(self.choose)       
            #i.updateAmount(temp)

    def randomFireAndDepot(self):
        #random fire depot
        a = random.randint(0,13)
        self.fire = Fire(self.nodeList[a])
        #init depot
        depot = self.ui.nodeButton_15
        for i in range(self.firefighterNum):
            ff = FireFighter(i+1, depot)
            depot.depotSetting()
            self.firefighterList.append(ff)
        self.firefighterList[1].pixmap = QPixmap("./image/fireman.png")
        self.nodeList[self.focusIndex].setStyleSheet("background-color: black;border: 2px solid blue;")

    def NodeConnection(self):
        for i in self.nodeList:
            for j in travel_time[i.getNum()]:           
                i.connectNode(self.nodeList[j[0]-1], j[1])

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.InfoDisable()
        if(a0.key()==Qt.Key_Enter-1):
            self.nextTime()
        elif(a0.key() == Qt.Key_A):
            self.buttonFocusStyle(-1)
        elif(a0.key() == Qt.Key_D):
            self.buttonFocusStyle(1)
        elif(a0.key() == Qt.Key_C):
            self.uiChangeFF()
        elif(a0.key() == Qt.Key_X):
            if(not self.ui.node_info_label.isVisible()):
                self.InfoShow()
        self.updateStatus()

    def buttonFocusStyle(self, plus):
        style = self.nodeList[self.focusIndex].styleSheet()
        result_string = ""
        for i in style.split(";"):
            if(i+";" != self.selectedStyle):
                result_string += i+";"
        self.nodeList[self.focusIndex].clearFocus()
        self.nodeList[self.focusIndex].setStyleSheet(result_string)
        self.focusIndex = (self.focusIndex + plus) % 15
        style = self.nodeList[self.focusIndex].styleSheet()
        self.nodeList[self.focusIndex].setStyleSheet(style + self.selectedStyle)
        self.nodeList[self.focusIndex].setFocus()

    def nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(10, 240))
        self.anim.setEndValue(QPoint(1200, 240))
        self.anim.setDuration(500)
        def start():
            self.anim.start()
        QTimer.singleShot(1000, start)  

    def descriptionAnimate(self, text):
        self.ui.descriptionLabel.setText(text)
        self.anim = QPropertyAnimation(self.ui.descriptionLabel, b"pos")
        self.anim.setEndValue(QPoint(10, 240))
        self.anim.setDuration(500)
        self.anim.start()

        self.anim.finished.connect(self.nextAnim)      
        self.ui.descriptionLabel.raise_()

    def InfoShow(self): #鼠標移到node時呼叫
        #移動label位置
        geo = self.nodeList[self.focusIndex].geometry()
        self.ui.node_info_label.setVisible(True)
        pos = QtCore.QRect(geo.x(), geo.y() + geo.width() ,self.ui.node_info_label.frameRect().width(),self.ui.node_info_label.frameRect().height())
        self.ui.node_info_label.setGeometry(pos)
        self.ui.node_info_label.raise_()

        #處理顯示文字
        infotext = self.checkStatus(self.nodeList[self.focusIndex]) #檢查指定消防員是否可以移動到指定點
        text = infotext + "\nnode: {}, A = {}, L= ".format(self.nodeList[self.focusIndex].getNum(), self.nodeList[self.focusIndex].getWaterAmount())
        #取得arc長度
        if(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex]) == -1):
            text += "None"
        else:
            text += str(self.firefighterList[self.FFindex].curPos().getArc(self.nodeList[self.focusIndex])["length"])
        self.ui.node_info_label.setText(text)


    #鼠標離開呼叫: 隱藏label
    def InfoDisable(self):
        self.ui.node_info_label.setVisible(False)

    def uiChangeFF(self):
        self.selectFireFighter()
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))

    def selectFireFighter(self): #選擇消防員
        self.FFindex = (self.FFindex + 1) % self.firefighterNum
        self.__opacitySet()
        self.firefighterList[self.FFindex].curPos().setImage(self.firefighterList[self.FFindex].pixmap)
    
    def __opacitySet(self):
        def setOpacity(num, label):
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(num)
            label.setGraphicsEffect(opacity_effect)

        for i in range(self.firefighterNum):
            opacity = 1 if i == self.FFindex else 0.3
            setOpacity(opacity, self.firefighterList[i].curPos().getLabel())
            setOpacity(opacity, self.labels[i])
        setOpacity(1, self.firefighterList[self.FFindex].curPos().getLabel())

    def printStatus(func):
        def aa(self):
            if(self.firefighterList[self.FFindex].isSelected() and self.sender() != self.firefighterList[self.FFindex].destNode):
                text = "already selected"
            else:
                self.sender().setText(str(self.firefighterList[self.FFindex].num))
                text = func(self)
            self.updateStatus()
            self.descriptionAnimate(text)
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        if (self.sender() == self.firefighterList[self.FFindex].curPos()):
            if(self.firefighterList[self.FFindex].destNode == self.sender()):
                self.firefighterList[self.FFindex].reset()
                self.sender().setStyleSheet("")
                return "{} reset".format(self.firefighterList[self.FFindex].getName())
            else:
                self.tryDefend()
                return "{} choose defend".format(self.firefighterList[self.FFindex].getName())
        else:
            text = self.checkStatus(self.sender())
            if(text == "vaild choose"):
                if(self.firefighterList[self.FFindex].destNode == self.sender()):
                    self.firefighterList[self.FFindex].reset()
                    self.sender().setStyleSheet("")
                    return "{} reset".format(self.firefighterList[self.FFindex].getName())
                self.firefighterList[self.FFindex].processAccept(self.sender(), text)
                text = "{} move to vertex {}".format(self.firefighterList[self.FFindex].getName(), self.sender().getNum())
                return text
            return text


    def checkStatus(self, node):
        if(self.firefighterList[self.FFindex].isProcess()):
            return "this firefighter is processing"
        self.fire.minTimeFireArrival(node)
        if(self.firefighterList[self.FFindex].isTraveling()):
            return "this firefighter is moving"
            #check if selected FireFighter can move to assigned Node
        text = self.firefighterList[self.FFindex].next_Pos_Accessment(node)
        return text

    def tryDefend(self): #指派消防員在原地澆水
        if(not self.firefighterList[self.FFindex].isSelected()):
            text = self.firefighterList[self.FFindex].process_Accessment()
            self.descriptionAnimate(text)


    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():
            text = "moving"
            for i in range(self.currentTime % 3):
                text += "."
            self.descriptionAnimate(text)            
            self.currentTime+=1
            self.fire.fire_spread(self.currentTime)
            for i in self.firefighterList:
                if(i.checkArrival(self.currentTime)):
                    self.descriptionAnimate("finish")
                    self.timer.stop()
            self.__opacitySet()
            self.ui.timeIndexLabel.setText("t= "+str(self.currentTime))
        
        for i in self.firefighterList:
            if(not (i.isTraveling() or i.isProcess())):
                if(i.isIdle()):
                    i.idle(self.currentTime)
                i.move(self.currentTime) 
        
        self.timer.setInterval(500)
        self.timer.timeout.connect(timeSkip)
        self.timer.start()
        

    def showInformationWindow(self):
        self.nw = InformationWindow()
        temp = self.nw.updateOutputMatrix(self.nodeList)
        temp2 =self.nw.setSetupMatrix(self.nodeList,self.firefighterNum,self.firefighterList[self.FFindex].rate_extinguish,self.firefighterList[self.FFindex].move_man,self.fire.rate_fireburn,self.fire.move_fire)
        self.nw.inputmatrix = temp
        self.nw.setupmatrix = temp2
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        self.nw.ui()
        self.nw.show()


