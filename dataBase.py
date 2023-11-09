from PyQt5.QtCore import pyqtSignal, QObject


class DataBase(QObject):
    dataUpdateSignal = pyqtSignal(str)

    P = {1:3,2:4} #各個消防單位時間處理的燃料量

    NODE_POS = {}
    N=[]
    N_D=[]
    N_F=[]
    K = set() #K=消防員集合
    A_p = []
    A_f = []
    tau = [] #travel time set
    lamb = [] #spread time set
    T = [] #時間list
    Q = {} #quantity
    b = {} #value
    process = {} #processing time
    H = {} #burning time
    x = {}
    w = {}
    u = {}
    u_bar = {}
    v = {}
    v_bar = {}

    def __init__(self):
        super().__init__()
        from controller import FFNum
        self.numFF = FFNum
        self.ffPosSta = []
        self.ffPosSta = self.initffPosStaList()
        '''------------------------------Methods-----------------------------------'''
    def initffPosStaList(self):
        temp = []
        for i in range(self.numFF):
            temp.append([[],[]])
        return temp




















