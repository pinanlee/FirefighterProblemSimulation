#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PyQt5 import QtWidgets

from controller import MainWindow_controller
from networkGenerator import example

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    #window = example()
    window.show()
    sys.exit(app.exec_())







