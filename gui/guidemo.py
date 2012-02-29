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
    onClickRemoveSignal = QtCore.pyqtSignal(QtGui.QWidget)  
    
    def __init__(self, parent, pluginType, number):
        QtGui.QWidget.__init__(self)

        self.pluginType = pluginType
        self.number = number
        
        self.ui=ui_plugin()
        self.ui.setupUi(self)

    
        
        QtCore.QObject.connect(self.ui.btnEdit, QtCore.SIGNAL('clicked()'), self.onClickConfig)
        QtCore.QObject.connect(self.ui.btnRemove, QtCore.SIGNAL('clicked()'), self.onClickRemove)
        
    def onClickConfig(self):
        print 'clicked on config in wiget nr.', self.number
        self.onClickConfigSignal.emit(self.number)
        
    def onClickRemove(self):
        print 'clicked on remove in wiget nr.', self.number
        self.onClickRemoveSignal.emit(self)
        

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.pluginContainers = [self.ui.vlayoutInp, self.ui.vlayoutProc, self.ui.vlayoutOutp]
        
        self.plugins = [[],[],[]]
        
        self.run()
        



    def run(self):
        for i in range(10):
            
            plugin = pluginWidget(self, i%3, i)
            
            plugin.onClickConfigSignal.connect(self.onClickConfigPlugin)
            plugin.onClickRemoveSignal.connect(self.onClickRemovePlugin)


            plugin.ui.txtName.setText('bla'+str(i))
            plugin.ui.txtDesc.setText(' blablablabla')
            
            self.pluginContainers[plugin.pluginType].insertWidget(0,plugin)

            self.plugins[plugin.pluginType].append(plugin)



            
    @QtCore.pyqtSlot(int)
    def onClickConfigPlugin(self, nr):
        print "configure plugin nr", nr

    @QtCore.pyqtSlot(QtGui.QWidget)
    def onClickRemovePlugin(self, plugin):
        print "remove plugin nr", plugin.number, "type:", plugin.pluginType
        self.pluginContainers[plugin.pluginType].removeWidget(plugin)
        self.plugins[plugin.pluginType].remove(plugin)
        plugin.deleteLater()




        

def main():

    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()