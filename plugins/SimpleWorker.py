# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

import cv2
import time



class piSimpleWorker(object):

    def __init__(self):
        pass
    
    def setup(self):
        cv2.namedWindow('worker')
    
    def procData(self, data):
        print 'worker: processing data (display it)'
        print type(data[0])
        print data[0]
        
        cv2.imshow('worker', data[0])
        
        print 'worker: sleeping and waiting for key'
        cv2.waitKey(1)
        time.sleep(2)
        

#    def __getstate__(self):
#        return ''
#    
#    def __setstate__(self, state):
#        pass

if __name__ == '__main__':
    #getData()
    pass
    