# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

import helper as h

#from os import sys
#import numpy as np
import cv2
import time

#file = cv.CaptureFromFile('bin/testfile.mpg')
#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)



class inpSimpleFrameGrabber(h.AbstractPlugin):

    def __init__(self):
        print ' - inpSimpleFrameGrabber: Init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.img_Any)        
            
        self.outputinfo = [out0, out1]

        self.counter = 0
    

    def config(self, filename):
        print ' - inpSimpleFrameGrabber: config @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        pass
        

    def __call__(self):
        #video = cv2.VideoCapture('bin/testfile.mpg')
        self.counter += 1
        print ' - inpSimpleFrameGrabber: read frame @t: %f' % (time.time())        
        ret, img = self.video.read()
        print ' - inpSimpleFrameGrabber: frame nr %.0f read finish @t: %f' % (self.counter, time.time())    
        #print img
        return [self.counter, img]
        


if __name__ == '__main__':
    #getData()
    pass