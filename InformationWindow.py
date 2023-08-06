from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QSizePolicy, QTabWidget
from PyQt5 import QtWidgets


class InformationWindow(QtWidgets.QMainWindow):
    pageChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Information Window')
        inputmatrix = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],

        ] #InputMatrix紀錄node information ; row數量代表節點數目, column數量代表想要呈現的數據名稱數量 0無意義 (目前為手動增加)
        outputmatrix =[] #OutputMatrix為使用者看到的table
        setupmatrix = [[0,1,2],[0,1,2]]
        self.inputmatrix = inputmatrix
        self.outputmatrix = outputmatrix
        self.setupmatrix = setupmatrix
        self.currentIndex = 0
        self.ui()

    def ui(self):

        # new a QTabWidget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        #增加分頁
        self.pageBasicSetup = QWidget()
        self.pageNode = QWidget()
        self.pageFF = QWidget()
        self.tab_widget.addTab(self.pageBasicSetup, "Basic Setup")
        self.tab_widget.addTab(self.pageNode, "Node Information")
        self.tab_widget.addTab(self.pageFF, "FireFighter Information")

        #Page : Basic Setup
        #Basic Setup table
        layoutBasic = QVBoxLayout(self.tab_widget)
        table_widget_basicsetup = QTableWidget()
        table_widget_basicsetup.setRowCount(2)
        table_widget_basicsetup.setColumnCount(3)
        self.basicSetuptableVisualizeSetting(table_widget_basicsetup)
        title_name_basicsetup=["Number","Process/Burn Rate","Moving Rate"]  # 這裡可以更換成想要的行標題名稱
        title_name_basic=["Fire","Firefighter"]  # 這裡可以更換成想要的行標題名稱
        table_widget_basicsetup.setHorizontalHeaderLabels(title_name_basicsetup)
        table_widget_basicsetup.setVerticalHeaderLabels(title_name_basic)  # 設定垂直標題（行名稱）
        layoutBasic.addWidget(table_widget_basicsetup,1)
        table_widget_basicsetup.resizeColumnsToContents()
        #把layout 增加在分頁上面
        self.pageFF.setLayout(layoutBasic)


        #Page : Node Information
        #Node Status table
        layoutNode = QVBoxLayout(self.tab_widget)
        table_widget_Node = QTableWidget()
        table_widget_Node.setRowCount(len(self.inputmatrix))
        table_widget_Node.setColumnCount(len(self.inputmatrix[0]))
        self.tableVisualizeSetting(table_widget_Node)
        #layoutBasic.addWidget(table_widget_Node,5)
        layoutNode.addWidget(table_widget_Node,5)
        title_name=["Status","Amount","Burned/Recovery Percentage",""]  # 這裡可以更換成想要的標題名稱
        table_widget_Node.setHorizontalHeaderLabels(title_name)
        table_widget_Node.resizeColumnsToContents()
        self.pageNode.setLayout(layoutNode)
        self.pageBasicSetup.setLayout(layoutNode)


        #Page : FireFighter Information


        #For Windows setting
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab_widget.currentChanged.connect(self.onTabChanged)
        self.currentIndex = self.tab_widget.currentIndex()

        self.resize(450, 800)

    def onTabChanged(self, index):
        print("分頁index：", index)
        self.pageChanged.emit(index)


    #將node information紀錄至InputMatrix
    # [[isProtected,isBurned,getGrassAmount,getWaterAmount] #node 1 with index 0,[,,,]#node 2 with index 1... [,,,]#node 14 with index 13]
    def calculateInputMatrix(self, nodeList,firefighterList):
        for i in nodeList:
            self.inputmatrix[i.getNum() - 1][0] = i.isProtected()
            self.inputmatrix[i.getNum() - 1][1] = i.isBurned()
            self.inputmatrix[i.getNum() - 1][2] = i.getGrassAmount()
            self.inputmatrix[i.getNum() - 1][3] = i.getWaterAmount()
            for j in firefighterList:
                if(j.isIdle()):
                    self.inputmatrix[j.curPos().getNum() - 1 ][4] = 1
                else:
                    self.inputmatrix[j.curPos().getNum() - 1 ][4] = 0


    #更新OutputMatrix
    def updateOutputMatrix(self, nodeList,firefighterList):
        outputmatrix =[]
        for i in range(0, 15):
            outputmatrix.append(["", "", "", "", ""])

        self.calculateInputMatrix(nodeList,firefighterList)

        #條件判斷的顯示
        #title index=[   0   ,   1    ,            2               ,3]
        #title_name=["Status","Amount","Burned/Recovery Percentage",""]

        for i in nodeList:
            if (self.inputmatrix[i.getNum() - 1][0] == 1): #node is being protected
                outputmatrix[i.getNum() - 1][1] = i.initialWaterAmount - i.getWaterAmount()
                # temp_percent = round((i.initialGrassAmount - i.getGrassAmount()) / i.initialGrassAmount, 4)
                # outputmatrix[i.getNum() - 1][2] = str(temp_percent * 100) + "%"
                outputmatrix[i.getNum() - 1][2] = str(i.getNodePercentage_FF() * 100) + "%"

            elif (self.inputmatrix[i.getNum() - 1][1] == 1):#node is burned
                outputmatrix[i.getNum() - 1][1] = i.getGrassAmount()
                outputmatrix[i.getNum() - 1][2] = str(i.getNodePercentage_Fire() * 100) + "%"

            elif (self.inputmatrix[i.getNum() - 1][1] == 0 and self.inputmatrix[i.getNum() - 1][0] == 0):#node is neither burned or protected
                outputmatrix[i.getNum() - 1][1] = "---"
                outputmatrix[i.getNum() - 1][2] = "0 %"

            if (self.inputmatrix[i.getNum() - 1][0] == 1 and self.inputmatrix[i.getNum() - 1][3] <= 0):
                outputmatrix[i.getNum() - 1][0] = "Save Success"
            elif (self.inputmatrix[i.getNum() - 1][4] == 1):
                outputmatrix[i.getNum() - 1][0] = "Idle"
            elif (self.inputmatrix[i.getNum() - 1][0] == 1 and self.inputmatrix[i.getNum() - 1][3] < i.initialGrassAmount):
                outputmatrix[i.getNum() - 1][0] = "Protecting..."
            elif (self.inputmatrix[i.getNum() - 1][1] == 1 and self.inputmatrix[i.getNum() - 1][2] <= 0):
                outputmatrix[i.getNum() - 1][0] = "Damage"
            elif (self.inputmatrix[i.getNum() - 1][1] == 1 and self.inputmatrix[i.getNum() - 1][2] < i.initialGrassAmount):
                outputmatrix[i.getNum() - 1][0] = "Burning..."
            elif (self.inputmatrix[i.getNum() - 1][1] == 0 and self.inputmatrix[i.getNum() - 1][0] == 0):
                outputmatrix[i.getNum() - 1][0] = "Normal"

        return outputmatrix

    #Information Table的單元格著色、字體設定都在這邊修改
    def tableVisualizeSetting(self,table_widget):
        for i, row in enumerate(self.inputmatrix):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if (value == "Burning..."):
                    item.setBackground(QColor(255, 192, 203))
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                elif (value == "Protecting..."):
                    item.setBackground(QColor("lightgreen"))
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                elif (value == "Save Success"):
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("darkgreen"))
                    item.setForeground(QColor("white"))
                elif (value == "Damage"):
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("darkred"))
                    item.setForeground(QColor("white"))
                elif (value == "Idle"):
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setBackground(QColor("yellow"))

                table_widget.setItem(i, j, item)

    def setSetupMatrix(self,nodeList,firefighterNum,rate_extinguish,move_man,rate_fireburn,move_fire):
        self.setupmatrix[0][0] = len(nodeList) - 1
        self.setupmatrix[0][1] = rate_fireburn
        self.setupmatrix[0][2] = move_fire
        self.setupmatrix[1][0] = firefighterNum
        self.setupmatrix[1][1] = rate_extinguish
        self.setupmatrix[1][2] = move_man

        return self.setupmatrix

    def basicSetuptableVisualizeSetting(self,table_widget_basicsetup,):
        for i, row in enumerate(self.setupmatrix):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table_widget_basicsetup.setItem(i, j, item)





