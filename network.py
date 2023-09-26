import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore
from node import Node
from nodeButtonController import NodeController

class Network:
    def __init__(self, adjFile, posFile) -> None:
        self.adjList = [[]]
        self.nodeList : list[NodeController] = []
        df = pd.read_excel(posFile)
        df_num = len(df.index)
        for i in range(df_num):
            self.adjList.append([])
            nodePos = QtCore.QRect(df.iloc[i]["x"] + 300, df.iloc[i]["y"], 30, 25)
            nodeButton = NodeController(i+1, nodePos)
            nodeButton.value = df.iloc[i]["value"]
            nodeButton.initValue = df.iloc[i]["value"]
            nodeButton.burningTime = df.iloc[i]["burning time"]
            nodeButton.quantity = df.iloc[i]["quantity"]
            self.nodeList.append(nodeButton)
        df = pd.read_excel(adjFile)
        for j in df.iloc:
            self.adjList[int(j["i"])].append([int(j["j"]), 1])
        self.connect(adjFile)
    
    def connect(self, adjFile):
        df = pd.read_excel(adjFile)
        df_num = len(df.index)
        for i in range(df_num):
            length = int(df.iloc[i]["d"])
            time = df.iloc[i]["travel time"]
            self.nodeList[int(df.iloc[i]["i"]) - 1].connectNode(self.nodeList[int(df.iloc[i]["j"]) - 1], length, time)

        '''for i in self.nodeList:
            pos1 = np.array((i.pos.x(),i.pos.y()))
            for j in self.adjList[i.getNum()]:
                pos2 = np.array((self.nodeList[j[0]-1].pos.x(),self.nodeList[j[0]-1].pos.y()))
                #length = int(np.linalg.norm(pos1-pos2))
                length = int(df.iloc[i]["d"])
                time = df.iloc[i]["travel-time"]
                i.connectNode(self.nodeList[j[0]-1], length, time)'''
    def getTotalValue(self) -> int:
        value = 0
        for i in self.nodeList:
            value += i.value
        return int(value)