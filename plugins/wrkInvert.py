# -*- coding: utf-8 -*-
"""
Demo Plugin
Inverts the picture

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

from Abstract import wrkAbstract

import cv2
import time


class wrkInvert(wrkAbstract):

    def __init__(self):
        pass
    
    def setup(self, *args):
        pass
    
    def procData(self, data):
        print ' - wrkInvert: processing data @t: %f' % (time.time())
        #time.sleep(1)
        
        return [cv2.transpose(data[0])]
        

if __name__ == '__main__':
    #getData()
    pass
    