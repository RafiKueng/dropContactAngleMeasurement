# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np
import cv2.cv as cv



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



def init():
    pass

def setup():
    cv.NamedWindow("win", cv.CV_WINDOW_AUTOSIZE)

def writeData(self,data):

    cv.ShowImage("win", data[0])
    cv.WaitKey(0)



if __name__ == '__main__':
    #getData()
    pass