# -*- coding: utf-8 -*-
"""
Basic worker layout, doesn't do anything except
waiting and passing the data on

Created on Tue Feb 07 15:17:12 2012

@author: rafik
"""

import helper as h

#import cv2
import time


class wrkNull(h.AbstractPlugin):

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
        
        out0 = h.createDataDescriptor(
            name="Frame",
            describtion="The unprocceded frame, grabbed from video or camera",
            datatype=h.Image,
            embeddedtype=h.iAny)        
            
        self.outputinfo = [out0]

    
    def config(self):
        pass
    
    def __call__(self, data):
        time.sleep(2)
        return data
        

if __name__ == '__main__':
    #getData()
    pass    