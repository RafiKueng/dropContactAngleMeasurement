# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

import time
import cv2

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.inpAveragingFrameGrabber as inpAFG

import plugins.wrkNull as wrkNull
import plugins.wrkInvert as wrkInv
import plugins.wrkEdgeFit as wrkEdge

import plugins.outSimpleDisplay as outSD
import plugins.outHistogram as outHG

inp = inpSFG.inpSimpleFrameGrabber()
inp1 = inpAFG.inpAveragingFrameGrabber()

#wrk0 = wrkNull.wrkNull()
#wrk1 = wrkInv.wrkInvert()
wrk2 = wrkEdge.wrkEdgeFit()

out0 = outSD.outSimpleDisplay() #display orginal
out1 = outSD.outSimpleDisplay() # display brighened orignal with edges overlay in red
out2 = outHG.outHistogram()




inp.setup()
inp1.setup()

#wrk0.setup([0,1])
#wrk1.setup([1])
wrk2.setup([1])

out0.setup([0,1])
out1.setup([0,2])





#inp.config('0')
inp1.config('bin/demo.avi', 3)

#wrk0.config()
#wrk1.config()
wrk2.config()

#out0.config()
out1.config()

for i in range(10):
    inp1()


for i in range(1000):
    data = []
    
    #inp()
    t1=time.clock()
    data.extend(inp1())
    t2=time.clock()
    print "inp: time taken:", (t2-t1)
    
    
    
    
    
    #data.extend(wrk0(data))
    #data.extend(wrk1(data))

    t1=time.clock()
    data.extend(wrk2(data))
    t2=time.clock()
    print "wrk: time taken:", (t2-t1)
    print 'angle', data[3]

#    n=50
#    t1=time.clock()
#    for i in range(n):
#        wrk2(data)
#    t2=time.clock()
#    print "time taken:", (t2-t1) / n
    #print data
    
    
    #out0(data)
    out1(data)

    cv2.waitKey()