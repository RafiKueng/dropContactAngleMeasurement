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
    
    def setup(self, id):
        cv2.namedWindow('Output %s'%id)
        self.id = id #id of element in datastream to display
    
    def writeData(self, data):
        print ' - outSimpleDisplay: display data nr %.0f @t: %f' % (data[0], time.time())
        #print type(data[1])
        #print data[1]
        
        cv2.imshow('Output %s'%self.id, data[self.id])
        
        print ' - outSimpleDisplay: (sleeping) and waiting for key @t: %f' % (time.time())
        cv2.waitKey(1)
        time.sleep(0.5)



if __name__ == '__main__':
    #getData()
    pass