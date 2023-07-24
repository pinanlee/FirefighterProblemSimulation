from PyQt5.QtGui import QImage, QPixmap

class Node:
    def __init__(self, pushButton, label, i, func, temp):
        self.__pushButton = pushButton
        self.__label = label
        self.__pushButton.setProperty("no.", i)
        self.__pushButton.setProperty("burned", False)
        self.__pushButton.setProperty("protected", False)
        self.__pushButton.setProperty("amount", temp)
        self.__pushButton.clicked.connect(func)
        self.__processingTime = 3
        self.__initialamount = temp
    def getNum(self):
        return self.__pushButton.property("no.")
    def onFire(self):
        #onFire setting
        self.__pushButton.setProperty("burned", True)
        self.__pushButton.setStyleSheet(f'background-color: rgba(255, 0, 0, {0.1});')
        #self.__pushButton.setStyleSheet("background-color: red;")

    def isBurned(self):
        return self.__pushButton.property("burned")
    def preDefend(self):
        #self.__pushButton.setProperty("protected",True)
        self.__pushButton.setStyleSheet("background-color: grey")
    def defend(self):
        self.__pushButton.setProperty("protected",True)
        #self.__pushButton.setStyleSheet("background-color: green")
        self.__pushButton.setStyleSheet(f'background-color: rgba(0, 255, 0, {0.1});')

    def isProtected(self):
        return self.__pushButton.property("protected")
    def depotSetting(self):
        self.__pushButton.setStyleSheet("background-color: black;")
        self.__pushButton.setProperty("protected", True)
    def updateAmount(self, remain):
        self.__pushButton.setProperty("amount", remain)
    def getAmount(self):
        return self.__pushButton.property("amount")
    def setImage(self, image):
        self.__label.setPixmap(image)
    def has(self, node):
        if(self.__pushButton == node):
            return True
        return False
    def mark(self, s):
        self.__pushButton.setText(s)
    def getProcessingTime(self):
        return self.__processingTime

class FireFighter:
    def __init__(self, num):
        self.__name = "firefighter " + str(num)
        self.__path = []
        self.__select = False
        self.__arrivalTime = 0
        self.cumArrivalTime = 0
        self.__travel = False

    def move(self, node, arrive, timer):
        self.__arrivalTime = arrive
        self.cumArrivalTime += self.__arrivalTime
        self.destNode = node
        self.checkArrival(timer)

    def isTraveling(self):
        return self.__travel
    def traveling(self):
        self.__travel = True
    def checkArrival(self, timer):
        #print("hi")
        if(self.cumArrivalTime==timer):
            print("j")
            self.__image_path = "firefighter.png"
            pixmap = QPixmap(self.__image_path)
            if(self.__path):
                self.curPos().setImage(QPixmap())
                self.curPos().mark("")
            self.__path.append(self.destNode)
            self.curPos().defend()
            self.curPos().setImage(pixmap)
            self.__select = False
            return True
        elif(self.cumArrivalTime < timer):
            cumArrivalTime = timer
            return True
        return False
    def curPos(self):
        return self.__path[-1]
    def selected(self):
        self.__select = True
    def isSelected(self):
        return self.__select