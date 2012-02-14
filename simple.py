# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

#import time
import cv2

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkNull as wrkNull
import plugins.wrkInvert as wrkInv
import plugins.outSimpleDisplay as outSD
import plugins.outHistogram as outHG
#import plugins.wrkEdgeFit as wrkEdge


inp = inpSFG.inpSimpleFrameGrabber()
wrk0 = wrkNull.wrkNull()
wrk1 = wrkInv.wrkInvert()

#wrk = wrkEdge.wrkEdgeFit()
#out = outSD.outSimpleDisplay() #display orginal
out0 = outSD.outSimpleDisplay() # display brighened orignal with edges overlay in red
out1 = outHG.outHistogram()


inp.setup()
wrk0.setup([0,1])
wrk1.setup([1])
out0.setup([0,4])
out1.setup([0,1])



inp.config('bin/demo.avi')
wrk0.config()
wrk1.config()
out0.config()
out1.config()



data = []

inp()

data.extend(inp())
data.extend(wrk0(data))
data.extend(wrk1(data))

out0(data)
out1(data)

cv2.waitKey()