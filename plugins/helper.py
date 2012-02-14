# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:52:14 2012

@author: rafik
"""

# def of datatypes that can be used in the datastream


#Undef = -1 #don't use this!!'
#None = 0
Bool = 1
Int = 2
Float = 3
Complex = 4

Array = 10
Matrix = 11
List = 12
Image = 13

#image datatypes
iAny = 20 
iBW = 21
iGray = 22
i8b = 23
i16b = 24
i32b = 25



def createDataDescriptor(name, describtion, datatype, embeddedtype=None):
    """Helper to create a tuple describing elements in the datastream

    name: short name
    desc: long describtion (for gui)
    dtype: basic datatype
    embtype: further classification for datatype (example: type of elements
            of a list, ...)
    """
    return (name, describtion, datatype, embeddedtype)
    
    
    
    
class AbstractPlugin(object):
    """Basic / Abstract class for plugins. each plugin should inherit from
    this class and implement the methods
    """
    def __init__(self):
        raise NotImplementedError
    
    def setup(self, inp_ch=None):
        """tells the plugin in which field of the datastream the expected 
        inputs can be found"""
        
        if inp_ch == None and self.inputinfo == None:
            self.inp_ch = None
        elif len(self.inputinfo) == len(inp_ch):
            self.inp_ch = inp_ch
        else:
            raise NotImplementedError, "some strage error occured"
        
    def config(self):
        raise NotImplementedError
    
    def __call__(self, data):
        raise NotImplementedError

    def getOutputInfo(self): #maybe get rid of these, since direct dataaccess is possible
        return self.outputinfo
        
    def getInputInfo(self):
        return self.inputinfo
        
    def check(self):
        """check whether this plugin is coded the right way"""
        success = True
        
        if success:
            return True
        else:
            raise NotImplementedError, "The Plugin is not programmed the right way"
        
    