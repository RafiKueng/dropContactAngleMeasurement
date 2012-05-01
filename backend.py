# -*- coding: utf-8 -*-
"""
backend of the program



Created on Mon Feb 27 19:14:20 2012

@author: rafik
"""

class Backend(object):

    isDoneSetup = False
    isDoneConfig = False

    def __init__(self):
        pass
    
    def getAvailablePlugins(self, pType):
        pass
    
    def setPlugins(self):
        self.isDoneSetup = True
        pass
        
    def saveSetup(self):
        pass        
        
    def loadSetup(self, filename):
        self.isDoneSetup = True
        pass
    

    def initConfig(self):
        pass
    
    def config(self, id, para=[]):
        # wenn para leer, return liste mit parameter und descr.
        pass
    
    def IsConfigDone(self):
        return False
        
    def saveConfig(self):
        pass
    
    def loadConfig(self):
        pass
        

    """ finally sets up the pipeline with all configs, ready to work"""
    
    def initWorking(self, config):
        pass
    
    def start():
        pass
    
    def stop():
        pass
    
    def abort():
        pass
    
    def getStatus():
        pass
    