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


class outSaveFrame(h.AbstractPlugin):
    

    def __init__(self):
        
        inp0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        inp1 = h.createDataDescriptor(
            name="Frame",
            describtion="The frame to save",
            datatype=h.Image,
            embeddedtype=h.img_Any)        
            
        self.inputinfo = [inp0, inp1]
        self.outputinfo = None


    
    def config(self, filename="outp", ext="jpg"):
        self.filename = filename
        self.ext = ext
        

    
    def __call__(self, data):
        print ' - outSaveFrame: display frame nr %.0f @t: %f' % (data[self.inp_ch[0]], time.time())
        
        fullfilename = "{:s}{:05.0f}.{:s}".format(self.filename, data[self.inp_ch[0]], self.ext)
        
        print fullfilename

        cv2.imwrite(fullfilename, data[self.inp_ch[1]])


if __name__ == '__main__':
    #getData()
    pass