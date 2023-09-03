#!/usr/bin/env python
# coding: utf-8
import os


from PyQt5 import QtWidgets
#from controller import MainWindow_controller
from titleScreen import titleScreen


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #window = MainWindow_controller()
    window = titleScreen()
    window.show()
    sys.exit(app.exec_())











