import math

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QSizePolicy, QTabWidget, QLabel, \
    QHBoxLayout, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class InformationWindow(QtWidgets.QMainWindow):
    pageChanged = pyqtSignal(int)

    def __init__(self,database):
        super().__init__()
        self.setWindowTitle('Information Window')
        self.currentIndex = 0
        self.currentTime = 0
        self.numFF = 0
        self.numNode = 0
        self.database = database
        self.database.dataUpdateSignal.connect(self.updateInfo)
        self.ffDict = self.database.ffDict_info
        self.ffPosSta = self.database.ffPosSta
        #self.nodeDict = self.database.ffNDict_info
        self.ui()

    '''------------------------------Next time-----------------------------------'''
    def updateInfo(self):
        self.currentTime = self.database.currentTime
        self.ffDict = self.database.ffDict_info
        self.ffPosSta = self.database.ffPosSta
        self.onTabChanged(self.currentIndex)

    def updateNodeUI(self):
        self.clear_layout(self.pageNode.layout)
        self.table_widget_Node = QTableWidget()
        self.table_widget_Node.setRowCount(self.database.numNode)
        self.table_widget_Node.setColumnCount(4)
        self.pageNode.layout.addWidget(self.table_widget_Node)
        title_name = ["Status", "Grass Amount", "Water Amount", "Time to burned"]  # 這裡可以更換成想要的標題名稱
        self.table_widget_Node.setHorizontalHeaderLabels(title_name)
        self.table_widget_Node.resizeColumnsToContents()
        self.pageNode.setLayout(self.pageNode.layout)


    def updateFFUI(self):
        #self.table_widget_Node.setRowCount(self.database.numNode)
        self.clear_layout(self.pageFF.layout)
        blockFF = self.generateblockFF()
        self.pageFF.layout.addWidget(blockFF)
        self.pageFF.setLayout(self.pageFF.layout)


    '''------------------------------Information Window  UI settings-----------------------------------'''
    def ui(self): #用於Information Window ui的手動設計
        #增加分頁物件
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabPosition(QTabWidget.East)

        #增加分頁
        self.pageBasicSetup = QWidget()
        self.pageNode = QWidget()
        self.pageFF = QWidget()
        self.tab_widget.addTab(self.pageBasicSetup, "Basic Setup")
        self.tab_widget.addTab(self.pageNode, "Node Info")
        self.tab_widget.addTab(self.pageFF, "FireFighter Info")

        #Page : Basic Setup
        #Basic Setup table
        # layoutBasic = QVBoxLayout(self.tab_widget)
        # table_widget_basicsetup = QTableWidget()
        # table_widget_basicsetup.setRowCount(3)
        # table_widget_basicsetup.setColumnCount(3)
        # title_name_basicsetup=["Number","Process/Burn Rate","Moving Rate"]  # 這裡可以更換成想要的行標題名稱
        # title_name_basic=["Node","Fire","Firefighter"]  # 這裡可以更換成想要的行標題名稱
        # table_widget_basicsetup.setHorizontalHeaderLabels(title_name_basicsetup)
        # table_widget_basicsetup.setVerticalHeaderLabels(title_name_basic)  # 設定垂直標題（行名稱）
        # layoutBasic.addWidget(table_widget_basicsetup,1)
        # table_widget_basicsetup.resizeColumnsToContents()
        # #把layout 增加在分頁上面
        # self.pageBasicSetup.setLayout(layoutBasic)


        #Page : Node Information
        #Node Status table
        self.pageNode.layout = QVBoxLayout()

        #Page : FireFighter Information
        self.pageFF.layout = QVBoxLayout()

        #For Windows setting
        self.tab_widget.currentChanged.connect(self.onTabChanged)
        self.setStyleSheet("""
                    QTabBar::tab:selected {
                        background-color: rgb(195, 205, 211);
                        border-radius: 6px;
                    }
                    QTabBar::tab:!selected {
                        background-color: white;
                        text-align: center;
                    }
                    QTabBar::tab:hover {
                        background-color: rgb(195, 205, 211);
                        border-radius: 6px;

                    }
                    # QTabBar::tab {
                    #     font-weight: bold;
                    # }
                    
                """)
        self.currentIndex = self.tab_widget.currentIndex()
        self.setGeometry(1345,150,450,786)
        self.setFixedSize(450, 786)
        self.setWindowFlags(Qt.WindowCloseButtonHint)



    '''------------------------------Methods-----------------------------------'''
    #切換分頁時傳遞分頁index至mainwindow class，防止分頁自動跳到default值用
    def onTabChanged(self, index):
        self.currentIndex = index
        if (self.currentIndex == 1):
            self.updateNodeUI()
            self.updatenodeInfo()
            self.clear_layout(self.pageFF.layout)
        elif (self.currentIndex == 2):
            self.updateFFUI()
            self.clear_layout(self.pageNode.layout)


    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
    def tableVisualizeSetting(self,value):
        item = QTableWidgetItem(str(value))
        if (value == "Burned"):
            item.setBackground(QColor(255, 192, 203))
            font = QFont()
            font.setBold(True)
            item.setFont(font)
        elif (value == "Protected"):
            item.setBackground(QColor("lightgreen"))
            font = QFont()
            font.setBold(True)
            item.setFont(font)
        elif (value == "Safe"):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("darkgreen"))
            item.setForeground(QColor("white"))
        elif (value == "Damaged"):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("darkred"))
            item.setForeground(QColor("white"))
        elif (value == "FFidle"):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("yellow"))
        elif (value == "Depot"):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("black"))
            item.setForeground(QColor("white"))

        return item
    '''------------------------------page: BasicSetup-----------------------------------'''

    '''------------------------------page: Node Information-----------------------------------'''
    def updatenodeInfo(self):
        for row in range(1,21):
            for col in range(0,4):
                if col == 0:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"status")
                    #item = QTableWidgetItem(value)
                    item = self.tableVisualizeSetting(value)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                elif col == 1:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"firePercentage")
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                elif col == 2:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"FFPercentage")
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                # elif col == 3:
                #     value  = self.database.getffNDictInfo(self.currentTime,row,"status")
                #     item = QTableWidgetItem(value)
                #     self.table_widget_Node.setItem(row-1, col, item)
                #     self.table_widget_Node.resizeColumnsToContents()

    '''------------------------------page: Firefighter Information------------------------------------'''
    #step 1
    def blockFF(self, currentTime, image_path, image_description,status):
        blockff = QWidget()
        layout = QHBoxLayout(blockff) #全部區塊
        vertical_layout = QVBoxLayout() #左半邊
        pixmap = QPixmap(image_path)
        self.image_label = QLabel()
        self.image_label.setPixmap(pixmap)
        vertical_layout.addWidget(self.image_label)
        self.description_label = QLabel("Firefighter  " + image_description)
        font = self.description_label.font()
        font.setBold(True)  # 设置字体为加粗
        self.description_label.setFont(font)
        self.description_label.setAlignment(Qt.AlignCenter)
        vertical_layout.addWidget(self.description_label)
        self.status_label = QLabel(status)
        font = self.status_label.font()
        font.setBold(True)  # 设置字体为加粗
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignCenter)
        vertical_layout.addWidget(self.status_label)
        layout.addLayout(vertical_layout) #左半邊完成
        time = currentTime

        self.table_widget = QTableWidget(self)
        self.title_name_FF = ["Node", "Status"]
        self.table_widget.setRowCount(len(self.title_name_FF))
        self.table_widget.setColumnCount(self.currentTime)
        self.table_widget.setVerticalHeaderLabels(self.title_name_FF)
        # self.table_widget.horizontalScrollBar().setValue(self.table_widget.horizontalScrollBar().maximum())

        layout.addWidget(self.table_widget)#右半邊完成

        self.chooseBlockData(image_description)#右半邊資料傳入
        self.uploadBlockData()
        self.table_widget.horizontalScrollBar().setValue(self.table_widget.horizontalScrollBar().maximum()-2)

        return blockff #step1

    #step 2
    def chooseBlockData(self,image_description):
        self.outputNode = []
        self.outputStatus = ""

        for i in range(self.numFF):
            if (image_description == str(i + 1)):
                self.outputNode = self.ffPosSta[int(image_description) - 1][0]
                self.outputStatus = self.ffPosSta[int(image_description) - 1][1]

    #step 3
    def uploadBlockData(self):
        for row in range(self.numFF):
            for col in range(self.currentTime):
                if row == 0:
                    item = QTableWidgetItem(str(self.outputNode[col]))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget.setItem(row, col, item)
                elif row == 1:
                    item = QTableWidgetItem(str(self.outputStatus[col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget.setItem(row, col, item)
                    self.table_widget.resizeColumnsToContents()

    #step 4
    def generateblockFF(self):
        blockffContainer = QWidget()
        self.blockffContainer_layout = QVBoxLayout(blockffContainer)
        for time,node in self.ffDict.items():
            currentTime = time
            for node_id,info in node.items():
                image_path = info["image"]
                image_description = str(info["num"])
                status = info["status"]
                if (currentTime == self.currentTime):
                    block = self.blockFF(currentTime, image_path, image_description, status)
                    self.blockffContainer_layout.addWidget(block)
        return blockffContainer



