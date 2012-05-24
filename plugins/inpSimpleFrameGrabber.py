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
        #print 'inpSimpleFrameGrabber\n  init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.img_Gray)        
            
        self.outputinfo = [out0, out1]

        self.counter = -1
    

    def config(self, filename):
        print 'inpSimpleFrameGrabber: config\n  @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        
        self.nFrames = self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.cv.CV_CAP_PROP_FPS)

    def __call__(self, advance=True):
        
        if not advance:
            self.setDeltaPos(-1)
        
        pos = self.video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        #self.counter += 1
        #print ' - inpSimpleFrameGrabber: read frame @t: %f' % (time.time())        
        img = cv2.cvtColor(self.video.read()[1], cv2.COLOR_BGR2GRAY)
        #print ' - inpSimpleFrameGrabber: frame nr %.0f read finish @t: %f' % (pos, time.time())    
        #print img
        return [pos, img]            
    
    
    def setPos(self, pos):
        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
    
    
    def setDeltaPos(self, delta):
        pos = self.video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos+delta)
        
    def getFrameNr(self, pos):
        self.video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
        img = cv2.cvtColor(self.video.read()[1], cv2.COLOR_BGR2GRAY)
        return [pos, img]
        

if __name__ == '__main__':
    #getData()
    pass