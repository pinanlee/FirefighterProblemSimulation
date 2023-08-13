import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore
from node import Node
from nodeButtonController import NodeController

class Network:
    def __init__(self, adjFile, posFile) -> None:
        self.adjList = [[]]
        self.nodeList = []
        df = pd.read_excel(posFile)
        df_num = len(df.index)
        for i in range(df_num):
            self.adjList.append([])
            nodePos = QtCore.QRect(df.iloc[i]["x"], df.iloc[i]["y"], 30, 25)
            nodeButton = NodeController(i+1, nodePos)
            self.nodeList.append(nodeButton)
        df = pd.read_excel(adjFile)
        for j in df.iloc:
            self.adjList[ord(j["i"])-64].append([ord(j["j"])-64, 1])
            self.adjList[ord(j["j"])-64].append([ord(j["i"])-64, 1])  
        self.connect()
    
    def connect(self):
        for i in self.nodeList:
            pos1 = np.array((i.pos.x(),i.pos.y()))
            for j in self.adjList[i.getNum()]:
                pos2 = np.array((self.nodeList[j[0]-1].pos.x(),self.nodeList[j[0]-1].pos.y()))
                length = np.linalg.norm(pos1-pos2)
                i.connectNode(self.nodeList[j[0]-1], length)
