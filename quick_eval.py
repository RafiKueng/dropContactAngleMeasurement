# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

#import time
#import cv2

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.inpAveragingFrameGrabber as inpAFG

#import plugins.wrkNull as wrkNull
#import plugins.wrkInvert as wrkInv
import plugins.wrkEdgeFit as wrkEdge

import plugins.outSimpleDisplay as outSD
#import plugins.outHistogram as outHG
import plugins.outSimpleCSVWriter as outCSV
import plugins.outSaveFrame as outFrame

#inp = inpSFG.inpSimpleFrameGrabber()
inp1 = inpAFG.inpAveragingPlayPauseFrameGrabber()

#wrk0 = wrkNull.wrkNull()
#wrk1 = wrkInv.wrkInvert()
wrk2 = wrkEdge.wrkEdgeFit()

out0 = outSD.outSimpleDisplay() #display orginal
out1 = outSD.outSimpleDisplay() # display brighened orignal with edges overlay in red
#out2 = outHG.outHistogram()
out3 = outCSV.outSimpleCSVWriter()
out4 = outFrame.outSaveFrame()



#inp.setup()
inp1.setup()

#wrk0.setup([0,1])
#wrk1.setup([1])
wrk2.setup([1])

out0.setup([0,1]) #display orginal image
out1.setup([0,2]) #display the edidet file

out3.setup([0,3])
out4.setup([0,2])



#inp.config('0')
inp1.config('bin/demo.avi', 3)

#wrk0.config()
#wrk1.config()
wrk2.config()

#out0.config()
out1.config()

folder = "outp"
filename = "testing"
path = folder + "/" + filename

out3.config(path)
out4.config(path)

print "there are that many frames: ", inp1.nFrames

for i in range(10):
    inp1()


for i in range(int(inp1.nFrames)):
    data = []
    
    #inp()
    data.extend(inp1())
    data.extend(wrk2(data))

    print 'angle', data[3]

    #out0(data)
    out1(data)
    out3(data)
    out4(data)

    #cv2.waitKey()
    #exit()
    
inp1.finish()
wrk2.finish()
out1.finish()
out3.finish()
out4.finish()