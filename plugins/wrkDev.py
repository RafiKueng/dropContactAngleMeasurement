# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 17:22:41 2012

@author: rafik
"""

from Abstract import wrkAbstract

#import cv2
import time


class wrkDev(wrkAbstract):

    def __init__(self):
        pass
    
    def setup(self, *args):
        self.waittime = args[0]
        pass
    
    def procData(self, data):
        time.sleep(self.waittime)
        #print ' - worker: ', data
        return data
        

if __name__ == '__main__':
    #getData()
    pass