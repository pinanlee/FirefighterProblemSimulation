#!/usr/bin/env python
# coding: utf-8
import os

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from titleScreen import titleScreen


if __name__ == '__main__':
    import sys
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    with open("stylesheet/titlescreen.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)
    window = titleScreen()
    window.show()
    sys.exit(app.exec_())











