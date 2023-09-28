import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore
from node import Node
from nodeButtonController import NodeController

class Network:
    def __init__(self, adjFile, posFile, S) -> None:
        self.adjList = [[]]
        self.nodeList : list[NodeController] = []
        df = pd.read_excel(posFile, sheet_name=None)
        ctr = 1
        for i in df["coordinates"].iloc:
            self.adjList.append([])
            nodePos = QtCore.QRect(i["x"] + 300, i["y"], 30, 25)
            nodeButton = NodeController(ctr, nodePos, i["value"], i["burning time"],  i["quantity"])
            self.nodeList.append(nodeButton)
            ctr+=1
        self.nodeList[df["source"].iloc[0][S]-1].depot = True
        df = pd.read_excel(adjFile)
        for j in df.iloc:
            self.adjList[int(j["i"])].append([int(j["j"]), 1])
        self.connect(df)
    
    def connect(self, df):
        for i in df.iloc:
            length = int(i["d"])
            time = i["travel time"]
            nodeNum = int(i["j"]) - 1
            self.nodeList[int(i["i"]) - 1].connectNode(self.nodeList[nodeNum], length, time)
    
    def getTotalValue(self) -> int:
        return int(sum(i.value for i in self.nodeList))