# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 02:32:17 2012

@author: rafik
"""

import helper as h

#from os import sys
import numpy as np
import cv2
import time

#file = cv.CaptureFromFile('bin/testfile.mpg')
#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)



class inpAveragingFrameGrabber(h.AbstractPlugin):

    def __init__(self):
        print ' - inpAveragingFrameGrabber: Init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The averages frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.iAny)        
            
        self.outputinfo = [out0, out1]

        self.counter = 0
    

    def config(self, filename, average_over=3):
        print ' - inpAveragingFrameGrabber: config @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        self.average_over = average_over
        pass
        

    def __call__(self):
        #video = cv2.VideoCapture('bin/testfile.mpg')
        self.counter += 1
        print ' - inpAveragingFrameGrabber: read frame @t: %f' % (time.time())  
        imgx = np.zeros((self.average_over, 1024,1280,3), np.uint16)
        for i in range(self.average_over):
            imgx[i] += self.video.read()[1]
        
        img = np.zeros((1024,1280,3), np.uint8)
        img = imgx // self.average_over
        print ' - inpAveragingFrameGrabber: frame nr %.0f read finish @t: %f' % (self.counter, time.time())    
        print img[0]
        return [self.counter, img[0]]
        


if __name__ == '__main__':
    #getData()
    pass