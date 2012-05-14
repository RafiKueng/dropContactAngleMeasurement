# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

#import time
#import cv2
import sys

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.inpAveragingFrameGrabber as inpAFG

#import plugins.wrkNull as wrkNull
#import plugins.wrkInvert as wrkInv
import plugins.wrkEdgeFit as wrkEdge

import plugins.outSimpleDisplay as outSD
#import plugins.outHistogram as outHG
import plugins.outSimpleCSVWriter as outCSV
import plugins.outSaveFrame as outFrame

inp = inpSFG.inpSimpleFrameGrabber()
#inp1 = inpAFG.inpAveragingPlayPauseFrameGrabber()

#wrk0 = wrkNull.wrkNull()
#wrk1 = wrkInv.wrkInvert()
wrk2 = wrkEdge.wrkEdgeFit()

#out0 = outSD.outSimpleDisplay() #display orginal
#out1 = outSD.outSimpleDisplay() # display brighened orignal with edges overlay in red
#out2 = outHG.outHistogram()
out3 = outCSV.outSimpleCSVWriter()
outIWrt = outFrame.outSaveFrame()
outDisp = outSD.outSimpleDisplay() #display a frame on demand... (abuse the plugin)


inp.setup()
#inp1.setup()

#wrk0.setup([0,1])
#wrk1.setup([1])
wrk2.setup([1])

#out0.setup([0,1]) #display orginal image
#out1.setup([0,2]) #display the edidet file

out3.setup([0,2])
outIWrt.setup([0,1]) #remember: this plaugin is abused and not called with the datastream
outDisp.setup([0,1]) #remember: this plaugin is abused and not called with the datastream

v = sys.argv[1]
print v[0:-4]
inpfilename = v[0:-4]#"Rh111BN_11_1_100mV"

inp.config("D:/sinergia_data/"+inpfilename+".avi")
#inp1.config('bin/Rh111BN_11_1_100mV.avi', 1)

#wrk0.config()
#wrk1.config()
wrk2.config()

#out0.config()
#out1.config()

folder = "D:/sinergia_data/outp"
filename = inpfilename
path = folder + "/" + filename

out3.config(path)
outIWrt.config(path)

print "there are that many frames: ", inp.nFrames

#take a few pictures from the start to train baseline and pipette pos

inp()
inp()
inp()

trainimg = []
for x in range(128):

    trainimg.append(inp()[1])
    
#print trainimg
wrk2.train(trainimg)

#for i in range(425):
#    inp()
    #pass

inp.setPos(0)

for i in range(int(inp.nFrames)):
    data = []
    
    #inp()
    data.extend(inp())



    if i%25==0:
        data.extend(wrk2(data, True))
        fn = data[0]
        #outDisp([fn,wrk2.lastpic])
        outIWrt([fn,wrk2.lastpic])
    else:
        data.extend(wrk2(data, False))

    print '   angle', data[2].toString()     
    #out0(data)
    #out1(data)
    out3(data)


    #cv2.waitKey()
    #exit()
    
inp.finish()
wrk2.finish()
#out1.finish()
out3.finish()
#out4.finish()