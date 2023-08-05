import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF

from controller import xPositionList, yPositionList


class PaintTool(QWidget):
    def paintEvent(self, event,nodeList):
        qpainter = QPainter()
        qpainter.begin(self)
        qpen = QPen(Qt.black, 2, Qt.SolidLine)
        qpainter.setPen(qpen)

        for i in nodeList:
            for j in i.getNeighbors():
                qpainter.drawLine(QPointF(xPositionList[i.getNum()], yPositionList[i.getNum()]),
                                  QPointF(xPositionList[j.getNum()], yPositionList[j.getNum()]))
                i.getXposition() + i.width() / 2

        qpen.setColor(Qt.red)
        qpainter.setPen(qpen)

        for i in nodeList:
            if (i.isBurned()):
                for j in i.getNeighbors():
                    tempXpercent = (xPositionList[j.getNum()] - xPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)
                    tempYpercent = (yPositionList[j.getNum()] - yPositionList[i.getNum()]) * i.getArcPercentage_Fire(j)

                    qpen.setColor(Qt.red)
                    qpen.setWidth(4)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(xPositionList[i.getNum()], yPositionList[i.getNum()]),
                                      QPointF(xPositionList[i.getNum()] + tempXpercent,
                                              yPositionList[i.getNum()] + tempYpercent))

        for i in nodeList:
            if (i.isProtected()):
                for j in i.getNeighbors():
                    tempXpercent = (xPositionList[j.getNum()] - xPositionList[i.getNum()]) * i.getArcPercentage_FF(j)
                    tempYpercent = (yPositionList[j.getNum()] - yPositionList[i.getNum()]) * i.getArcPercentage_FF(j)

                    qpen.setColor(Qt.darkGreen)
                    qpen.setWidth(4)
                    qpainter.setPen(qpen)
                    qpainter.drawLine(QPointF(xPositionList[i.getNum()], yPositionList[i.getNum()]),
                                      QPointF(xPositionList[i.getNum()] + tempXpercent,
                                              yPositionList[i.getNum()] + tempYpercent))

        self.update()
        qpainter.end()
