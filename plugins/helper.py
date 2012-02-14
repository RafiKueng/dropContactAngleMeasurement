# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:52:14 2012

@author: rafik
"""

# def of datatypes that can be used in the datastream

Undef = -1 #don't use this!!'
None = 0
Bool = 1
Int = 2
Float = 3
Complex = 4

Array = 10
Matrix = 11
List = 12
Image = 13

#image datatypes
iBW = 20
iGray = 21
i8b = 22
i16b = 23
i32b = 24



def createDataDescriptor(name, describtion, datatype, embeddedtype):
    """Helper to create a tuple describing elements in the datastream

    name: short name
    desc: long describtion (for gui)
    dtype: basic datatype
    embtype: further classification for datatype (example: type of elements
            of a list, ...)
    """
    return (name, desc, dtype, embtype)
    
    
    
    
class AbstractPlugin(object):
    """Basic / Abstract class for plugins. each plugin should inherit from
    this class and implement the methods
    """
    def __init__(self):
        raise NotImplementedError
    
    def setup(self, *args):
        raise NotImplementedError
        
    def config(self):
        raise NotImplementedError
    
    def __call__(self, data):
        raise NotImplementedError

    def getOutputInfo(self):
        return self.outputinfo
        
    def getInputInfo(self):
        return self.inputinfo