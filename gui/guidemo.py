# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:26:22 2012

@author: rafik
"""

import sys
from PyQt4 import QtCore, QtGui

from gui import MainWindow

app = QtGui.QApplication(sys.argv)
gui = MainWindow()
gui.show()
app.exec_()
