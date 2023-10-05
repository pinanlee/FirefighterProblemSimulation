import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore
from node import Node
from nodeButtonController import NodeController

class Network:
    def __init__(self, adjFile, posFile, depot) -> None:
        self.nodeList : list[NodeController] = []
        self.__createNode(posFile, depot)
        self.__connectNode(adjFile)
    
    def __connectNode(self, adjFile):
        df = pd.read_excel(adjFile)
        for i in df.iloc:
            length = int(i["d"])
            time = i["travel time"]
            nodeNum = int(i["j"]) - 1
            self.nodeList[int(i["i"]) - 1].connectNode(self.nodeList[nodeNum], length, time)
    
    def getTotalValue(self) -> int:
        return int(sum(node.getValue() for node in self.nodeList))

    def __createNode(self,posFile, depot):
        df = pd.read_excel(posFile, sheet_name=None)
        ctr = 1
        for i in df["coordinates"].iloc:
            #self.__adjList.append([])
            nodePos = QtCore.QRect(i["x"] + 300, i["y"], 30, 25)
            nodeButton = NodeController(ctr, nodePos, i["value"], i["burning time"],  i["quantity"])
            self.nodeList.append(nodeButton)
            ctr+=1
        self.nodeList[df["source"].iloc[0][depot]-1].depotSetting()