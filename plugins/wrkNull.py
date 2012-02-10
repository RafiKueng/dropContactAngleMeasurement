# -*- coding: utf-8 -*-
"""
Basic worker layout, doesn't do anything except
waiting and passing the data on

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

import Abstract as a

#import cv2
import time


class wrkNull(a.BasePlugin):

    def __init__(self):
        self.inputinfo = 
        pass
    
    def setup(self):
        pass
    
    def __call__(self, data):
        time.sleep(2)
        return data
        

if __name__ == '__main__':
    #getData()
    pass
    