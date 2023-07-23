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
    def getNum(self):
        return self.__pushButton.property("no.")
    def onFire(self):
        self.__pushButton.setStyleSheet("background-color: red;")
        self.__pushButton.setProperty("burned", True)
    def isBurned(self):
        return self.__pushButton.property("burned")
    def defend(self):
        self.__pushButton.setProperty("protected",True)
        self.__pushButton.setStyleSheet("background-color: green")
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

class FireFighter:
    def __init__(self, num):
        self.__name = "firefighter " + str(num)
        self.__path = []
        self.__select = False
        self.__arrivalTime = 0
    def move(self, node):
        self.__image_path = "firefighter.png"
        pixmap = QPixmap(self.__image_path)
        if(self.__path):
            self.curPos().setImage(QPixmap())
            self.curPos().mark("")
        self.__path.append(node)
        self.curPos().setImage(pixmap)
        self.__select = False
    def curPos(self):
        return self.__path[-1]
    def selected(self):
        self.__select = True
    def isSelected(self):
        return self.__select