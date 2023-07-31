from PyQt5 import QtWidgets

from ui import Ui_MainWindow

class example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.aa()
        #self.ui.setupUi(self)
    
    