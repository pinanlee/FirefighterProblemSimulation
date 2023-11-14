from PyQt5.QtWidgets import  QLabel, QSizePolicy, QWidget, QGraphicsOpacityEffect, QPushButton,QStyle, QStyleOption
from PyQt5.QtGui import QFont, QPixmap, QCursor,QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from controllerUtils import flashTimer


class gameWindow(QWidget):
    def __init__(self, widget, ff) -> None:
        super().__init__(widget)
        self.widget = widget
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.ff = ff
        self.setObjectName(f'{ff.getNum()}')
        self.setFixedSize(240,115)


        self.setStyleSheet(
            "QWidget {"
            "   border: 2px solid ;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "}"
        )
        self.raise_()
        pixmap = QPixmap(ff.pixmaploc)
        self.title_label_img = QLabel(self)
        self.title_label_img.setGeometry(10, 10, 85,100)

        self.title_label_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.title_label_img.setStyleSheet(
            "QLabel {"
            "   border: 2px solid #0078d7;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "}"
        )
        scaled_pixmap = pixmap.scaled(self.title_label_img.width(), self.title_label_img.height())
        self.title_label_img.setPixmap(scaled_pixmap)

        self.title_label_name_des = QLabel(ff.getName(), self)
        setattr(self, "flash_timer", flashTimer(self))
                
        self.title_label_name_des.setFont(font)
        self.title_label_name_des.setGeometry(100, 75, 140, 30)
        temp = str(ff.getStatus())
        self.title_label_ready_des = QLabel(temp, self)
        self.title_label_ready_des.setFont(font)
        self.title_label_ready_des.setGeometry(100, 25, 120, 35)

    
    def activate(self):
        self.flash_timer.start()
    
    def setStatus(self, status):
        self.title_label_ready_des.setText(status)
        if status != "Not ready":
            self.title_label_ready_des.setStyleSheet("background-color: lightgreen;")
        else:
            self.title_label_ready_des.setStyleSheet("")
    
    def setOpacity(self, opacity):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        self.title_label_img.setGraphicsEffect(opacity_effect)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.block_complete = blockFFComplete(self.widget, self.objectName, self.ff)
        self.block_complete.raise_()
        self.block_complete.show()
        self.block_complete.setGeometry(270,250,240,400)        

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet(
            "QWidget {"
            "   border: 2px solid #FF4778 ;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "}"
        )
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setStyleSheet(
            "QWidget {"
            "   border: 2px solid  ;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "}"
        )
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

class blockFFComplete(QWidget):
    def __init__(self, widget, num, ff):
        super().__init__(widget)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)

        self.setObjectName(f'{num}')
        self.setFixedSize(280,380)
        self.setStyleSheet(
            "QWidget {"
            "   border: 2px solid ;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "background-color: white;"
            "}"
        )

        button_delete = QPushButton("Close",self)
        button_delete.setGeometry(180, 10, 50, 25)
        button_delete.clicked.connect(self.delete_self)


        pixmap = ff.grab()
        title_label_img = QLabel(self)
        title_label_img.setGeometry(10, 10, 85,100)

        title_label_img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        title_label_img.setStyleSheet(
            "QLabel {"
            "   border: 2px solid #0078d7;"  
            "   border-radius: 10px;"  
            "   padding: 5px;"  
            "}"
        )
        scaled_pixmap = pixmap.scaled(title_label_img.width(), title_label_img.height())
        title_label_img.setPixmap(scaled_pixmap)
        title_label_name = QLabel("Name\t:", self)
        title_label_name.setFont(font)
        title_label_name.setGeometry(0, 115, 80, 30)
        title_label_name_des = QLabel(ff.getName(), self)
        title_label_name_des.setFont(font)
        title_label_name_des.setGeometry(0, 155, 140, 30)

        title_label_wr = QLabel("Water Rate\t:", self)
        title_label_wr.setFont(font)
        title_label_wr.setGeometry(0, 205, 120, 30)
        temp = str(ff.rate_extinguish)
        title_label_wr_des = QLabel(temp, self)
        title_label_wr_des.setFont(font)
        title_label_wr_des.setGeometry(0, 245, 150, 30)
        
    def delete_self(self):
            self.close()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)