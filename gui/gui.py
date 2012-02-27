# -*- coding: utf-8 -*-
"""
gui tests
Created on Wed Feb 22 21:00:12 2012

@author: rafik
"""


from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setGeometry(300, 300, 180, 380)
        self.setWindowTitle('drop C.A.M.')

        self.interface = Interface(self)
                
        self.setCentralWidget(self.interface)
            
        self.statusbar = self.statusBar()
        self.connect(self.interface, QtCore.SIGNAL("messageToStatusbar(QString)"), self.statusbar, QtCore.SLOT("showMessage(QString)"))
                
        #self.interface.start()
        self.center()
        
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        
class Interface(QtGui.QFrame):
    
    def __init__(self, parent):
        print "interface init"
        QtGui.QFrame.__init__(self, parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
    def keyPressEvent(self, event):
        key = event.key()
        print "key pressed", key
        if key == QtCore.Qt.Key_P:
            self.pause()
        return
        
    def pause(self):
        print "key p pressed"
        self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "p pressed")