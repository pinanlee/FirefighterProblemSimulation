import pandas as pd
from PyQt5 import QtCore
from node import Node
from nodeButtonController import NodeController
from dataBase import DataBase

class Network:
    def __init__(self, adjFile, posFile, depot) -> None:
        self.nodeList : list[NodeController] = []
        self.__createNode(posFile, depot)
        self.__connectNode(adjFile, depot)
    
    def __connectNode(self, adjFile, depot):
        df = pd.read_excel(adjFile)
        for i in df.iloc:
            length = int(i["d"])
            time = i["travel time"]
            if(depot == "N_D"):
                DataBase.tau.append(time)
            else:
                DataBase.lamb.append(time)
            nodeNum = int(i["j"]) - 1
            self.nodeList[int(i["i"]) - 1].connectNode(self.nodeList[nodeNum], length, time)
    
    def getTotalValue(self) -> int:
        return int(sum(node.getValue() for node in self.nodeList))

    def __createNode(self,posFile, depot):
        df = pd.read_excel(posFile, sheet_name=None)
        for index, i in enumerate(df["coordinates"].iloc):
            nodePos = QtCore.QRect(i["x"], i["y"], 30, 25)
            nodeButton = NodeController(index + 1, nodePos, i["value"], i["burning time"],  i["quantity"])
            self.nodeList.append(nodeButton)
        self.nodeList[df["source"].iloc[0][depot]-1].depotSetting()