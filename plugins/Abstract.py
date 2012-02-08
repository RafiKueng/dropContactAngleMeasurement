# -*- coding: utf-8 -*-
"""
Abstract baseclasses for
* input
* output
* worker
plugins

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""


class wrkAbstract(object):

    def __init__(self):
        raise NotImplementedError
    
    def setup(self):
        raise NotImplementedError
    
    def procData(self, data):
        raise NotImplementedError
        




class inpAbstract(object):

    def __init__(self):
        raise NotImplementedError
    
    def setup(self):
        raise NotImplementedError
        
    def getData(self):
        raise NotImplementedError





class outAbstract(object):

    def __init__(self):
        raise NotImplementedError
    
    def setup(self):
        raise NotImplementedError
        
    def writeData(self):
        raise NotImplementedError




if __name__ == '__main__':
    #getData()
    pass
    