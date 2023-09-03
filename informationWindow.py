import math

from PyQt5.QtCore import pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QFont, QPixmap, QRegion
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QSizePolicy, QTabWidget, QLabel, \
    QHBoxLayout, QPushButton, QGraphicsOpacityEffect
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
        self.ffblockCP_img1 =QPixmap("image/firefighter.png")
        self.ffblockCP_sta1 = ""
        self.ffblockCP_name1 = ""
        self.ffblockCP_wr1 = ""
        self.ffblockCP_img2 = QPixmap("image/firefighter.png")
        self.ffblockCP_sta2 = ""
        self.ffblockCP_name2 = ""
        self.ffblockCP_wr2 = ""
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
        title_name = ["Status", "Water Percentage", "Burned Percentage", "Time to burned"]  # 這裡可以更換成想要的標題名稱
        self.table_widget_Node.setHorizontalHeaderLabels(title_name)
        self.table_widget_Node.resizeColumnsToContents()
        self.pageNode.setLayout(self.pageNode.layout)


    def updateFFUI(self):
        #self.table_widget_Node.setRowCount(self.database.numNode)
        self.clear_layout(self.pageFF.layout)
        blockFF = self.pageFF_generateblockFF()
        self.pageFF.layout.addWidget(blockFF)
        self.pageFF.setLayout(self.pageFF.layout)


    '''------------------------------Information Window  UI settings-----------------------------------'''
    def ui(self): #用於Information Window ui的手動設計
        #增加分頁物件
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabPosition(QTabWidget.East)

        #增加分頁
        self.pageControlPanel = QWidget()
        self.pageNode = QWidget()
        self.pageFF = QWidget()
        self.tab_widget.addTab(self.pageControlPanel, "ControlPanel")
        self.tab_widget.addTab(self.pageNode, "Node Info")
        self.tab_widget.addTab(self.pageFF, "FireFighter Info")

        #Page : Control panel
        self.pageControlPanel.layout = QVBoxLayout()
        #Control panel-node區塊
        self.nodeBlock = QWidget()
        self.nodeBlock.setStyleSheet("background-color: lightgrey;")
        self.nodeBlock.setFixedSize(400, 200)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)  # 設定為加粗

        self.nodeblock_textnode = ""
        self.nodeblock_textlen = ""
        self.nodeblock_texttta = ""
        self.nodeblock_textttb = ""
        self.nodeblock_textsta = ""


        self.nodeCircle = QWidget(self.nodeBlock)
        self.nodeCircle.setGeometry(15, 45, 100, 100)  # 設定容器的位置和大小
        self.nodeCircle.setStyleSheet("background-color: white;")
        circle_region = QRegion(self.nodeCircle.rect(), QRegion.Ellipse)
        self.nodeCircle.setMask(circle_region)
        self.title_label_sta_des = QLabel(self.nodeblock_textsta, self.nodeBlock)
        self.title_label_sta_des.setFont(font)
        self.title_label_sta_des.setGeometry(40, 155, 200, 20)


        self.title_label_node = QLabel("Node\t:", self.nodeBlock)
        self.title_label_node.setFont(font)
        self.title_label_node.setGeometry(135, 45, 200, 20)
        self.title_label_node_des = QLabel(self.nodeblock_textnode, self.nodeBlock)
        self.title_label_node_des.setFont(font)
        self.title_label_node_des.setGeometry(220, 45, 200, 20)

        self.title_label_length = QLabel("Length\t:", self.nodeBlock)
        self.title_label_length.setFont(font)
        self.title_label_length.setGeometry(135, 75, 200, 20)  # 設定容器的位置和大小
        self.title_label_length_des = QLabel(self.nodeblock_textlen, self.nodeBlock)
        self.title_label_length_des.setFont(font)
        self.title_label_length_des.setGeometry(220, 75, 200, 20)

        self.title_label_tta = QLabel("Time to arrive\t:", self.nodeBlock)
        self.title_label_tta.setFont(font)
        self.title_label_tta.setGeometry(135, 105, 200, 20)  # 設定容器的位置和大小
        self.title_label_tta_des = QLabel(self.nodeblock_texttta, self.nodeBlock)
        self.title_label_tta_des.setFont(font)
        self.title_label_tta_des.setGeometry(300, 105, 200, 20)

        self.title_label_ttb = QLabel("Time to burned\t:", self.nodeBlock)
        self.title_label_ttb.setFont(font)
        self.title_label_ttb.setGeometry(135, 135, 200, 20)  # 設定容器的位置和大小
        self.title_label_ttb_des = QLabel(self.nodeblock_textttb, self.nodeBlock)
        self.title_label_ttb_des.setFont(font)
        self.title_label_ttb_des.setGeometry(300, 135, 200, 20)


        self.pageControlPanel.layout.addWidget(self.nodeBlock)

        self.blockffContainerCP = QWidget()
        self.blockffContainerCP_layout = QVBoxLayout(self.blockffContainerCP)
        self.pageCP_generateblockFF()
        self.pageControlPanel.layout.addWidget(self.blockffContainerCP)


        self.pageControlPanel.setLayout(self.pageControlPanel.layout)


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
        elif (value == "Idle"):
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
        elif (value == "Traveling"):
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QColor("grey"))
            item.setForeground(QColor("white"))

        return item
    '''------------------------------page: Control Panel-----------------------------------'''
    def pageCP_blockFF(self,num):
        if(num == 1):
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)

            blockff = QWidget(self.blockffContainerCP)
            #pixmap = QPixmap(self.ffblockCP_img1)
            pixmap = self.ffblockCP_img1
            pixmap = pixmap.scaledToWidth(100)  # Adjust width as needed
            title_label_img = QLabel(blockff)
            title_label_img.setPixmap(pixmap)
            title_label_img.setGeometry(0, 0, 200, 200)

            title_label_sta_des = QLabel(self.ffblockCP_sta1, blockff)
            font.setPointSize(14)
            title_label_sta_des.setFont(font)
            font.setPointSize(12)
            title_label_sta_des.setGeometry(150, 55, 250, 20)

            title_label_name = QLabel("Name\t:", blockff)
            title_label_name.setFont(font)
            title_label_name.setGeometry(150, 85, 100, 20)
            title_label_name_des = QLabel(self.ffblockCP_name1, blockff)
            title_label_name_des.setFont(font)
            title_label_name_des.setGeometry(250, 85, 100, 20)

            title_label_wr = QLabel("Water Rate\t:", blockff)
            title_label_wr.setFont(font)
            title_label_wr.setGeometry(150, 115, 100, 20)
            title_label_wr_des = QLabel(self.ffblockCP_wr1, blockff)
            title_label_wr_des.setFont(font)
            title_label_wr_des.setGeometry(300, 115, 100, 20)
        if (num == 2):
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)

            blockff = QWidget(self.blockffContainerCP)
            #pixmap = QPixmap(self.ffblockCP_img2)
            pixmap = self.ffblockCP_img2

            pixmap = pixmap.scaledToWidth(100)  # Adjust width as needed
            title_label_img = QLabel(blockff)
            title_label_img.setPixmap(pixmap)
            title_label_img.setGeometry(0, 0, 200, 200)
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.3)
            title_label_img.setGraphicsEffect(opacity_effect)

            title_label_sta_des = QLabel(self.ffblockCP_sta2, blockff)
            title_label_sta_des.setGeometry(150, 55, 250, 20)

            title_label_name = QLabel("Name\t:", blockff)
            title_label_name.setFont(font)
            title_label_name.setGeometry(150, 85, 100, 20)
            title_label_name_des = QLabel(self.ffblockCP_name2, blockff)
            title_label_name_des.setGeometry(300, 85, 100, 20)

            title_label_wr = QLabel("Water Rate\t:", blockff)
            title_label_wr.setFont(font)
            title_label_wr.setGeometry(150, 115, 100, 20)
            title_label_wr_des = QLabel(self.ffblockCP_wr2, blockff)
            title_label_wr_des.setGeometry(300, 115, 100, 20)

        return blockff

    def pageCP_generateblockFF(self):
        self.clear_layout(self.blockffContainerCP_layout)
        block1 = self.pageCP_blockFF(1)
        block2 = self.pageCP_blockFF(2)

        self.blockffContainerCP_layout.addWidget(block1)
        self.blockffContainerCP_layout.addWidget(block2)



    '''------------------------------page: Node Information-----------------------------------'''
    def updatenodeInfo(self):
        for row in range(1,21):
            for col in range(0,4):
                if col == 0:
                    print(f'currenttime{self.currentTime}row{row}')
                    value  = self.database.getffNDictInfo(self.currentTime,row,"status")
                    #item = QTableWidgetItem(value)
                    item = self.tableVisualizeSetting(value)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                elif col == 1:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"FFPercentage")
                    value = (1-value) *100
                    item = QTableWidgetItem(str(value)+ "%")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                elif col == 2:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"firePercentage")
                    value = (1-value) *100
                    item = QTableWidgetItem(str(value)+ "%")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()
                elif col == 3:
                    value  = self.database.getffNDictInfo(self.currentTime,row,"burntime")
                    item = QTableWidgetItem(str(value))
                    self.table_widget_Node.setItem(row-1, col, item)
                    self.table_widget_Node.resizeColumnsToContents()

    '''------------------------------page: Firefighter Information------------------------------------'''
    #step 1
    def pageFF_blockFF(self, currentTime, image_path, image_description, status):
        blockff = QWidget()
        layout = QHBoxLayout(blockff) #全部區塊
        vertical_layout = QVBoxLayout() #左半邊
        #pixmap = QPixmap(image_path)
        pixmap = image_path
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
                    #item = QTableWidgetItem(str(self.outputStatus[col]))
                    item = self.tableVisualizeSetting(str(self.outputStatus[col]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.table_widget.setItem(row, col, item)
                    self.table_widget.resizeColumnsToContents()

    #step 4
    def pageFF_generateblockFF(self):
        blockffContainer = QWidget()
        self.blockffContainer_layout = QVBoxLayout(blockffContainer)
        for time,node in self.ffDict.items():
            currentTime = time
            for node_id,info in node.items():
                image_path = info["image"]
                image_description = str(info["num"])
                status = info["status"]
                if (currentTime == self.currentTime):
                    block = self.pageFF_blockFF(currentTime, image_path, image_description, status)
                    self.blockffContainer_layout.addWidget(block)
        return blockffContainer



