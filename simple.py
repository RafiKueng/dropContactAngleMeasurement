# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 16:59:26 2012

@author: rafik
"""

import time

import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkNull as wrkNull
import plugins.wrkInvert as wrkInv
import plugins.outSimpleDisplay as outSD

inp = inpSFG.inpSimpleFrameGrabber()
wrk = wrkNull.wrkNull() #wrkInv.wrkInvert()
out = outSD.outSimpleDisplay()

inp.setup('bin/testfile.mpg')
wrk.setup()
out.setup()

data = inp.getData()
data = inp.getData()
data = inp.getData()
data = wrk.procData(data)
out.writeData(data)

time.sleep(5)