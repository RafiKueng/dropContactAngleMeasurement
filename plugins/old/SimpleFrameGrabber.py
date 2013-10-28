# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np
import cv2


#file = cv.CaptureFromFile('bin/testfile.mpg')
#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)



class piSimpleFrameGrabber(object):
    def __init__(self):
        print 'init framegraber'
        self.filename = 'bin/testfile.mpg'
        pass
    
    def setup(self):
        print 'setup framegraber'
        self.video = cv2.VideoCapture(self.filename)
        pass
        
    def getData(self):
        #video = cv2.VideoCapture('bin/testfile.mpg')
        ret, img = self.video.read()
        return img
        
        #cv.GrabFrame(file)    
        #return cv.RetrieveFrame(file)

#    def __getstate__(self):
#        return self.filename
#    
#    def __setstate__(self, state):
#        self.filename = state
#        #self.video = cv2.VideoCapture(self.filename)


if __name__ == '__main__':
    #getData()
    pass