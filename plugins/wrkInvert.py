# -*- coding: utf-8 -*-
"""
Demo Plugin
Inverts the picture

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

import helper as h

import cv2
import time


class wrkInvert(h.AbstractPlugin):

    def __init__(self):
            
        inp0 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.iAny)
            
        self.inputinfo = [inp0]
        
        out0 = h.createDataDescriptor(
            name="TransposedFrame",
            describtion="the same frame, transposed",
            datatype=h.Image,
            embeddedtype=h.iAny)        
            
        self.outputinfo = [out0]


    def config(self, *args):
        pass
    

    def __call__(self, data):
        print ' - wrkInvert: processing data @t: %f' % (time.time())
        #time.sleep(1)
        
        return [cv2.transpose(data[self.inp_ch[0]])]
        

if __name__ == '__main__':
    #getData()
    pass
    