'''
這個class應該要包含以下功能性:
1.存檔: 收錄每一刻t的浮動資料至dictionary (完成)
2.讀檔: 整理成各自class指定格式---for each classes where needs data (待研究)
3.易取得: 取得每一刻t的浮動資料 (完成)
4.格式化: 整理成list格式---for InformationWindow class
5.資料處理: 可以對現有資料進行sorting功能，並以function方式提供給other class
'''
from PyQt5.QtCore import pyqtSignal, QObject


class DataBase(QObject):
    dataUpdateSignal = pyqtSignal(str)

    P = {1:3,2:4} #各個消防單位時間處理的燃料量
    epsilon = 1e-4
    X={}
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

    w = {}
    u = {}
    u_bar = {}
    v = {}
    v_bar = {}



    def __init__(self):
        super().__init__()
        from controller import FFNum

        self.numFF = FFNum
        self.currentTime = 0
        self.fireNetworkNodeList = self.initList() #fireNetwork 後續簡稱fiN
        self.ffnetworkNodeList = self.initList()   #ffnetwork後續簡稱ffN
        self.controllerNodeList = self.initList()#controllerNodeList後續簡稱cN
        self.firefighterList = self.initList()
        self.fiNDict = {}
        self.ffNDict = {}
        self.cNDict = {}
        self.ffDict = {}
        self.fiNDict_info = {}
        self.ffNDict_info = {}
        self.cNDict_info = {}
        self.ffDict_info = {} # dict for information window
        self.ffPosSta = []
        self.ffPosSta = self.initffPosStaList()
        self.numNode = 20
        self.infoNextTime()
        '''------------------------------Methods-----------------------------------'''
    def initList(self): #initial list,要求T數量空間(目前設定為50,index starts from 0),後續可以跟據T時間調整
        temp = []
        for i in range(150):
            temp.append([])
        return temp

    def initffPosStaList(self):
        temp = []
        for i in range(self.numFF):
            temp.append([[],[]])
        return temp

    def getfiNNodeInfo(self,time,num,key):
        if (time > self.currentTime):
            return f'No time {time} data'
        elif  num > self.numNode or num <=0 :
            return f'Node {num} not exist'
        return self.fiNDict[time][num][key]

    def getffNNodeInfo(self,time,num,key):
        if (time > self.currentTime):
            return f'No time {time} data'
        elif  num > self.numNode or num <=0 :
            return f'Node {num} not exist'
        return self.ffNDict[time][num][key]

    def getcNNodeInfo(self,time,num,key):
        if (time > self.currentTime):
            return f'No time {time} data'
        elif  num > self.numNode or num <=0 :
            return f'Node {num} not exist'
        return self.cNDict[time][num][key]

    def getffNDictInfo(self,time,num,key):
        if (time > self.currentTime or time < 0 ):
            return f'No time {time} data'
        elif  num > self.numNode or num <=0 :
            return f'Node {num} not exist'
        return self.ffNDict_info[time][num][key]



    '''------------------------------Next Time-----------------------------------'''
    def infoNextTime(self): #用於mainWindow nexttime的同步更新
        # self.ffPosSta = self.initffPosStaList()
        def updateDict_node(list):
            dict_main = {}
            dict_time = {}
            dict_main_info = {}  # {"obj","num","pos","image","status"}
            dict_time_info = {}
            for i in range(self.currentTime + 1):
                for j in list[i]:
                    dict_Node = {"obj":j,
                                 "num": j.getNum(),
                                 "arc": 0,
                                 "protect":j.isProtected(),
                                 "burn":j.isBurned(),
                                 "water": j.getWaterAmount(),
                                 "grass": j.getGrassAmount()  ,
                                 "firePercentage": j.getNodePercentage_Fire(),
                                 "FFPercentage": j.getNodePercentage_FF(),
                                 "idle": j.isIdle(),
                                 "burntime": j.fireMinArrivalTime}
                    dict_time[j.getNum()] = dict_Node
                    if (dict_Node["protect"] == True and dict_Node["water"] > 0 ):
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Protected",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                    elif(dict_Node["idle"] == True):
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Idle",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                    elif (dict_Node["protect"] == True and dict_Node["water"] <= 0 ):
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Safe",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                    elif (dict_Node["burn"] == True and dict_Node["grass"] > 0 ):
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Burned",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                    elif (dict_Node["burn"] == True and dict_Node["grass"] <= 0):
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Damaged",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                    else:
                        dict_Node_info = {"obj": j,
                                          "num": j.getNum(),
                                          "firePercentage": j.getNodePercentage_Fire(),
                                          "FFPercentage": j.getNodePercentage_FF(),
                                          "status": "Normal",
                                          "water": j.getWaterAmount(),
                                          "burntime": j.fireMinArrivalTime
                                          }
                        dict_time_info[j.getNum()] = dict_Node_info
                dict_main[i] = dict_time
                dict_main_info[i] = dict_time_info
            return dict_main,dict_main_info
        self.fiNDict,self.fiNDict_info = updateDict_node(self.fireNetworkNodeList)
        self.ffNDict,self.ffNDict_info = updateDict_node(self.ffnetworkNodeList)
        #self.cNDict,self.cNDict_info = updateDict_node(self.controllerNodeList)


        def updateDict_FF(list):
            dict_main = {} #{"obj","num","pos","image","process","travel","idle"}
            dict_time = {}
            dict_main_info = {}#{"obj","num","pos","image","status"}
            dict_time_info = {}

            for i in range(self.currentTime + 1):
                for j in list[i]:
                    dict_Node = {"obj":j,"num": j.num,"pos":j.curPos().getNum(),"image":j.grab(),"process":j.isProcess(),"travel":j.isTraveling(),"idle":j.isIdle()}
                    dict_time[j.num] = dict_Node
                    if (dict_Node["process"] == True):
                        dict_Node_info = {"obj": j, "num": j.num, "pos": j.curPos().getNum(), "image": j.grab(),"status": "processing"}
                        dict_time_info[j.num] = dict_Node_info
                    elif (dict_Node["travel"] == True):
                        dict_Node_info = {"obj": j, "num": j.num, "pos": j.curPos().getNum(), "image": j.grab(),"status": "travelling"}
                        dict_time_info[j.num] = dict_Node_info
                    else:
                        dict_Node_info = {"obj": j, "num": j.num, "pos": j.curPos().getNum(), "image": j.grab(),"status": "Idel"}
                        dict_time_info[j.num] = dict_Node_info
                dict_main[i] = dict_time
                dict_main_info[i] = dict_time_info

            return dict_main,dict_main_info
        self.ffDict ,self.ffDict_info= updateDict_FF(self.firefighterList)

        def ffStatusAndPosDict(list):
            for i in range(self.currentTime + 1):
                for j in list[i]:
                    if(i == self.currentTime):
                        self.ffPosSta[j.num - 1][0].append(j.curPos().getNum())
                        if (j.isProcess() == True):
                            self.ffPosSta[j.num - 1][1].append("Processing")
                        elif (j.isTraveling() == True):
                            self.ffPosSta[j.num - 1][1].append("Traveling")
                        else:
                            self.ffPosSta[j.num - 1][1].append("Idle")
        ffStatusAndPosDict(self.firefighterList)

        self.dataUpdateSignal.emit("")





















