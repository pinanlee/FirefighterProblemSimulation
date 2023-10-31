import pandas as pd
from PyQt5 import QtCore
from nodeButtonController import NodeController
from dataBase import DataBase

class Network:
    def __init__(self, adjFile, depot=None) -> None:
        self.nodeList : list[NodeController] = []
        self.ffNum = 0
        self.__createNode(adjFile, depot)
        self.__connectNode(adjFile, depot)
        self.FFrate=[]

    def __connectNode(self, adjFile, depot):
        df = pd.read_excel(adjFile, sheet_name=None)
        if(depot=="N_D"):
            for i in df["firefighter_route"].iloc:
                nodeNum = int(i["j"]) - 1
                if self.nodeList[int(i["i"]) - 1].getArc(self.nodeList[nodeNum]) == None:
                    length = int(i["d"])
                    time = i["travel time"]
                    DataBase.tau.append(time)
                    self.nodeList[int(i["i"]) - 1].connectNode(self.nodeList[nodeNum], length, i["k"], time)
                else:
                    time = i["travel time"]
                    self.nodeList[int(i["i"]) - 1].arcAddTime(self.nodeList[nodeNum], i["k"], time)
                self.ffNum = max(i["k"], self.ffNum)
        else:
            for i in df["fire_route"].iloc:
                length = int(i["d"])
                time = i["travel time"]
                DataBase.lamb.append(time)
                nodeNum = int(i["j"]) - 1
                self.nodeList[int(i["i"]) - 1].connectNode(self.nodeList[nodeNum], length, None, time)

    
    def getTotalValue(self) -> int:
        return int(sum(node.getValue() for node in self.nodeList))

    def __createNode(self,posFile, depot):
        df = pd.read_excel(posFile, sheet_name=None)
        for index, i in enumerate(df["coordinates"].iloc):
            nodePos = QtCore.QRect(i["x"], int(i["y"]/2), 30, 25)
            nodeButton = NodeController(index + 1, nodePos, i["value"], i["burning time"],  i["quantity"])
            self.nodeList.append(nodeButton)
        if(depot=="N_D"):
            self.nodeList[int(df["ff_source"].iloc[0][depot])-1].depotSetting()
        else:
            self.nodeList[int(df["fire_source"].iloc[0][depot])-1].depotSetting()
        DataBase.T =  df["T"].iloc[0]["T"]