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

inp = inpAFG.inpAveragingFrameGrabber()

#wrk0 = wrkNull.wrkNull()
#wrk1 = wrkInv.wrkInvert()
wrk2 = wrkEdge.wrkEdgeFit()

out0 = outSD.outSimpleDisplay()




inp.setup()


#wrk0.setup([0,1])
#wrk1.setup([1])
wrk2.setup([1])

out0.setup([0,1])
#out1.setup([0,2])





inp.config(0)
#inp1.config('bin/demo.avi', 3)

#wrk0.config()
#wrk1.config()
wrk2.config()

#out0.config()
out0.config()



for i in range(50):
    data = []
    
    data.extend(inp())
    data.extend(wrk2(data))
    
    out0(data)
    cv2.waitKey()