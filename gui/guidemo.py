# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:26:22 2012

@author: rafik
"""

#import sys
#from PyQt4 import QtCore, QtGui
#
#from dropgui import Ui_MainWindow
#
#
#class MainWindow(QtGui.QMainWindow()):
#    def __init__(self):
#        QtGui.QMainWindow.__init__(self)
#
#        self.ui = Ui_MainWindow()
#        self.ui.setupUi(self)
#
#
#
#
#
#
#def main():
#    print 'main'
#    app = QtGui.QApplication(sys.argv)
#    mw = MainWindow()
#    mw.show()
#    app.exec_()
#
#
#if __name__=="__main__":
#        main()



import os,sys

# Import Qt modules
from PyQt4 import QtCore,QtGui

# Import the compiled UI module
from dropgui import Ui_MainWindow

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        for i in range(3):
            item=QtGui.QTreeWidgetItem(["test",str(i)])
            item.setCheckState(0, QtCore.Qt.Checked)
            self.ui.treeInput.addTopLevelItem(item)
            
    def on_treeInput_itemChanged(self, item, column):
        print 'item changed', item, column
        

def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()