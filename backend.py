# -*- coding: utf-8 -*-
"""
backend of the program



Created on Mon Feb 27 19:14:20 2012

@author: rafik
"""

class PipelineSetup(object):
    """Handles the Setup of the Pipeline"""
    
    def __init__():
        pass
    
    def getAvailablePlugins(self, pType):
        pass
    
    def setPlugin(self):
        pass
        
    def saveSetup(self):
        pass        
        
    def loadSetup(self, filename):
        pass
    

class PipelineConfig(object):
    """Sets up the pipeline and handles the configuration of each plugin"""
    
    def __init__(self, setup):
        pass
    
    def config(self, id):
        pass
    
    def IsConfigDone(self):
        return False
        
    def saveConfig(self):
        pass
    
    def loadConfig(self):
        pass
        

class Pipeline(object):
    """ finally sets up the pipeline with all configs, ready to work"""
    
    def __init__(self, config):
        pass
    
    def start():
        pass
    
    def stop():
        pass
    
    def abort():
        pass
    
    def getStatus():
        pass
    