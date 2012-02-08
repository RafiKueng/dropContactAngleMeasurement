# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np

from Abstract import outAbstract

import cv2
import time



#cap = cv.CreateFileCapture("../bin/tree.avi")
#img = cv.QueryFrame(cap)
#print "Got frame of dimensions (", img.width, " x ", img.height, ")"
#
#cv.NamedWindow("win", cv.CV_WINDOW_AUTOSIZE)
#cv.ShowImage("win", img)
#cv.MoveWindow("win", 200, 200)
#cv.WaitKey(0)


#file = cv.CaptureFromFile('../bin/testfile.mpg')

#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)


class outSimpleDisplay(outAbstract):
    

    def __init__(self):
        pass
    
    def setup(self):
        cv2.namedWindow('Output')
    
    def writeData(self, data):
        print ' - outSimpleDisplay: display data @t: %f' % (time.time())
        #print type(data[0])
        #print data[0]
        
        cv2.imshow('Output', data[0])
        
        print ' - outSimpleDisplay: (sleeping) and waiting for key @t: %f' % (time.time())
        cv2.waitKey(1)
        #time.sleep(0.001)



if __name__ == '__main__':
    #getData()
    pass