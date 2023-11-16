#!/usr/bin/env python
# coding: utf-8
import json
import os
from functools import partial
from PyQt5.QtCore import QTimer, QPropertyAnimation, QPoint, Qt, QPointF
from PyQt5 import QtWidgets, QtGui
import math

from PyQt5.QtWidgets import QWidget

from FFSettingsWindow import FFnumWindow
from FF import FireFighter
from node import Node 
from fireObject import Fire
from network import Network
from PyQt5.QtGui import QPainter, QPen, QFont, QCursor, QColor,  QBrush
from dataBase import DataBase
from results import resultsWindow
import sys
from controllerUtils import Controller_Utils, AnimationTimer, flashTimer

class MainWindow_controller(QtWidgets.QMainWindow):
    modelTest : bool = False
    fire : list[Fire] = []
    nodeList : list[Node] = []
    firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
    firefighterNum = 1
    FFindex = 0 
    labels : QtWidgets.QLabel = []
    timer = QTimer()
    currentTime = 0
    pageList = -1
    FFnetwork : Network = None
    fireNetwork : Network = None
    showFFnetwork : bool = True
    showFireNetwork : bool = True
    FFInfoDict = []
    totalValue = 0
    availFF = 0
    screenshot_range = (290, 60, 1900, 751)
    gameTerminated = False
    model_dir = "./network/FF2test/FFP_n20_no5"
    mode=1
    blocklist=[]
    dashlineWidgetList = []

    def __init__(self,mode):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.mode = mode
        self.flashtimer = []
        Controller_Utils.UIInitialize(self)
        self.subwindows = []
        if os.path.exists("filename.json"):
            with open("filename.json", 'r') as file:
                data = json.load(file)
            self.model_dir = data["filename"][:-5]
        self.setup_control()
        self.window_FFnum = FFnumWindow()
        self.window_FFnum.window_FF.updateFFnumSignal.connect(self.newFFnum)
        self.block_completelist = []
        self.ffAccess_DashlineAnimation()
        self.move_downbar()
        self.make_draggable(self.widget_downbar)


    '''------------------------------------初始化--------------------------------------------------------'''
    def setup_control(self):
        Controller_Utils.createNetworkInfrastructures(self)
        Controller_Utils.nodeListInitialize(self)
        Controller_Utils.nodeConnection(self)
        Controller_Utils.depotInitialize(self)
        Controller_Utils.UIInformationInitialization(self)
        
    def modelTimeSet(self):
        Controller_Utils.getModelSolution(self)
        self.modelTime = QTimer()
        self.modelTime.timeout.connect(self.modelAuto)
        self.modelTime.setInterval(300)
        self.modelTime.start()

    def modelAuto(self):
        assignCandidate = [self.temp[s-1][0] for s in DataBase.K]
        assignCandidate.sort(key=lambda x: x[3])

        (i,j,k,t) = (assignCandidate[0][0],assignCandidate[0][1],assignCandidate[0][2],assignCandidate[0][3])
        self.focusIndex = j-1
        self.FFindex = k-1
        if t == self.currentTime:
            if i != j: 
                self.choose()
                text = "消防員 {}在時刻 {} 從node {} 移動到 node {} ,travel time: {}".format(k, t, i, j, DataBase.tau[f"({i}, {j}, {float(k)})"]) 
            else:         
                if DataBase.u_bar[f"({i}, {k}, {t})"] > DataBase.epsilon:
                    self.choose()
                    text = "消防員 {}在時刻 {} 對node {} 進行保護, processing time: {}".format(k,t,i, math.ceil(DataBase.Q[f"{i}"] * DataBase.b[f"{i}"] / self.currentSelectedFF().rate_extinguish)) 
                else:
                    self.assignIdle()
                    text = "消防員 {}在時刻 {} 在node {} idle".format(k,t,i)
            print(text)
            self.consoleLabel.setText(text)
            self.temp[k-1].append(self.temp[k-1].pop(0))
        

    def howManyAvail(self):
        if(not self.modelTest):
            self.criticalMessage ="firefighter available: {}".format(self.availFF) 
            self.hintAnimate(self.criticalMessage)
        
    def showProblem(self):
        self.inst.show()

    def assignIdle(self):
        if(self.currentSelectedFF().isSelected()):
            self.descriptionAnimate("Invaild assignment: No available firefighter")
            return 
        
        if(self.currentSelectedFF().curPos().getFireMinArrivalTime() < self.currentTime + self.spinBox.value()):
            self.descriptionAnimate("Invaild assignment: fire will arrive during idle")
            return

        self.availFF -= 1
        self.descriptionAnimate("Assign sucessful! : {} idle for {} time step(s)".format(self.currentSelectedFF().getName(), self.spinBox.value()))
        self.nextTime()
        return "assign idle"

    def idleLock(self):
        if(self.checkBox.isChecked()):
            self.spinBox.setValue(300)
        self.spinBox.setEnabled(not self.checkBox.isChecked())

    def currentSelectedFF(self):
        return self.firefighterList[self.FFindex]

    '''---------------------------------------firefighter signal-----------------------------------------'''
    def ffSignalDetermination(self, text, no):
        if(text == "protect"):
            self.networkUpdate(no)
        if(text == "trapped"):
            self.criticalMessage = f"firefighter {no} can't move to other nodes, please assign protect or idle to the end"
            self.hintAnimate(self.criticalMessage)

    def networkUpdate(self,no): #FF network有節點被保護時呼叫，更新fire network
        self.fireNetwork.nodeList[no-1].defend()
        self.updateMinTime()

    def updateMinTime(self): #更新FF network的fireMinArrivalTime
        for i in self.fireNetwork.nodeList:
            i.setFireMinArrivalTime(10000)
        
        [i.minTimeFireArrival() for i in self.fire]

        for i in self.FFnetwork.nodeList:
            i.setFireMinArrivalTime(self.fireNetwork.nodeList[i.getNum()-1].getFireMinArrivalTime())


    '''------------------------------------------fire signal---------------------------------------------'''
    def fireSignalDetermination(self, text, opacity = 0, no = 0):
        if(text == "burn"):
            self.networkUpdateF(no)
        if(text == "visual"):
            self.fireVisualize(opacity, no)
    
    def networkUpdateF(self,no): #當fire network有新的節點燒起來時，更新ff network並增加新的"火"物件
        self.nodeList[no - 1].onFire()
        self.fire.append(Fire(self.fireNetwork, no, self.currentTime))
        self.listWidget.addItem(f"At time {self.currentTime}, node {no} had burned")
        self.listWidget.scrollToItem(self.listWidget.item(self.listWidget.count() - 1))
        self.fire[-1].fireSignal.connect(self.fireSignalDetermination)

    def fireVisualize(self, opacity, no): #當fire network的節點正在燃燒時，更新ui上的opacity
        self.nodeList[no-1].setStyle(f'background-color: rgba(255, 0, 0, {opacity}); color: white;')
        if(opacity==1):
            self.nodeList[no - 1].setStyle(f'background-color: rgba(139, 0, 0, {opacity}); color: white;')

        self.nodeList[no-1].setStyleSheet(self.nodeList[no-1].getStyle())
        self.totalValue = self.fireNetwork.getTotalValue()
        self.progressBar.setValue(self.totalValue)

    def finish(self):
        self.timer.stop()
        if(self.modelTest):
            self.modelTime.stop()
        self.result = resultsWindow(self.nodeList, self.currentTime)
        self.result.show()
        if os.path.exists("filename.json"):
            os.remove("filename.json")

    '''------------------------------操作方式-----------------------------------'''
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if(a0.key() == Qt.Key_S):
            self.networkChange()
        if(a0.key() == Qt.Key_N):
            self.newNetwork()
        if(a0.key() == Qt.Key_Q):
            self.finish()
        if(a0.key() == Qt.Key_X):
            self.showProperty(1)
        if(a0.key() == Qt.Key_Z):
            self.showProperty(0)
        if(a0.key() == Qt.Key_A):
            self.modelTimeSet()

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        for i in self.nodeList:
            i.grassVisualize.hide()

    def showProperty(self, key):
        for i in self.nodeList:
            if(key):
                i.grassVisualize.showGrassValue()
                i.grassVisualize.setText(str(math.ceil(i.getProcessingTime()/self.currentSelectedFF().rate_extinguish)))
            else:
                i.grassVisualize.showValue()
                i.grassVisualize.setText(str(i.getValue()))
            i.grassVisualize.show()

    def newNetwork(self):
        from randomPlanarGraph.GenerateGraph import generate_test_data
        generate_test_data(20, 35, 35, 1)
        self.model_dir = "./randomPlanarGraph/data/FFP_n20_no1"
        # for _, _, files in os.walk("./randomPlanarGraph/data/"):
        #     self.model_dir = "./randomPlanarGraph/data" + files[self.__num-1:-5]
        for i in self.nodeList:
            i.deleteLater()
        for i in self.firefighterList:
            i.deleteLater()
        for i in self.fire:
            i.deleteLater()
        for i in self.labels:
            i.deleteLater()
        del self.FFnetwork
        del self.fireNetwork
        for i in self.blocklist:
            i.flash_timer.stop()
            i.deleteLater()
        self.modelTest : bool = False
        self.fire : list[Fire] = []
        self.nodeList : list[Node] = []
        self.firefighterList : list[FireFighter] = [] #store all firefighter (class: FireFighter)
        self.firefighterNum = 1
        self.FFindex = 0 
        self.labels : QtWidgets.QLabel = []
        self.timer = QTimer()
        self.currentTime = 0
        self.pageList = -1
        self.FFnetwork : Network = None
        self.fireNetwork : Network = None
        self.showFFnetwork : bool = True
        self.showFireNetwork : bool = True
        self.FFInfoDict = []
        self.totalValue = 0
        self.availFF = 0
        self.gameTerminated = False
        self.blocklist=[]
        Controller_Utils.createNetworkInfrastructures(self)
        Controller_Utils.nodeListInitialize(self)
        Controller_Utils.nodeConnection(self)
        Controller_Utils.depotInitialize(self)
        Controller_Utils.UIInformationInitialization(self)
        # import subprocess
        # import os
        # subprocess.call("./randomPlanerGraph/GenerateGraph.py", shell=True)
        # p = sys.executable
        # os.execl(p, p, *sys.argv)

    def newFFnum(self):
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)


    def networkChange(self):
        if(self.showFFnetwork and self.showFireNetwork):
            self.showFireNetwork = False
            self.networkLabel.setText("FF network")
            self.comboBox_network.setCurrentIndex(2)
        elif(self.showFFnetwork and not self.showFireNetwork):
            self.showFFnetwork, self.showFireNetwork = False, True
            self.networkLabel.setText("Fire network")
            self.comboBox_network.setCurrentIndex(1)
        elif(not self.showFFnetwork and self.showFireNetwork):
            self.showFFnetwork = True
            self.networkLabel.setText("Hybrid network")
            self.comboBox_network.setCurrentIndex(0)

    def __nextAnim(self):
        self.anim.stop()
        self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
        self.anim.setStartValue(QPoint(800, 710))
        self.anim.setEndValue(QPoint(2200, 710))
        self.anim.setDuration(250)
        def start():
            self.anim.start()
        QTimer.singleShot(1500, start)

    def descriptionAnimate(self, text):
        def initAnim(self):
            self.descriptionLabel.setText(text)
            self.descriptionLabel.raise_()
            self.anim = QPropertyAnimation(self.descriptionLabel, b"pos")
            self.anim.setStartValue(QPoint(2200, 600))
            self.anim.setEndValue(QPoint(800, 600))
            self.anim.setDuration(250)
            
        initAnim(self)
        self.anim.start()

    def flashTimerActivate(self, selectedWidget):
        selectedWidget.activate()


    def __nextHintAnim(self):
        if self.index < len(self.text):
            self.consoleLabel.setText(self.text[:self.index+1])
            self.index += 1
        else:
            self.timeHint.stop()

    def hintAnimate(self, text):
        self.index = 0
        self.text = text
        self.timeHint = QTimer()
        self.timeHint.setInterval(5)
        self.timeHint.timeout.connect(self.__nextHintAnim)
        self.timeHint.start()        

    def InfoShow(self,no): #查看node資訊
        #處理顯示文字
        if(no==-1):
            self.hintAnimate(self.criticalMessage)
            return
        nodeNum, status, burntime = self.sender().getNum(), self.sender().getStatus(), self.sender().getFireMinArrivalTime()
        text = "Node: {} ({}), \nEarlist burn time: {}, \nTravel time: ".format(nodeNum, status, burntime)
        if(self.currentSelectedFF().curPos().getArc(self.sender()) != None):
            text+= str(self.currentSelectedFF().curPos().getArc(self.sender())["travel-time"][f"{self.FFindex+1}"])
        else:
            text+="not neighbor"
        if(not self.modelTest):
            self.hintAnimate(text)

    def selectFireFighter(self, index): #切換選擇消防員
        self.currentSelectedFF().closeaccessibleVisualize(self.nodeList)
        self.FFindex = index - 1
        self.opacitySet()
        for index,block in enumerate(self.blocklist):
            opacity = 1 if index == self.FFindex else 0.3
            block.setOpacity(opacity)
        self.currentSelectedFF().accessibleVisualize(self.currentTime, self.nodeList)
        # self.refreshBlock()
        self.label_selectedFF.setText(self.currentSelectedFF().getName())

    def opacitySet(self): #調整FF的opacity
        for index,block in enumerate(self.blocklist):
            if index == self.FFindex:
                opacity = 1
                pos_global = block.mapToGlobal(block.title_label_img.pos())
                y_position_in_layout = self.centralWidget().mapFromGlobal(pos_global).y()
                self.selectedFFlabel.setGeometry(self.selectedFFlabel.x(),y_position_in_layout,self.selectedFFlabel.width(),self.selectedFFlabel.height())
            else:
                opacity = 0.3
            block.setOpacity(opacity)

    def printStatus(func):
        def aa(self):
            text = func(self)
            self.descriptionAnimate(text)            
            self.nextTime()
        return aa
    @printStatus
    def choose(self): #指派消防員移動至給定node
        send = None
        if(not self.modelTest):
            send = self.currentSelectedFF().curPos() if self.sender().objectName() == "defendButton" else self.sender()
        else:
            send = self.nodeList[self.focusIndex]
        text = self.checkStatus(send)
        if(text == "vaild choose"):
            text = self.currentSelectedFF().processCheck(send)
            # self.refreshBlock()
            self.availFF -= 1
            return text
        return text

    def refreshBlock(self):
        for index,block in enumerate(self.blocklist):
            block.setStatus(self.firefighterList[index].getStatus())
            # block.title_label_ready_des.setText(self.firefighterList[index].getStatus())
        # self.clear_layout(self.verticalLayout)
        # self.generateblockFF_gameWindow()

    def checkStatus(self, node):
        if(self.currentSelectedFF().isProcess() or self.currentSelectedFF().isTraveling()):
            return "No firefighter is available"
        if(node == self.currentSelectedFF().curPos()):
            return "vaild choose"
            #check if selected FireFighter can move to assigned Node
        text = self.currentSelectedFF().next_Pos_Accessment(node, self.currentTime)
        return text
        
    def nextTime(self): #跳轉至下一個時間點
        self.deleteDashWidget()
        def timeSkip():
            Controller_Utils.screenshot(self.screenshot_range, self.currentTime)
            self.currentTime+=1

            finishList = Controller_Utils.firefighterMoveLogic(self)
            if(finishList):
                # setattr(self.widget_downright, "flash_timer", flashTimer(self.widget_downright))
                # self.flashTimerActivate(self.widget_downright)
                
                self.availFF = len(finishList)
                self.howManyAvail()
                text = ""
                for i in finishList:
                    if(self.firefighterList[i-1].curPos().isBurned()):
                        self.criticalMessage = f"firefighter {i}'s position just burned, please protect it."
                    self.flashTimerActivate(self.blocklist[i-1])
                    text += str(i) + ", "
                self.selectFireFighter(finishList[0])
                self.descriptionAnimate("firefighter {} has finished task".format(text[:-2]))
                
                self.refreshBlock()
                self.ffAccess_DashlineAnimation()
                self.move_downbar()
            Controller_Utils.fireSpreadLogic(self.fire)
            
            self.lcd_time.display(self.currentTime)

            self.gameTerminated = all(i.isComplete() for i in self.fire) or self.currentTime == DataBase.T
            if self.gameTerminated:
                self.finish()
                return

        if(not self.availFF):
            self.deleteDashWidget()
            self.widget_downbar.setVisible(False)
            
            for ff in self.firefighterList:
                if(not (ff.isTraveling() or ff.isProcess())):
                    ff.finishTimeSet(self.spinBox.value())
                    ff.closeaccessibleVisualize(self.nodeList)
                ff.move()
            self.timer = AnimationTimer()
            self.timer.timeout.connect(timeSkip)
            self.timer.start()
        else:
            for i in self.firefighterList:
                if not i.isSelected():
                    self.selectFireFighter(i.getNum())
                    break
            self.howManyAvail()
        self.refreshBlock()

    def onSubWindowPageChanged(self, index):
        self.pageList = index
   
    def paintEvent(self, event):
        if self.mode == 1:
            qpainter = QPainter()
            qpainter.setRenderHint(QPainter.Antialiasing)
        elif self.mode == 2 :
            qpainter = QPainter(self.label_background.pixmap())
            qpainter.setRenderHint(QPainter.Antialiasing)
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing)
        if(self.showFireNetwork):
            qpen = QPen(Qt.red, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.fireNetwork.nodeList:
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))
                    elif self.mode == 2:
                        qpainter.drawLine(
                            QPointF(i.x()  +  2.1 * i.width() / 2, i.y() + 6 / 2 * i.height()),
                            QPointF(j.x()  +  2.1 * j.width() / 2, j.y() + 6 / 2 * j.height()))

            for i in self.nodeList:
                i.setText(str(i.getFireMinArrivalTime()))
        if(self.showFFnetwork):
            qpen = QPen(Qt.black, 4, Qt.SolidLine)
            qpainter.setPen(qpen)
            for i in self.nodeList:
                i.setText(str(i.getNum()))
                for j in i.getNeighbors():
                    if self.mode == 1:
                        qpainter.drawLine(
                            QPointF(i.x() + self.gamewidget.x() + i.width() / 2, i.y() + 5 / 2 * i.height()),
                            QPointF(j.x() + self.gamewidget.x() + j.width() / 2, j.y() + 5 / 2 * j.height()))
                    elif self.mode == 2:
                        qpen = QPen(Qt.black, 6, Qt.SolidLine)
                        qpainter.setPen(qpen)
                        qpainter.drawLine(
                            QPointF(i.x()  + i.width() / 2, i.y() + 3 / 2 * i.height()),
                            QPointF(j.x()  + j.width() / 2, j.y() + 3 / 2 * j.height()))
                        if i.getNodePercentage_FF(self.currentSelectedFF().rate_extinguish)>=0.5 and j.getNodePercentage_FF(self.currentSelectedFF().rate_extinguish)>=0.5 :
                            qpen = QPen(Qt.yellow, 6, Qt.SolidLine)
                            qpainter.setPen(qpen)
                            qpainter.drawLine(
                                QPointF(i.x() + i.width() / 2, i.y() + 3 / 2 * i.height()),
                                QPointF(j.x() + j.width() / 2, j.y() + 3 / 2 * j.height()))

        for i in self.fire:
            for j in i.getArcs():
                    tempXpercent = (j["node"].x() + j["node"].width()/2 - i.x() - i.width()/2) * i.getArcPercentage_Fire(j)
                    tempYpercent = (j["node"].y() + 3/2*j["node"].height() - i.y() - 3/2*i.height()) * i.getArcPercentage_Fire(j)
                    qpen = QPen(Qt.darkRed, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.x() + self.gamewidget.x() + i.width()/2, i.y() + 5/2*i.height()), QPointF(i.x() + self.gamewidget.x() + i.width()/2 + tempXpercent, i.y() + 5/2*i.height() + tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.x() + 2.1 * i.width()/2, i.y() + 6/2*i.height()), QPointF(i.x()  + 2.1 * i.width()/2 + tempXpercent, i.y() + 6/2*i.height() + tempYpercent))
                        current_x = int(i.x() + tempXpercent - 4*i.width()/2)
                        current_y = int(i.y() + tempYpercent - 3*i.height()/2)
                        qpainter.setPen(Qt.NoPen)
                        qpainter.drawEllipse(current_x, current_y, 150, 150)
                        brush = QBrush(QColor(100, 0, 0, 2))
                        qpainter.setBrush(brush)
                        qpainter.drawEllipse(current_x, current_y, 150, 150)


        for i in self.firefighterList:
            if(i.destination() != None):
                    tempXpercent = (i.destination().x() + i.destination().width()/2 - i.curPos().x() - i.curPos().width()/2) * i.getArcPercentage_FF(i.destination())
                    tempYpercent = (i.destination().y() + 3/2*i.destination().height() - i.curPos().y() - 3/2*i.curPos().height()) * i.getArcPercentage_FF(i.destination())
                    qpen = QPen(Qt.darkGreen, 6, Qt.SolidLine)
                    qpainter.setPen(qpen)
                    if self.mode == 1:
                        qpainter.drawLine(QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2, i.curPos().y() + 5/2*i.curPos().height()), QPointF(i.curPos().x() + self.gamewidget.x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 5/2*i.curPos().height()+tempYpercent))
                    elif self.mode == 2:
                        qpainter.drawLine(QPointF(i.curPos().x()+ i.curPos().width()/2, i.curPos().y() + 3/2*i.curPos().height()), QPointF(i.curPos().x() + i.curPos().width()/2 + tempXpercent ,i.curPos().y() + 3/2*i.curPos().height()+tempYpercent))
        self.update()
        qpainter.end()


    def closeEvent(self, event): #當主視窗關閉時關閉全部視窗
        # if os.path.exists("FFInfo.json"):
        #     os.remove("FFInfo.json")
        if os.path.exists("filename.json"):
            os.remove("filename.json")
        for subwindow in self.subwindows:
            subwindow.close()  # Close all open subwindows
        event.accept()

        folder_path_to_delete = "image/timescreenshot"
        try:
            for filename in os.listdir(folder_path_to_delete):
                file_path = os.path.join(folder_path_to_delete, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print("Error")

    def showFFWindow(self):
        self.subwindows.append(self.window_FFnum)
        self.subwindows.append(self.window_FFnum.window_FF)
        self.window_FFnum.show()

    def generateblockFF_gameWindow(self):
        from gameWindow import gameWindow
        self.blocklist = []
        for i in self.firefighterList:
            block = gameWindow(self, self.firefighterList[i.getNum()-1])
            self.blocklist.append(block)
            self.verticalLayout.addWidget(block)
        self.opacitySet()

    def backMenu(self):
        import os
        p = sys.executable
        os.execl(p, p, *sys.argv)

    def comboBoxEvent(self,text):
        if(text == "Hybrid network"):
            self.showFFnetwork = False
            self.showFireNetwork = True
        elif(text == "FF network"):
            self.showFFnetwork = True
            self.showFireNetwork = True
        elif(text == "Fire network"):
            self.showFFnetwork = True
            self.showFireNetwork = False
        self.networkChange()

    def dashlineAnimation(self,parent,x1,y1,x2,y2):
        dash_widget = QWidget(parent)
        dash_widget.raise_()
        # dash_widget.setStyleSheet(f'background-color: red;') //用來看dash_widget大小的
        for tmp in self.nodeList:
            tmp.raise_()
        self.widget_downbar.raise_()
        dash_widget.setGeometry(0, 0, 1000, 1000)
        dash_widget.length = 6
        dash_widget.width = 5
        dash_widget.lineStep = 1
        dash_widget.speed = 100
        dash_widget.lineColor = Qt.blue
        dash_widget.dashes = dash_widget.length
        dash_widget.spaces = dash_widget.length
        dash_widget.dashPattern = [dash_widget.length] * 20
        dash_widget.timer = QTimer(dash_widget)
        dash_widget.timer.timeout.connect(lambda: updateLine(dash_widget))
        dash_widget.timer.start(dash_widget.speed)

        def paintEvent(event):
            painter = QPainter(dash_widget)
            painter.setRenderHints(QPainter.Antialiasing)
            pen = QPen()
            pen.setWidth(dash_widget.width)
            pen.setColor(dash_widget.lineColor)
            pen.setDashPattern(dash_widget.dashPattern)
            painter.setPen(pen)
            start = QPointF(x1,y1)
            end = QPointF(x2,y2)
            painter.drawLine(start,end)
        def updateLine(widget):
            if widget.dashes == widget.length and widget.spaces == widget.length:
                widget.dashes = 0
                widget.spaces = 0
            if widget.dashes == 0 and widget.spaces < widget.length:
                widget.spaces += widget.lineStep
            elif widget.spaces == widget.length and widget.dashes < widget.length:
                widget.dashes += widget.lineStep
            widget.dashPattern[0] = widget.dashes
            widget.dashPattern[1] = widget.spaces
            widget.update()

        dash_widget.paintEvent = paintEvent
        dash_widget.updateValue = updateLine
        return dash_widget

    def ffAccess_DashlineAnimation(self):
        for i in self.firefighterList:
            if i.getNum()-1 == self.FFindex:
                for j in (i.curPos().getNeighbors()):
                    node = i.curPos()
                    x1 = node.x()+ node.width() / 2
                    y1 = node.y() + node.height() / 2
                    x2 = j.x() + j.width() / 2
                    y2 = j.y() + j.height() / 2
                    drawingWidget = self.dashlineAnimation(self.gamewidget,x1,y1,x2,y2)
                    self.dashlineWidgetList.append(drawingWidget)
                    drawingWidget.show()

    def deleteDashWidget(self):
        for i in self.dashlineWidgetList:
            i.deleteLater()
        self.dashlineWidgetList = []

    def move_downbar(self):
        self.widget_downbar.setVisible(True)
        loc_x = self.firefighterList[self.FFindex].x() + self.firefighterList[self.FFindex].width()
        loc_y = self.firefighterList[self.FFindex].y()
        self.widget_downbar.move(loc_x,loc_y)
    def make_draggable(self,widget):
        dragging = False
        offset = QPoint()

        def on_mouse_press(event):
            nonlocal dragging, offset #nonlocal: 讓巢狀function的內部function同步修改外部variable值
            if event.buttons() == Qt.LeftButton:
                dragging = True
                offset = event.pos()
        def on_mouse_move(event):
            nonlocal dragging, offset
            if dragging:
                widget.move(widget.mapToParent(event.pos() - offset))
        def on_mouse_release(event):
            nonlocal dragging
            if event.button() == Qt.LeftButton:
                dragging = False

        widget.mousePressEvent = on_mouse_press
        widget.mouseMoveEvent = on_mouse_move
        widget.mouseReleaseEvent = on_mouse_release