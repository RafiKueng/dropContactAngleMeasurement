# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 00:13:54 2012

@author: rafael kueng
@contact: rafael.kueng@uzh.ch
"""

#from os import sys

import multiprocessing as mproc

#import numpy as np
#import matplotlib as mplib

import time

#import random as rnd

import Handler as H

#tmp, this is later done by plugin manager
import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkNull as wrkNull
import plugins.wrkInvert as wrkInv
import plugins.wrkDev as wrkDev
import plugins.outSimpleDisplay as outSD


testrange = range(0,100)



#-----------------------------------------------------------------------------
# define processes
#-----------------------------------------------------------------------------




#-----------------------------------------------------------------------------
# main section
#-----------------------------------------------------------------------------     
   
def main():
    print "main"
    
    #num_processorhandlers = min(1,mproc.cpu_count-1)
    num_workhandlers = 2
    
    # set up data pipes and queue
    result_queue = mproc.Queue()
    datapipes = [mproc.Pipe(False) for i in xrange(num_workhandlers)]
    
    h_input = H.InputHandler(
                [datapipes[i][1] for i in xrange(num_workhandlers)],
                [inpSFG.inpSimpleFrameGrabber()])
                 
    h_work = [H.WorkerHandler(
                    datapipes[i][0], result_queue, [wrkDev.wrkDev()])
                for i in xrange(num_workhandlers)]
                
    waittime = [0,0]
    for i, handler in enumerate(h_work):
        handler.setup(waittime[i])
                
    h_output = H.OutputHandler(result_queue, [outSD.outSimpleDisplay()])
    processes = list([h_input, h_output])
    processes.extend(h_work)
    
    # start all the processes
    [p.start() for p in processes]
    
    #h_input.start()
    #h_output.start()
    #h_work[0].start()
    
    
    # cleaning up
    h_input.join() #close the input handler
    [handler.join() for handler in h_work] #wait for the workers to finish
    h_output.join() #wait for ouput to finish writing
    result_queue.close() #close the 
    result_queue.join_thread()







def init_class():
    """gets called when the module is imported"""
    #print "imported as a class: do nothing"
    pass



#-----------------------------------------------------------------------------
# general startup procedure
#-----------------------------------------------------------------------------

if __name__ == '__main__':

    def cmdmain(*args):
        try:
            main()
        except:
            # handle general exceptions
            raise
        else:
            return 0 #exit with errorcode 0 = everything ok

    #sys.exit(cmdmain(*sys.argv))
    cmdmain()
    
else:
    init_class()
    