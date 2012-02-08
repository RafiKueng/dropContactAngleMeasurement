# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 00:13:54 2012

@author: rafael kueng
@contact: rafael.kueng@uzh.ch
"""

from os import sys

import multiprocessing as mproc

import numpy as np
import matplotlib as mplib
import cv
import copy

import time
import random as rnd



#tmp, this is later done by plugin manager
import plugins.inpSimpleFrameGrabber as inpSFG
import plugins.wrkNull as wrkNull
import plugins.outSimpleDisplay as outSD



#-----------------------------------------------------------------------------
# define processes
#-----------------------------------------------------------------------------

class InputHandler(mproc.Process):
    """handels the input plugins, feeds the pipes
        
    will be spawn once    
    """   

    def __init__(self, datapipes, readers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipes = datapipes
        self.readers = readers
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        self.readers[0].setup()

        time.sleep(3)
        
        for i in [0,1]:
            print '%s: getframe %.0f @t: %f' % (self.name, i, time.time())
            frame = self.readers[0].getData()
            time.sleep(1)            
            print '%s: sendframe %.0f @t: %f' % (self.name, i, time.time())
            self.datapipes[0].send([frame])
            time.sleep(5)
        print '%s: stop'%self.name
        
#    def __getstate__(self):
#        return self.datapipes, self.readers
#        
#    def __setstate__(self, state):
#        self.datapipes, self.readers = state
        

class WorkerHandler(mproc.Process):
    """handels the processing of the data
    
    can possibly be spawn multiple times (depening on no of cpu cores)    
    """     
    
    def __init__(self, datapipe, result_queue, workers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipe = datapipe
        self.result_queue = result_queue
        self.workers = workers
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        self.workers[0].setup()        
        
        time.sleep(3)
        
        for i in [0,1]:
            print '%s: waiting for data %.0f @t: %f' % (self.name, i, time.time())
            data = self.datapipe.recv() #waits till it gets something
            print '%s: got data @t: %f' % (self.name, time.time())
            
            print '%s: got data @t: %f' % (self.name, time.time())
            data = self.workers[0].procData(data)        
            
            #print time.clock()
            self.result_queue.put(data)
        print '%s: stop'%self.name
        
#    def __getstate__(self):
#        return 'bla'
#        
#    def __setstate__(self, str):
#        pass



        
class OutputHandler(mproc.Process):
    """handels the output (display, saving) of the data
    
    will be spawn once    
    """     
    
    def __init__(self, result_queue, writers):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.result_queue = result_queue
        self.writers = writers
        #self.writers[0].init()
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        self.writers[0].setup()        
        
        for i in [0,1]:
            time.sleep(5)
            data = self.result_queue.get()
            print '%s: got dataframe from queue @t: %f' % (self.name, time.time())
            self.writers[0].writeData(data)
        print '%s: stopping @t: %f' % (self.name, time.time())
        
#    def __getstate__(self):
#        return 'bla'
#        
#    def __setstate__(self, str):
#        pass


#-----------------------------------------------------------------------------
# main section
#-----------------------------------------------------------------------------     
   
def main():
    print "main"
    
    #num_processorhandlers = min(1,mproc.cpu_count-1)
    num_workhandlers = 1
    
    # set up data pipes and queue
    result_queue = mproc.Queue()
    datapipes = [mproc.Pipe(False) for i in xrange(num_workhandlers)]
    
    h_input = InputHandler(
                [datapipes[i][1] for i in xrange(num_workhandlers)],
                [inpSFG.inpSimpleFrameGrabber()])
                 
    h_work = [WorkerHandler(
                    datapipes[i][0], result_queue, [wrkNull.wrkNull()])
                for i in xrange(num_workhandlers)]
                
    h_output = OutputHandler(result_queue, [outSD.outSimpleDisplay()])
    processes = list([h_input, h_output])
    processes.extend(h_work)
    
    # start all the processes
    [p.start() for p in processes]
    
    #h_input.start()
    #h_output.start()
    #h_work[0].start()
    
    
    # cleaning up
    result_queue.close()
    result_queue.join_thread()
    [p.join() for p in processes]
    #h_input.join()
    #h_work[0].join()



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
    