# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:40:30 2012

@author: rafik
"""

#from os import sys
#import numpy as np

import helper as h

import time

import csv



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


class outSimpleCSVWriter(h.AbstractPlugin):
    

    def __init__(self):
        
        inp0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)

        inp1 = h.createDataDescriptor(
            name="Angle",
            describtion="The final angles (array, left, right, in degrees)",
            datatype=h.Array,
            embeddedtype=h.Int)        
            
        self.inputinfo = [inp0, inp1]
        self.outputinfo = None

    
    def config(self, filename, ext = "csv"):
        print 'outSimpleCSVWriter: config\n  outpath:' + filename + "."+ext
        #self.f = open(filename, "wb")
        #self.f.write("testingggggg")
        #self.writer = csv.writer(self.f)
        #self.writer.writerow(["testing", "test2"])
        #self.fff = open(filename, "wb")
        self.file = open(filename + "."+ext, "wb")
        self.csvwrt = csv.writer(self.file, dialect='excel')
        self.csvwrt.writerow(["FrameNr","ms", "AngleL","AngleR","ResL","ResR","RootL","RootR","chosenAngle",
                              "AngleL1","AngleR1","ResL1","ResR1","RootL1","RootR1",
                              "AngleL2","AngleR2","ResL2","ResR2","RootL2","RootR2",
                              "AngleL3","AngleR3","ResL3","ResR3","RootL3","RootR3",
                              "AngleL_Mean","AngleR_Mean","ResL_Mean","ResR_Mean","RootL_Mean","RootR_Mean",
                              "AngleL_Median","AngleR_Median","ResL_Median","ResR_Median","RootL_Median","RootR_Median",])
    
    def __call__(self, data):
        #print ' - outSimpleCSVWriter: write data nr %.0f @t: %f' % (data[self.inp_ch[0]], time.time())
        #print [data[self.inp_ch[0]]] + data[self.inp_ch[1]]
        
        self.csvwrt.writerow([data[0]] + [data[2]] + data[3].getRes())
        self.file.flush()
        
    def finish(self):
        self.file.flush()
        self.file.close()



if __name__ == '__main__':
    #getData()
    pass