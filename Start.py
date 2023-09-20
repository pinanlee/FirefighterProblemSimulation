#!/usr/bin/env python
# coding: utf-8
import os


from PyQt5 import QtWidgets
from titleScreen import titleScreen


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = titleScreen()
    window.show()
    sys.exit(app.exec_())











