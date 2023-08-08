import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QTimer
import random 
import json

NODE_NUMBER = 10
NODE_POS = {}
    
class Node(QPushButton):
    def __init__(self, q, b, h, *args):
        super().__init__(*args)
        self.q = q
        self.b = b
        self.h = h
        self.r = q*h

class Burned_Node(Node):
    def __init__(self, node, *args):
        super().__init__(node.q, node.b, node.h, *args)

class Burning_Node(Node):
    def __init__(self, node, *args):
        super().__init__(node.q, node.b, node.h, *args)

class Processing_Node(Node):
    def __init__(self, node, *args):
        super().__init__(node.q, node.b, node.h, *args)

class Processed_Node(Node):
    def __init__(self, node, *args):
        super().__init__(node.q, node.b, node.h, *args)

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
        self.t_text.setFixedWidth(120)
        self.t_text.setStyleSheet("font: 18pt;")
        
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.next_time)
        self.mytimer.start(100)


    def next_time(self):
        self.time += 1
        if self.time > self.T[-1]:
            self.mytimer.stop()
            return
        self.t_text.setText("time = " + str(self.time))

        for i in self.node_btn:
            if type(self.node_btn[i]) is Burning_Node:
                self.node_btn[i].h -= 1
                if self.node_btn[i].h <=0:
                    temp = Burned_Node(self.node_btn[i], self)
                    temp.move(self.node_btn[i].x(), self.node_btn[i].y())
                    temp.setText(self.node_btn[i].text())
                    temp.show()
                    self.node_btn[i].deleteLater
                    self.node_btn[i] = temp
            elif type(self.node_btn[i]) is Processing_Node:
                self.node_btn[i].r -= self.p[1]
                if self.node_btn[i].r <= 0:
                    temp = Processed_Node(self.node_btn[i], self)
                    temp.move(self.node_btn[i].x(), self.node_btn[i].y())
                    temp.setText(self.node_btn[i].text())
                    temp.show()
                    self.node_btn[i].deleteLater
                    self.node_btn[i] = temp


        for i in range(len(self.node_btn)):
            if self.u[(i+1,self.time)] == 1:
                temp = Burning_Node(self.node_btn[i+1], self)
                temp.move(self.node_btn[i+1].x(), self.node_btn[i+1].y())
                temp.setText(self.node_btn[i+1].text())
                temp.show()
                self.node_btn[i+1].deleteLater()
                self.node_btn[i+1] = temp
            for k in self.K:
                if self.u_bar[(i+1, k, self.time)] == 1:
                    temp = Processing_Node(self.node_btn[i+1], self)
                    temp.move(self.node_btn[i+1].x(), self.node_btn[i+1].y())
                    temp.setText(self.node_btn[i+1].text())
                    temp.show()
                    self.node_btn[i+1].deleteLater()
                    self.node_btn[i+1] = temp

        

    def load_from_json(self):
        data = {}
        with open("data.json", 'r') as file:
            data = file.read()
        data = json.loads(data)
        self.N = set(data['N'])
        self.N_D = set(data['N_D'])
        self.N_F = set(data['N_F'])
        self.K = data['K']
        self.A_p = data['A_p']
        self.A_f = data['A_f']
        self.A_p = list([tuple(map(int, i[1:-1].split(','))) for i in data['A_p']])
        self.A_f = list([tuple(map(int, i[1:-1].split(','))) for i in data['A_f']])
        self.x = dict([(tuple(map(int, i[1:-1].split(','))),data['x'][i]) for i in data['x']])
        self.v = dict([(tuple(map(int, i[1:-1].split(','))),data['v'][i]) for i in data['v']])
        self.v_bar = dict([(tuple(map(int, i[1:-1].split(','))),data['v_bar'][i]) for i in data['v_bar']])
        self.u = dict([(tuple(map(int, i[1:-1].split(','))),data['u'][i]) for i in data['u']])
        self.u_bar = dict([(tuple(map(int, i[1:-1].split(','))),data['u_bar'][i]) for i in data['u_bar']])
        self.T = data['T']
        self.q = dict([(int(i), data['q'][i]) for i in data['q']])
        self.b = dict([(int(i), data['b'][i]) for i in data['b']])
        # self.p = data['p']
        self.p = {1:3}
        self.h = dict([(int(i), data['h'][i]) for i in data['h']])
        
        self.NODE_POS = data['NODE_POS']
        # self.node_btn = []
        # for i in self.N:
        #     self.node_btn.append(Node(self.q[i], self.b[i], self.h[i],self))
        #     self.node_btn[i-1].move(self.NODE_POS[str(i)][0], self.NODE_POS[str(i)][1])
        #     self.node_btn[i-1].setText(str(i))
        # for i in self.N_F:
        #     temp = Burning_Node(self)
        #     temp.move(self.node_btn[i-1].x(), self.node_btn[i-1].y())
        #     temp.setText(self.node_btn[i-1].text())
        #     self.node_btn[i-1].deleteLater
        #     self.node_btn[i-1] = temp

        self.node_btn = {}
        for i in self.N-self.N_D:
            print(i)
            self.node_btn[i] =Node(self.q[i], self.b[i], self.h[i],self)
            self.node_btn[i].move(self.NODE_POS[str(i)][0], self.NODE_POS[str(i)][1])
            self.node_btn[i].setText(str(i))

        for i in self.N_D:
            self.node_btn[i] = Node(0, 0, 0, self)
            self.node_btn[i].move(self.NODE_POS[str(i)][0], self.NODE_POS[str(i)][1])
            self.node_btn[i].setText(str(i))

        for i in self.N_F:
            temp = Burning_Node(self.node_btn[i], self)
            temp.move(self.node_btn[i].x(), self.node_btn[i].y())
            temp.setText(self.node_btn[i].text())
            self.node_btn[i].deleteLater
            self.node_btn[i] = temp

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
                 qpainter.drawLine(self.NODE_POS[str(i[0])][0]+15,self.NODE_POS[str(i[0])][1]+15, self.NODE_POS[str(i[1])][0]+25, self.NODE_POS[str(i[1])][1]+25)
        
        qpen.setStyle(Qt.DotLine)
        qpainter.setPen(qpen)
        for i in self.A_f:
            if i[0] < i[1]:
                 qpainter.drawLine(self.NODE_POS[str(i[0])][0]+10,self.NODE_POS[str(i[0])][1]+10, self.NODE_POS[str(i[1])][0]+20, self.NODE_POS[str(i[1])][1]+20)

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