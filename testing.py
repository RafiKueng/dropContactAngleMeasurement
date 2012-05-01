# -*- coding: utf-8 -*-
"""
Created on Tue May 01 15:53:49 2012

@author: rafik
"""

import csv
import cv2

#c = csv.writer(open("MYFILE.csv", "wb"))
#c.writerow(["Name","Address","Telephone","Fax","E-mail","Others"])
class base():
    def __init__(self):
        print "baseinit"

class test():
    def __init__(self, filename):
        print "classinti"
        self.filename = filename
        
    def __call__(self):
        self.f = open(self.filename, "wb")
        self.c = csv.writer(self.f)
        self.c.writerow(["Name","Address","Telephone","Fax","E-mail","Others"])
        
        
t = test("testclass.csv")
t()