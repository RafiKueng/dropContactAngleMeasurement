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
from pluginWidget import Ui_Form as ui_plugin


class pluginWidget(QtGui.QWidget):
    
    onClickConfigSignal = QtCore.pyqtSignal(int)  
    onClickRemoveSignal = QtCore.pyqtSignal(int)  
    
    def __init__(self, parent, pluginType, number):
        QtGui.QWidget.__init__(self)

        self.pluginType = pluginType
        self.number = number
        
        self.ui=ui_plugin()
        self.ui.setupUi(self)

    
        
        QtCore.QObject.connect(self.ui.btnEdit, QtCore.SIGNAL('clicked()'), self.onClickConfig)
        QtCore.QObject.connect(self.ui.btnEdit, QtCore.SIGNAL('clicked()'), self.onClickConfig)
        
        #QtCore.QObject.connect(self.ui.btnEdit, QtCore.SIGNAL('clicked()'), )
        
        #self.clicked_config.connect(parent.onClickConfigPlugin)

        #self.ui.btnEdit.clicked.connect(self.clkConf)
        #self.ui.btnEdit.clicked.connect(parent.onClickConfigPlugin)
        
    def onClickConfig(self):
        print 'clicked on config in wiget nr.', self.number
        self.onClickConfigSignal.emit(self.number)
        
    def onClickRemove(self):
        print 'clicked on remove in wiget nr.', self.number
        self.onClickRemoveSignal.emit(self.number)
        

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        inpPlugins = []*10
        
        for i in range(10):
            inpPlugins[i] = pluginWidget(self, 'inp', i)
            
            inpPlugins[i].clickedConfigSignal.connect(self.onClickConfigPlugin)
            inpPlugins[i].clickedConfigSignal.connect(self.onClickRemovePlugin)


            inpPlugins[i].ui.txtName.setText('bla'+str(i))
            inpPlugins[i].ui.txtDesc.setText(' blablablabla')
            self.ui.vlayoutInput.insertWidget(i,inpPlugins[i])
            

            
    @QtCore.pyqtSlot(int)
    def onClickConfigPlugin(self, nr):
        print "configure plugin nr", nr

    @QtCore.pyqtSlot(int)
    def onClickRemovePlugin(self, nr):
        print "remove plugin nr", nr
        

def main():

    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()