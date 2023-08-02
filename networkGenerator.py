from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from UIv2_ui import Ui_MainWindow
import pandas as pd
from node import Node
traveltime = [[]]

class example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupControl()

    def setupControl(self):
        global traveltime
        df = pd.read_excel("firefighter_route.xlsx")
        df_num = len(df.index)
        nodeNum = df.iloc[0]["node"]
        for i in range(int(nodeNum)):
            traveltime.append([])
        for i in range(df_num):
        #print(df_num)
            traveltime[int(df.iloc[i]['i'])].append([df.iloc[i]["j"],df.iloc[i]["travel time"]])
        print(traveltime)    
        self.ui.image_1 = QtWidgets.QLabel(self.ui.centralwidget)
        node1Pos = QtCore.QRect(310, 20, 61, 51)
        #self.ui.image_1.setGeometry(QtCore.QRect(230, 0, 101, 101))
        self.ui.image_1.setGeometry(QtCore.QRect(310-20, 20-25, 101, 101))
        #self.ui.image_1.setGeometry(node1Pos)
        self.ui.image_1.setPixmap(QPixmap("firefighter.png"))

        self.nodeButton_1 = Node(self.ui.centralwidget, self.ui.image_1, 1, node1Pos)
        self.nodeButton_1.raise_()
        self.nodeButton_1.setStyleSheet("border-radius : 50px; border:2px soild black; background-color: red")
