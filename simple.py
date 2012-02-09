# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

import time
import cv2

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkNull as wrkNull
import plugins.wrkInvert as wrkInv
import plugins.outSimpleDisplay as outSD
import plugins.wrkEdgeFit as wrkEdge

inp = inpSFG.inpSimpleFrameGrabber()
#wrk = wrkNull.wrkNull() #wrkInv.wrkInvert()
wrk = wrkEdge.wrkEdgeFit()
#out = outSD.outSimpleDisplay() #display orginal
out2 = outSD.outSimpleDisplay() # display brighened orignal with edges overlay in red

inp.setup('bin/demo.avi')
wrk.setup()
#out.setup(1) 
out2.setup(2)

data = inp.getData()
data = inp.getData()
data = inp.getData()
data.append(wrk.procData(data))
#out.writeData(data)
out2.writeData(data)

cv2.waitKey()