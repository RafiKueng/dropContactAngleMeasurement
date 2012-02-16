# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:40:30 2012

@author: rafik
"""

import helper as h

import cv2
import time
import numpy as np


class outHistogram(h.AbstractPlugin):
    

    def __init__(self):
        
        inp0 = h.createDataDescriptor(
            name="Framecounter",
            describtion="",
            datatype=h.Int)
        
        inp1 = h.createDataDescriptor(
            name="Frame",
            describtion="The frame, whose histogram should be displayed",
            datatype=h.Image,
            embeddedtype=h.img_Any)        
            
        self.inputinfo = [inp0, inp1]
        self.outputinfo = None


    
    def config(self, colorchannels = [0]):
        self.colorchannels = colorchannels

        print ' - outHisto: setup Histogram of streamelement %s, channel %s'% (self.inp_ch[1], colorchannels)

    
    def __call__(self, data):
        print ' - outHisto: display data nr %.0f @t: %f' % (data[self.inp_ch[0]], time.time())
        print ' - outHisto: display the Histogram of streamelement %s, channels %s, frame %s'% (self.inp_ch[1], self.colorchannels, self.inp_ch[0])
        

        hist = cv2.calcHist( [data[self.inp_ch[1]]], self.colorchannels, None, [256], [0, 255] )
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX);
        #print hist
        bin_count = hist.shape[0]
        bin_w = 2
        bin_max_h = 200
        img = np.ones((int(bin_max_h*1.1), bin_count*bin_w, 3), np.uint8)*[70,255,255]*255 #last list is background color
    
        #print hist
        for i in xrange(bin_count):
            val = hist[i]
            h = int(val*bin_max_h)
            #print h
            cv2.rectangle(img, (i*bin_w+2, int(bin_max_h*1.1)), ((i+1)*bin_w-2, int(bin_max_h*1.1)-h), [int(255*255.0*i/bin_count)]*3, -1)
        #img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)       
    
        
        print ' - outHisto: finished and waiting for key @t: %f' % (time.time())
        cv2.waitKey(1)



if __name__ == '__main__':
    #getData()
    pass