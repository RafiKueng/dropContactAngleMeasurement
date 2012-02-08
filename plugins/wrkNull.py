# -*- coding: utf-8 -*-
"""
Basic worker layout, doesn't do anything except passing the data on

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

#import cv2
import time


class wrkNull(object):

    def __init__(self):
        pass
    
    def setup(self):
        pass
    
    def procData(self, data):
        time.sleep(2)
        return data
        

if __name__ == '__main__':
    #getData()
    pass
    