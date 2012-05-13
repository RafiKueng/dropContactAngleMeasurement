# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:52:14 2012

@author: rafik
"""

import numpy as np

#def of types for plugins
class plugintype:
    #None = -1 = None
    Reader = 0
    Worker = 1
    Writer = 2

# def of datatypes that can be used in the datastream

#Undef = -1 #don't use this!!
#None = 0
Bool = 1
Int = 2
Float = 3
Complex = 4

Array = 10
Matrix = 11
List = 12
Image = 13
String = 14

#image datatypes
img_Any = 20 
img_BW = 21
img_Gray = 22
img_8b = 23
img_16b = 24
img_32b = 25



def createDataDescriptor(name, describtion, datatype, embeddedtype=None, unit="1"):
    """Helper to create a tuple describing elements in the datastream

    name: short name
    desc: long describtion (for gui)
    dtype: basic datatype
    embtype: further classification for datatype (example: type of elements
            of a list, ...)
    unit: the si unit (as a string)
    """
    return (name, describtion, datatype, embeddedtype, unit)
    
    
    
    
class AbstractPlugin(object):
    """Basic / Abstract class for plugins. each plugin should inherit from
    this class and implement the methods
    """
    

    # methods to override by child classes

    def __init__(self):
        raise NotImplementedError
    
    def config(self):
        raise NotImplementedError
    
    def __call__(self, data):
        raise NotImplementedError
        
    def finish(self):
        """will be called on at the end of the programm
        use for cleaning up, saving files ect..."""
        raise NotImplementedError
        
        
    
    
    # provided functions, no need to override, since default behaviour is mosly what you want
    
    def setup(self, inp_ch=None):
        """tells the plugin in which field of the datastream the expected 
        inputs can be found"""
        
        if inp_ch == None and self.inputinfo == None:
            self.inp_ch = None
        elif len(self.inputinfo) == len(inp_ch):
            self.inp_ch = inp_ch
        else:
            raise NotImplementedError, "some strage error occured"


    def getOutputInfo(self): #maybe get rid of these, since direct dataaccess is possible
        return self.outputinfo

    __type__ = None 

    def getInputInfo(self):
        return self.inputinfo
        
    def check(self):
        """check whether this plugin is coded the right way"""
        success = True
        
        if success:
            return True
        else:
            raise NotImplementedError, "The Plugin is not programmed the right way"
    
    
class AngleMeasurement:
    angleLeft = np.NaN
    angleRight = np.NaN

    angleLefrR2 = 0
    angleRightR2 = 0

    rootOk = False
    rootDelta = 0
    
    baselineOk = False
    baseline = [[0,0],[0,0]]

    pipetteOK = False
    
    fitOK = False
    
    def isOK(self):
        return (self.rootOk and self.baselineOk
                and self.pipetteOK and self.fitOK)