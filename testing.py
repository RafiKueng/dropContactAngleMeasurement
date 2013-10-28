# -*- coding: utf-8 -*-
"""
Created on Tue May 01 15:53:49 2012

@author: rafik
"""
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
        

class Foo():
    class Bar():
        val1=0
        val2=0
        
    def __init__(self):
        bar = Foo.Bar()
        print bar.val1
        bar.val1 = 3
        print bar.val1
        
        bar2 = Foo.Bar()
        print bar2.val1
        print bar.val1        
        


#t = test("testclass.csv")
#t()
f = Foo()

"""

import sys
v = sys.argv[1]
print v[0:-4]