# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np
import cv2
from Abstract import inpAbstract
import time

#file = cv.CaptureFromFile('bin/testfile.mpg')
#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)



class inpSimpleFrameGrabber(inpAbstract):

    def __init__(self):
        print ' - inpSimpleFrameGrabber: Init @t: %f' % (time.time())
        #self.filename = 'bin/demo.avi'
        self.counter = 0
        pass
    
    def setup(self, filename):
        print ' - inpSimpleFrameGrabber: Setup @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        pass
        
    def getData(self):
        #video = cv2.VideoCapture('bin/testfile.mpg')
        print ' - inpSimpleFrameGrabber: read frame @t: %f' % (time.time())        
        ret, img = self.video.read()
        print ' - inpSimpleFrameGrabber: frame read finish @t: %f' % (time.time())    
        self.counter =+ 1
        return [img, self.counter]
        


if __name__ == '__main__':
    #getData()
    pass