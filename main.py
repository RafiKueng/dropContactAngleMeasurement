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

import time
import random as rnd


#-----------------------------------------------------------------------------
# define processes
#-----------------------------------------------------------------------------

class InputHandler(mproc.Process):
    """handels the input plugins, feeds the pipes
        
    will be spawn once    
    """   

    def __init__(self, datapipes):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipes = datapipes        
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        time.sleep(1)
        self.datapipes[0].send('hi there')
        print '%s: stop'%self.name
        

class WorkHandler(mproc.Process):
    """handels the processing of the data
    
    can possibly be spawn multiple times (depening on no of cpu cores)    
    """     
    
    def __init__(self, datapipe, result_queue):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.datapipe = datapipe
        self.result_queue = result_queue
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        time.sleep(5)
        tmp = self.datapipe.recv()
        print '%s: i got message: <%s>, putting it on the stack @t: %f' % (self.name, tmp, time.time())
        #print time.clock()
        self.result_queue.put(tmp)
        print '%s: stop'%self.name
        
        
class OutputHandler(mproc.Process):
    """handels the output (display, saving) of the data
    
    will be spawn once    
    """     
    
    def __init__(self, result_queue):
        mproc.Process.__init__(self)
        print '%s: init'%self.name
        self.result_queue = result_queue
        
    def run(self):
        print '%s: run @t: %f' % (self.name, time.time())
        time.sleep(2)
        tmp = 'rien'#self.result_queue.get()
        print '%s: stop: got <%s> from queue @t: %f' % (self.name, tmp, time.time())
        



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
    
    h_input = InputHandler([datapipes[i][1] for i in xrange(num_workhandlers)])
    h_work = [WorkHandler(datapipes[i][0], result_queue)
                for i in xrange(num_workhandlers)]
    h_output = OutputHandler(result_queue)
    processes = list([h_input, h_output])
    processes.extend(h_work)
    
    # start all the processes
    [p.start() for p in processes]
    
    
    # cleaning up
    result_queue.close()
    result_queue.join_thread()
    [p.join() for p in processes]



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
    