#!/usr/bin/env python
# coding: utf-8
import os


from PyQt5 import QtWidgets
from titleScreen import titleScreen


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    with open("stylesheet/titlescreen.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = titleScreen()
    window.show()
    
    sys.exit(app.exec_())











