# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np

import helper as h

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


class outSimpleDisplay(h.AbstractPlugin):
    

    def __init__(self):
        
        inp0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        inp1 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.iAny)        
            
        self.inputinfo = [inp0, inp1]
        self.outputinfo = None


    
    def config(self):
        cv2.namedWindow('Output %s'%self.inp_ch[1])
        #self.id = id #id of element in datastream to display


    
    def __call__(self, data):
        print ' - outSimpleDisplay: display data nr %.0f @t: %f' % (data[self.inp_ch[0]], time.time())
        #print type(data[1])
        
        #print data[0]
        #print data[1]
        #print data[2]
        
        cv2.imshow('Output %s'%self.inp_ch[1], data[self.inp_ch[1]])
        
        print ' - outSimpleDisplay: (sleeping) and waiting for key @t: %f' % (time.time())
        cv2.waitKey(1)
        time.sleep(0.5)



if __name__ == '__main__':
    #getData()
    pass