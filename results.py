from PyQt5.QtWidgets import QLabel
from PyQt5 import QtWidgets


class resultsWindow(QtWidgets.QMainWindow):

    def __init__(self, nodes, t):
        super().__init__()
        self.resize(800,600)
        self.nodeLabel = QLabel(self)
        text = "protected: \n"
        value = 0
        ctr = 1
        for i in nodes:
            if(i.isBurned()):
                text += ""
            else:
                if(ctr % 3 == 0):
                    text += "\n"
                value += i.getValue()
                text += "node {}, ".format(i.getNum())
                ctr+=1
        self.nodeLabel.setGeometry(50,150,300,300)
        self.nodeLabel.setText(text)

        self.valueLabel = QLabel(self)
        self.valueLabel.setGeometry(400, 150, 200, 100)
        self.valueLabel.setText("protected value: {}".format(value))

        self.timeLabel = QLabel(self)
        self.timeLabel.setGeometry(400, 250, 200, 100)
        self.timeLabel.setText("finish time: {}".format(t))