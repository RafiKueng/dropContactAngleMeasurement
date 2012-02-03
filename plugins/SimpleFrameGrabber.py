# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np
import cv2.cv as cv


file = cv.CaptureFromFile('bin/testfile.mpg')
print cv.GetCaptureProperty(file, cv.CV_CAP_PROP_FRAME_WIDTH)


def getData():
    cv.GrabFrame(file)    
    return cv.RetrieveFrame(file)

if __name__ == '__main__':
    #getData()
    pass