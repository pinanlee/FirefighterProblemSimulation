import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import random 
import json

NODE_NUMBER = 10
NODE_POS = {}
    
class Node(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)

class Deactivated_Node(Node):
    def __init__(self, *args):
        super().__init__(*args)

class MyWidget(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.initUI()
        if (mode == "rand_gen"):
            self.random_generate()
        elif (mode == 'load_json'):
            self.load_from_json()

        self.time = 0
        t_plus = QPushButton(self)
        t_plus.setText('next time step')
        t_plus.move(10,850)
        t_plus.clicked.connect(self.next_time)
        self.t_text = QLabel(self)
        self.t_text.setText("time = " + str(self.time))
        self.t_text.setFixedWidth(70)
        
    def next_time(self):
        self.time += 1
        self.t_text.setText("time = " + str(self.time))
        

    def load_from_json(self):
        data = {}
        with open("data.json", 'r') as file:
            data = file.read()
        data = json.loads(data)
        self.N = data['N']
        self.N_D = data['N_D']
        self.N_F = data['N_F']
        self.A_p = data['A_p']
        self.A_f = data['A_f']
        self.A_p = list([tuple(map(int, i[1:-1].split(','))) for i in data['A_p']])
        self.A_f = list([tuple(map(int, i[1:-1].split(','))) for i in data['A_f']])
        
        
        
        self.NODE_POS = data['NODE_POS']
        node_btn = []
        for i in self.N:
            node_btn.append(Node(self))
            node_btn[i-1].move(self.NODE_POS[str(i)][0], self.NODE_POS[str(i)][1])
            node_btn[i-1].setText(str(i))


    def random_generate(self):
        node_btn = []
        for i in range(NODE_NUMBER):
            NODE_POS[i] = (random.randint(25, 1415), random.randint(25, 875))
            node_btn.append(Node(self))
            node_btn[i].move(NODE_POS[i][0], NODE_POS[i][1])
            node_btn[i].setText(str(i))
        
    def initUI(self):
        self.setWindowTitle('my window')
        self.setGeometry(50, 50, 200, 150)

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
 
        qpen = QPen(Qt.black, 2, Qt.SolidLine)
        qpainter.setPen(qpen)
        # qpainter.drawLine(20, 40, 180, 40)

        # qpen.setStyle(Qt.DashLine)
        # qpainter.setPen(qpen)
        # qpainter.drawLine(20, 60, 180, 60)

        # qpen.setStyle(Qt.DashDotLine)
        # qpainter.setPen(qpen)
        # qpainter.drawLine(20, 80, 180, 80)

        # qpen.setStyle(Qt.DashDotDotLine)
        # qpainter.setPen(qpen)
        # qpainter.drawLine(20, 100, 180, 100)

        for i in self.A_p:
            if i[0] < i[1]:
                 qpainter.drawLine(self.NODE_POS[str(i[0])][0]+25,self.NODE_POS[str(i[0])][1]+25, self.NODE_POS[str(i[1])][0]+25, self.NODE_POS[str(i[1])][1]+25)
        
        qpen.setStyle(Qt.DotLine)
        qpainter.setPen(qpen)
        for i in self.A_f:
            if i[0] < i[1]:
                 qpainter.drawLine(self.NODE_POS[str(i[0])][0]+20,self.NODE_POS[str(i[0])][1]+20, self.NODE_POS[str(i[1])][0]+20, self.NODE_POS[str(i[1])][1]+20)

        qpainter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # w = MyWidget("rand_gen")
    w = MyWidget("load_json")
    w.resize(1440,900)
    
    # label = QLabel(w)
    # label.setText("Behold the Guru, Guru99")
    # label.move(100,130)
    # label.show()
    
    # t_plus = Deactivated_Node(w)
    # t_plus.setText('next time step')
    # t_plus.move(10,850)
    # t_plus.show()

    with open("./stylesheet.qss") as f:
        qss = f.read()
        
    app.setStyleSheet(qss)
    # app.setStyleSheet("")
    
    w.show()
    
    sys.exit(app.exec_())