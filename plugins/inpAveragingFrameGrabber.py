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
from collections import deque

#file = cv.CaptureFromFile('bin/testfile.mpg')
#print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)




class inpAveragingPlayPauseFrameGrabber(h.AbstractPlugin):
    """This does a moving average, for each frame in the input movie theres
    one in the output data, the average is taken over the x last frames
    offers the ability to get the last frame once again (using __call__(advance=false) )
    
    converts frame to grayscale first    
    """

    def __init__(self):
        print ' - inpAveragingPlayPauseFrameGrabber: Init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The averaged grayscale frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.img_Gray,
            unit="Px")        
            
        self.outputinfo = [out0, out1]

        self.counter = -1
    

    def config(self, filename, average_over=3):
        print ' - inpAveragingPlayPauseFrameGrabber: config @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        self.average_over = average_over
        self.frames = deque(maxlen=self.average_over) #set up buffer. if full, and new element added, last one is lost
        
        #fill up buffer   
        print ' - inpAveragingPlayPauseFrameGrabber: fill up avg buffer with %.0f frames @t: %f' % (self.average_over-1, time.time())
        
        while self.counter < self.average_over-2:
            self.frames.append(
                np.uint32( #convert to uint32, so the summation afterwards doesnt encounter an overflow
                    cv2.cvtColor( #convert to grayscale
                            self.video.read()[1], #read image
                        cv2.COLOR_BGR2GRAY)))
            self.counter += 1
            
        #get the length of the video
        self.nFrames = self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        

    def __call__(self, advance=True):
        if advance:
            self.counter += 1
            print ' - inpAveragingPlayPauseFrameGrabber: read frame @t: %f' % (time.time())  
            
            self.frames.append(
                np.uint32( #convert to uint32, so the summation afterwards doesnt encounter an overflow
                    cv2.cvtColor( #convert to grayscale
                            self.video.read()[1], #read image
                        cv2.COLOR_BGR2GRAY)))
    
            img = np.uint8(sum(self.frames) // self.average_over)
    
            print ' - inpAveragingPlayPauseFrameGrabber: frame nr %.0f read finish @t: %f' % (self.counter, time.time())    
            return [self.counter, img]
        else:
            print ' - inpAveragingPlayPauseFrameGrabber: returning old frame @t: %f' % (time.time())  
            img = np.uint8(sum(self.frames) // self.average_over)
            return [self.counter, img]


    def finish(self):
        pass


class inpAveragingFrameGrabber(h.AbstractPlugin):
    """This does a moving average, for each frame in the input movie theres
    one in the output data, the average is taken over the x last frames
    
    converts frame to grayscale first    
    """

    def __init__(self):
        print ' - inpAveragingFrameGrabber: Init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The averaged grayscale frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.img_Gray,
            unit="Px")        
            
        self.outputinfo = [out0, out1]

        self.counter = -1
    

    def config(self, filename, average_over=3):
        print ' - inpAveragingFrameGrabber: config @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        self.average_over = average_over
        self.frames = deque(maxlen=self.average_over) #set up buffer. if full, and new element added, last one is lost
        
        #fill up buffer   
        print ' - inpAveragingFrameGrabber: fill up avg buffer with %.0f frames @t: %f' % (self.average_over-1, time.time())
        
        while self.counter < self.average_over-2:
            self.frames.append(
                np.uint32( #convert to uint32, so the summation afterwards doesnt encounter an overflow
                    cv2.cvtColor( #convert to grayscale
                            self.video.read()[1], #read image
                        cv2.COLOR_BGR2GRAY)))
            self.counter += 1
            
        #get the length of the video
        self.nFrames = self.video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        

    def __call__(self):
        self.counter += 1
        print ' - inpAveragingFrameGrabber: read frame @t: %f' % (time.time())  
        
        self.frames.append(
            np.uint32( #convert to uint32, so the summation afterwards doesnt encounter an overflow
                cv2.cvtColor( #convert to grayscale
                        self.video.read()[1], #read image
                    cv2.COLOR_BGR2GRAY)))

        img = np.uint8(sum(self.frames) // self.average_over)

        print ' - inpAveragingFrameGrabber: frame nr %.0f read finish @t: %f' % (self.counter, time.time())    
        return [self.counter, img]
        


class inpSimpleAveragingFrameGrabber(h.AbstractPlugin):
    """This reads x frames in a row, makes an average and returns that
    as one frame to the datastream"""

    def __init__(self):
        print ' - inpSAveragingFrameGrabber: Init @t: %f' % (time.time())

        self.inputinfo = None
        
        out0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        out1 = h.createDataDescriptor(
            name="Frame",
            describtion="The averages frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.iAny,
            unit="Px")        
            
        self.outputinfo = [out0, out1]

        self.counter = -1
    

    def config(self, filename, average_over=3):
        print ' - inpAveragingFrameGrabber: config @t: %f' % (time.time())
        self.video = cv2.VideoCapture(filename)
        self.average_over = average_over
        pass
        

    def __call__(self):
        #video = cv2.VideoCapture('bin/testfile.mpg')
        self.counter += 1
        print ' - inpAveragingFrameGrabber: read frame @t: %f' % (time.time())  
        #imgx = np.zeros((self.average_over, 1024,1280,3), np.uint32)
        imgx = np.zeros((1024,1280,3), np.uint32)
        for i in range(self.average_over):
            imgx += self.video.read()[1]
        
        #img = np.zeros((1024,1280,3), np.uint8)
        img = np.uint8(imgx // self.average_over)
        print ' - inpAveragingFrameGrabber: frame nr %.0f read finish @t: %f' % (self.counter, time.time())    
        #print img[0]
        return [self.counter, img]


if __name__ == '__main__':
    #getData()
    pass