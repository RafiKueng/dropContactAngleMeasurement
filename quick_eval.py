# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

#import time
#import cv2
import sys
import os
import numpy as np

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

v = sys.argv[2]
#print v[0:-4]
inpfilename = v[0:-4]#"Rh111BN_11_1_100mV"

w = sys.argv[1] #folder in basepath

#basepath = "G:/sinergia_data/" + w
basepath = "./" + w

inp.config(basepath+'/'+inpfilename+".avi")
#inp1.config('bin/Rh111BN_11_1_100mV.avi', 1)

#wrk0.config()
#wrk1.config()
wrk2.config()

#out0.config()
#out1.config()

folder = basepath + "/outp"
filename = inpfilename
path = folder + "/" + filename

out3.config(path)
outIWrt.config(path)


#take a few pictures from the start to train baseline and pipette pos

#inp()
#inp()
#inp()

print '  nframes:', inp.nFrames, 'fps:', inp.fps
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

print "Read frames for training"
trainimg = []

sys.stdout.write('  [')
for i in range(64):
    sys.stdout.write('.')
sys.stdout.write(']')
for i in range(64+1):
    sys.stdout.write('\b')
sys.stdout.flush()

for x in range(64):

    img = inp.getFrameNr(inp.nFrames//64*x)[1]
    #outDisp([x,img])
    trainimg.append(img)
    sys.stdout.write('*')
    sys.stdout.flush()
sys.stdout.write('\n')
sys.stdout.flush()  
#print "\nTrain the Worker"
wrk2.train(trainimg)

#for d in trainimg:
#    wrk2([1, d], True)
#    outDisp([x,wrk2.lastpic])
    

inp.setPos(0)

for i in range(int(inp.nFrames)):
    data = []
    saved = False
    #inp()
    data.extend(inp())
    
    #add the time in msec    
    data.append(i*1000/inp.fps)

    # do the work
    data.extend(wrk2(data, i%25==0)) #save each 25th frame

    # write the frame?
    if wrk2.saveImg:
        outIWrt([data[0],wrk2.lastpic])

    #status output to stdout
    print '  f#:%04i (%3i%%) | ch:%2i | ang:%4s,%4s | res:%4s,%4s | bas:%4s,%4s ' % (
            data[0], data[0]*100 // inp.nFrames,
            data[3].chosen,
            '----' if np.isnan(data[3].angle.angle[0]) else '%4.1f'%data[3].angle.angle[0],
            '----' if np.isnan(data[3].angle.angle[1]) else '%4.1f'%data[3].angle.angle[1],
            '----' if np.isnan(data[3].angle.residuals[0]) else '%4i'%data[3].angle.residuals[0],
            '----' if np.isnan(data[3].angle.residuals[1]) else '%4i'%data[3].angle.residuals[1],
            '----' if np.isnan(data[3].angle.root[0]) else '%4i'%data[3].angle.root[0],
            '----' if np.isnan(data[3].angle.root[1]) else '%4i'%data[3].angle.root[1]
            ) + ('*' if wrk2.saveImg else ' ')
    
    #out0(data)
    #out1(data)
    out3(data) #write to csv

    
#inp.finish()
#wrk2.finish()
#out1.finish()
out3.finish() #close file
#out4.finish()