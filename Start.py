#!/usr/bin/env python
# coding: utf-8
<<<<<<< HEAD
import os


from PyQt5 import QtWidgets
#from controller import MainWindow_controller
from titleScreen import titleScreen

=======

# In[ ]:


from PyQt5 import QtWidgets

from controller import MainWindow_controller
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
<<<<<<< HEAD
    #window = MainWindow_controller()
    window = titleScreen()
=======
    window = MainWindow_controller()
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
    window.show()
    sys.exit(app.exec_())







<<<<<<< HEAD




=======
>>>>>>> 8d9ef3706cfac9a94427e981d940585d65a6741e
