#!/usr/bin/env python
# coding: utf-8
from PyQt5.QtCore import QTimer, QPointF, pyqtSignal
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer
import random
import math
from UIv2_ui import Ui_MainWindow
#from example_ui import Ui_MainWindow
from FF import FireFighter
from node import Node 
from fire import Fire
from InformationWindow import InformationWindow
from PyQt5.QtCore import QPropertyAnimation, QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen

'''
Bug or improvement:
消防員個數自定義
status 顯示可以更完整: 去...node ,在... node processing


Latest task : 
增加消防員可選點可視化 完成 (需要修飾code)
arc進度條 消防員還沒有好

未來更新 : 
跟li合併
火燒過來消防員怎麼辦
idle的標示
動態更新information window 
自定義生成網路
結算畫面

有時間做:
Readme 版本紀錄資訊、簡介
UI Designed
'''


#parameter settings



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
    focusIndex = 14
    nodeList : list[Node] = []
    #nodeList = []
    firefighterNum = 3
    selectedStyle : str = "border: 2px solid blue;"
    FFindex = 0
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    #firefighterList = []
    timer = QTimer()
    currentTime = 0
    xPositionList = [[]]
    yPositionList = [[]]


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
        #self.firefighterNum = FFNum
        self.setup_control()
        self.nw = InformationWindow()


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
        self.ui.FFlabel.setPixmap(QPixmap("firefighter.png"))
        self.ui.FFlabel_2.setPixmap(QPixmap("fireman.png"))



    def updateStatus(self):
        if(self.firefighterList[0].isTraveling()):
            self.ui.statuslabel.setText("Traveling")
        elif(self.firefighterList[0].isProcess()):
            self.ui.statuslabel.setText("Processing")
        elif(self.firefighterList[0].isSelected()):
            self.ui.statuslabel.setText("Selected")
        else:
            self.ui.statuslabel.setText("Idle")

        if(self.firefighterList[1].isTraveling()):
            self.ui.statuslabel_2.setText("Traveling")
        elif(self.firefighterList[1].isProcess()):
            self.ui.statuslabel_2.setText("Processing")
        elif(self.firefighterList[1].isSelected()):
            self.ui.statuslabel_2.setText("Selected")
        else:
            self.ui.statuslabel_2.setText("Idle")

    def initNode(self):
        for i in self.nodeList:
            temp = random.randrange(5,11)
            i.clicked.connect(self.choose)       
            #i.updateAmount(temp)
            #紀錄按鈕的位置，因為位置預設在左上，後面值為調整座標至中間
            self.xPositionList.append(i.getXposition() + i.width() / 2)
            self.yPositionList.append(i.getYposition() + i.width() / 2)

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
        self.firefighterList[1].pixmap = QPixmap("fireman.png")
        self.nodeList[self.focusIndex].setStyleSheet("background-color: black;border: 2px solid blue;")

    def NodeConnection(self):
        for i in self.nodeList:
            for j in travel_time[i.getNum()]:           
                i.connectNode(self.nodeList[j[0]-1], j[1])

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if(a0.key()==Qt.Key_Enter-1):
            self.nextTime()
            self.updateStatus()
            return
        elif(a0.key() == Qt.Key_A):
            self.InfoDisable()
            self.buttonFocusStyle(-1)
        elif(a0.key() == Qt.Key_D):
            self.InfoDisable()
            self.buttonFocusStyle(1)
        elif(a0.key() == Qt.Key_C):
            self.InfoDisable()
            self.uiChangeFF()
            self.updateStatus()
        elif(a0.key() == Qt.Key_X):
            if(self.ui.node_info_label.isVisible()):
                self.InfoDisable()
            else:
                self.InfoShow()

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
        #print(text)
        self.ui.node_info_label.setText(text)


    #鼠標離開呼叫: 隱藏label
    def InfoDisable(self):
        self.ui.node_info_label.setVisible(False)

    def uiChangeFF(self):
        self.selectFireFighter()
        self.descriptionAnimate("change to {}".format(self.firefighterList[self.FFindex].getName()))

    def selectFireFighter(self): #選擇消防員
        prev = self.FFindex
        self.FFindex = (self.FFindex + 1) % self.firefighterNum

        self.__opacitySet()
        if(self.firefighterList[self.FFindex].isSelected()):
            for i in range(len(self.firefighterList)):
                if(not self.firefighterList[i].isSelected()):
                    self.FFindex = prev
                    return
            self.FFindex = prev
            self.__opacitySet()
            self.descriptionAnimate("all firefighter has assigned")
        self.firefighterList[self.FFindex].curPos().setImage(self.firefighterList[self.FFindex].pixmap)

        for i in (self.firefighterList[self.FFindex].curPos().getNeighbors()): #計算鄰近點minTimeFireArrival
            self.fire.minTimeFireArrival(i)
        self.firefighterList[prev].closeaccessibleVisualize()
        self.firefighterList[self.FFindex].accessibleVisualize(self.nodeList)
    
    def __opacitySet(self):
        for i in self.firefighterList:
            i.curPos().setOpacity(0.3)
        self.firefighterList[self.FFindex].curPos().setOpacity(1)


    def printStatus(func):
        def aa(self):
            if (self.firefighterList[self.FFindex].isSelected() and self.sender() != self.firefighterList[
                self.FFindex].destNode):
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
                self.selectFireFighter()
                return text
            return text


    def checkStatus(self, node):
        if(not self.firefighterList[self.FFindex].isProcess()):
            self.fire.minTimeFireArrival(node)
            if(not self.firefighterList[self.FFindex].isTraveling()):
                #check if selected FireFighter can move to assigned Node
                text = self.firefighterList[self.FFindex].next_Pos_Accessment(node)
                return text
            else:
                return "this firefighter is moving"
        else:
            return "this firefighter is processing"

    def tryDefend(self): #指派消防員在原地澆水
        if(not self.firefighterList[self.FFindex].isSelected()):
            text = self.firefighterList[self.FFindex].process_Accessment()
            self.selectFireFighter()
            self.descriptionAnimate(text)


    def nextTime(self): #跳轉至下一個時間點
        def timeSkip():
            text = "moving"
            print("func")
            self.upadateInformation()
            self.currentTime+=1
            self.fire.fire_spread(self.currentTime)
            for i in self.firefighterList:
                i.move(self.currentTime)
                if(i.checkArrival(self.currentTime)):
                    self.timer.stop()
            self.__opacitySet()
            self.ui.timeIndexLabel.setText("t= "+str(self.currentTime))
            self.ui.descriptionLabel.setText("moving.")


        for i in self.firefighterList:
            if(not (i.isTraveling() or i.isProcess())):
                '''if(i.isIdle()):
                    i.idle(self.currentTime)
                i.move(self.currentTime)'''
                i.finishTimeSet()
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(timeSkip)
        self.timer.start()
        

    def showInformationWindow(self):
        #self.nw = InformationWindow()
        self.upadateInformation()
        self.nw.show()


    def onSubWindowPageChanged(self, index):
        print("現在選中的index：", index)
        self.nw.tab_widget.setCurrentIndex(index)


    def upadateInformation(self):
        #self.nw.pageChanged.connect(self.onSubWindowPageChanged)


        temp = self.nw.updateOutputMatrix(self.nodeList,self.firefighterList)
        temp2 = self.nw.setSetupMatrix(self.nodeList, self.firefighterNum,
                                       self.firefighterList[self.FFindex].rate_extinguish,
                                       self.firefighterList[self.FFindex].move_man, self.fire.rate_fireburn,
                                       self.fire.move_fire)
        self.nw.inputmatrix = temp
        self.nw.setupmatrix = temp2
        x = self.nw.pos().x()
        y = self.nw.pos().y()
        self.nw.move(x, y)
        self.nw.ui()


    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpen = QPen(Qt.darkGray, 2, Qt.SolidLine)
        qpainter.setPen(qpen)


        for i in self.nodeList:
            for j in i.getNeighbors():
                qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[j.getNum()], self.yPositionList[j.getNum()]))
                i.getXposition() + i.width()/2

        for i in self.nodeList:
            if(i.isBurned()):
                for j in i.getNeighbors():
                    tempXpercent = (self.xPositionList[j.getNum()] - self.xPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)
                    tempYpercent = (self.yPositionList[j.getNum()] - self.yPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)

                    qpen.setColor(Qt.red)
                    qpen.setWidth(6)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[i.getNum()]+tempXpercent ,self.yPositionList[i.getNum()]+tempYpercent))

        for i in self.nodeList:
                for j in i.getNeighbors():
                    tempXpercent = (self.xPositionList[j.getNum()] - self.xPositionList[i.getNum()]) * i.getArcPercentage_FF(j)
                    tempYpercent = (self.yPositionList[j.getNum()] - self.yPositionList[i.getNum()]) * i.getArcPercentage_FF(j)

                    qpen.setColor(Qt.darkGreen)
                    qpen.setWidth(6)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(self.xPositionList[i.getNum()], self.yPositionList[i.getNum()]), QPointF(self.xPositionList[i.getNum()]+tempXpercent ,self.yPositionList[i.getNum()]+tempYpercent))

        self.update()
        qpainter.end()


